import os

from typing import Optional
import multiprocessing
from queue import Empty

from warp_beacon.scraper.exceptions import NotFound, UnknownError, TimeOut, Unavailable, FileTooBig, YotubeLiveError, YotubeAgeRestrictedError, IGRateLimitOccurred, CaptchaIssue, AllAccountsFailed
from warp_beacon.mediainfo.video import VideoInfo
from warp_beacon.mediainfo.audio import AudioInfo
from warp_beacon.mediainfo.silencer import Silencer
from warp_beacon.compress.video import VideoCompress
from warp_beacon.uploader import AsyncUploader
from warp_beacon.jobs import Origin
from warp_beacon.jobs.download_job import DownloadJob
from warp_beacon.jobs.upload_job import UploadJob
from warp_beacon.jobs.types import JobType
from warp_beacon.scraper.account_selector import AccountSelector
from warp_beacon.scheduler.scheduler import IGScheduler

import logging

ACC_FILE = os.environ.get("SERVICE_ACCOUNTS_FILE", default="/var/warp_beacon/accounts.json")

class AsyncDownloader(object):
	__JOE_BIDEN_WAKEUP = None
	workers = []
	allow_loop = None
	job_queue = multiprocessing.Queue()
	uploader = None
	workers_count = 0
	auth_event = multiprocessing.Event()
	acc_selector = None
	scheduler = None

	def __init__(self, uploader: AsyncUploader, workers_count: int) -> None:
		self.allow_loop = multiprocessing.Value('i', 1)
		self.uploader = uploader
		self.workers_count = workers_count
		self.acc_selector = AccountSelector(ACC_FILE)
		self.scheduler = IGScheduler(self)
		self.scheduler.start()

	def __del__(self) -> None:
		self.stop_all()

	def start(self) -> None:
		for _ in range(self.workers_count):
			proc = multiprocessing.Process(target=self.do_work)
			self.workers.append(proc)
			proc.start()

	def get_media_info(self, path: str, fr_media_info: dict={}, media_type: JobType = JobType.VIDEO) -> Optional[dict]:
		media_info = None
		try:
			if path:
				if media_type == JobType.VIDEO:
					video_info = VideoInfo(path)
					media_info = video_info.get_finfo(tuple(fr_media_info.keys()))
					media_info.update(fr_media_info)
					if not media_info.get("thumb", None):
						media_info["thumb"] = video_info.generate_thumbnail()
					media_info["has_sound"] = video_info.has_sound()
				elif media_type == JobType.AUDIO:
					audio_info = AudioInfo(path)
					media_info = audio_info.get_finfo(tuple(fr_media_info.keys()))
		except Exception as e:
			logging.error("Failed to process media info!")
			logging.exception(e)

		return media_info

	def try_next_account(self, job: DownloadJob, report_error: str = None) -> None:
		logging.warning("Switching account!")
		if job.account_switches > self.acc_selector.count_service_accounts(job.job_origin):
			raise AllAccountsFailed("All config accounts failed!")
		if report_error:
			self.acc_selector.bump_acc_fail("rate_limits")
		self.acc_selector.next()
		cur_acc = self.acc_selector.get_current()
		logging.info("Current account: '%s'", str(cur_acc))
		job.account_switches += 1

	def do_work(self) -> None:
		logging.info("download worker started")
		while self.allow_loop.value == 1:
			try:
				job = None
				try:
					job = self.job_queue.get()
					if job is self.__JOE_BIDEN_WAKEUP:
						continue
					actor = None
					try:
						items = []
						if job.job_origin is Origin.UNKNOWN:
							logging.warning("Unknown task origin! Skipping.")
							continue
						if not job.in_process:
							actor = None
							self.acc_selector.set_module(job.job_origin)
							if job.job_origin is Origin.INSTAGRAM:
								from warp_beacon.scraper.instagram.instagram import InstagramScraper
								actor = InstagramScraper(self.acc_selector.get_current())
							elif job.job_origin is Origin.YT_SHORTS:
								from warp_beacon.scraper.youtube.shorts import YoutubeShortsScraper
								actor = YoutubeShortsScraper(self.acc_selector.get_current())
							elif job.job_origin is Origin.YT_MUSIC:
								from warp_beacon.scraper.youtube.music import YoutubeMusicScraper
								actor = YoutubeMusicScraper(self.acc_selector.get_current())
							elif job.job_origin is Origin.YOUTUBE:
								from warp_beacon.scraper.youtube.youtube import YoutubeScraper
								actor = YoutubeScraper(self.acc_selector.get_current())
							actor.send_message_to_admin_func = self.send_message_to_admin
							actor.auth_event = self.auth_event
							while True:
								try:
									if job.session_validation:
										logging.info("Validating '%s' session ...", job.job_origin.value)
										actor.validate_session()
										logging.info("done")
									else:
										logging.info("Downloading URL '%s'", job.url)
										items = actor.download(job.url)
									break
								except NotFound as e:
									logging.warning("Not found error occurred!")
									logging.exception(e)
									self.uploader.queue_task(job.to_upload_job(
										job_failed=True,
										job_failed_msg="Unable to access to media under this URL. Seems like the media is private.")
									)
									self.send_message_to_admin(
										f"Task {job.job_id} failed. URL: '{job.url}'. Reason: 'NotFound'."
									)
									break
								except Unavailable as e:
									logging.warning("Not found or unavailable error occurred!")
									logging.exception(e)
									if job.unvailable_error_count > self.acc_selector.count_service_accounts(job.job_origin):
										self.uploader.queue_task(job.to_upload_job(
											job_failed=True,
											job_failed_msg="Video is unvailable for all your service accounts.")
										)
										break
									job.unvailable_error_count += 1
									logging.info("Trying to switch account")
									self.acc_selector.next()
									self.job_queue.put(job)
									break
								except TimeOut as e:
									logging.warning("Timeout error occurred!")
									logging.exception(e)
									self.uploader.queue_task(job.to_upload_job(
										job_failed=True,
										job_failed_msg="Failed to download content due timeout error. Please check you Internet connection, retry amount or request timeout bot configuration settings.")
									)
									self.send_message_to_admin(
										f"Task {job.job_id} failed. URL: '{job.url}'. Reason: 'TimeOut'."
									)
									break
								except FileTooBig as e:
									logging.warning("Telegram limits exceeded :(")
									logging.exception(e)
									self.uploader.queue_task(job.to_upload_job(
										job_failed=True,
										job_failed_msg="Unfortunately this file has exceeded the Telegram limits. A file cannot be larger than 2 gigabytes.")
									)
									self.send_message_to_admin(
										f"Task {job.job_id} failed. URL: '{job.url}'. Reason: 'FileTooBig'."
									)
									break
								except IGRateLimitOccurred as e:
									logging.warning("IG ratelimit occurred :(")
									logging.exception(e)
									self.try_next_account(job, report_error="rate_limits")
									self.job_queue.put(job)
									break
								except CaptchaIssue as e:
									logging.warning("Challange occurred!")
									logging.exception(e)
									self.try_next_account(job)
									self.job_queue.put(job)
									break
								except YotubeLiveError as e:
									logging.warning("Youtube Live videos are not supported. Skipping.")
									logging.exception(e)
									self.uploader.queue_task(job.to_upload_job(
										job_failed=True,
										job_failed_msg="Youtube Live videos are not supported. Please wait until the live broadcast ends.")
									)
									break
								except YotubeAgeRestrictedError as e:
									logging.error("Youtube Age Restricted error")
									logging.exception(e)
									self.uploader.queue_task(job.to_upload_job(
										job_failed=True,
										job_failed_msg="Youtube Age Restricted error. Check your bot Youtube account settings.")
									)
									self.send_message_to_admin(
										f"Task {job.job_id} failed. URL: '{job.url}'. Reason: 'YotubeAgeRestrictedError'."
									)
									break
								except AllAccountsFailed as e:
									logging.error("All accounts failed!")
									logging.exception(e)
									self.uploader.queue_task(job.to_upload_job(
										job_failed=True,
										job_failed_msg="All bot accounts failed to download content. Bot administrator noticed about the issue.")
									)
									self.send_message_to_admin(
										f"Task {job.job_id} failed. URL: '{job.url}'. Reason: 'AllAccountsFailed'."
									)
									break
								except (UnknownError, Exception) as e:
									logging.warning("UnknownError occurred!")
									logging.exception(e)
									exception_msg = ""
									if hasattr(e, "message"):
										exception_msg = e.message
									else:
										exception_msg = str(e)
									if "geoblock_required" in exception_msg:
										if job.geoblock_error_count > self.acc_selector.count_service_accounts(job.job_origin):
											self.uploader.queue_task(job.to_upload_job(
												job_failed=True,
												job_failed_msg="This content does not accessible for all yout bot accounts. Seems like author blocked certain regions.")
											)
											self.send_message_to_admin(
												f"Task {job.job_id} failed. URL: '{job.url}'. Reason: 'geoblock_required'."
											)
											break
										job.geoblock_error_count += 1
										logging.info("Trying to switch account")
										self.acc_selector.next()
										self.job_queue.put(job)
										break
									self.uploader.queue_task(job.to_upload_job(
										job_failed=True,
										job_failed_msg="WOW, unknown error occured! Please [create issue](https://github.com/sb0y/warp_beacon/issues) with service logs.")
									)
									self.send_message_to_admin(
										f"Task {job.job_id} failed. URL: '{job.url}'. Reason: 'UnknownError'."
										f"Exception:\n```\n{exception_msg}\n```"
									)
									break

							if items:
								for item in items:
									media_info = {"filesize": 0}
									if item["media_type"] == JobType.VIDEO:
										media_info = self.get_media_info(item["local_media_path"], item.get("media_info", {}), JobType.VIDEO)
										logging.info("Final media info: %s", media_info)
										if media_info["filesize"] > 2e+9:
											logging.info("Filesize is '%d' MiB", round(media_info["filesize"] / 1024 / 1024))
											logging.info("Detected big file. Starting compressing with ffmpeg ...")
											self.uploader.queue_task(job.to_upload_job(
												job_warning=True,
												job_warning_msg="Downloaded file size is bigger than Telegram limits! Performing video compression. This may take a while.")
											)
											ffmpeg = VideoCompress(file_path=item["local_media_path"])
											new_filepath = ffmpeg.generate_filepath(base_filepath=item["local_media_path"])
											if ffmpeg.compress_to(new_filepath, target_size=2000 * 1000):
												logging.info("Successfully compressed file '%s'", new_filepath)
												os.unlink(item["local_media_path"])
												item["local_media_path"] = new_filepath
												item["local_compressed_media_path"] = new_filepath
												media_info["filesize"] = VideoInfo.get_filesize(new_filepath)
												logging.info("New file size of compressed file is '%.3f'", media_info["filesize"])
										if not media_info["has_sound"]:
											item["media_type"] = JobType.ANIMATION
									elif item["media_type"] == JobType.AUDIO:
										media_info = self.get_media_info(item["local_media_path"], item.get("media_info", {}), JobType.AUDIO)
										media_info["performer"] = item.get("performer", None)
										media_info["thumb"] = item.get("thumb", None)
										logging.info("Final media info: %s", media_info)
									elif item["media_type"] == JobType.COLLECTION:
										for chunk in item["items"]:
											for v in chunk:
												if v["media_type"] == JobType.VIDEO:
													col_media_info = self.get_media_info(v["local_media_path"], v["media_info"])
													media_info["filesize"] += int(col_media_info.get("filesize", 0))
													v["media_info"] = col_media_info
													if not v["media_info"]["has_sound"]:
														silencer = Silencer(v["local_media_path"])
														silent_video_path = silencer.add_silent_audio()
														os.unlink(v["local_media_path"])
														v["local_media_path"] = silent_video_path
														v["media_info"].update(silencer.get_finfo())
														v["media_info"]["has_sound"] = True

									job_args = {"media_type": item["media_type"], "media_info": media_info}
									if item["media_type"] == JobType.COLLECTION:
										job_args["media_collection"] = item["items"]
										if item.get("save_items", None) is not None:
											job_args["save_items"] = item.get("save_items", False)
									else:
										job_args["local_media_path"] = item["local_media_path"]
										if item.get("local_compressed_media_path", None):
											job_args["local_media_path"] = item.get("local_compressed_media_path", None)

									job_args["canonical_name"] = item.get("canonical_name", "")

									logging.debug("local_media_path: '%s'", job_args.get("local_media_path", ""))
									logging.debug("media_collection: '%s'", str(job_args.get("media_collection", {})))
									#logging.info(job_args)
									upload_job = job.to_upload_job(**job_args)
									if upload_job.is_empty():
										logging.info("Upload job is empty. Nothing to do here!")
										self.uploader.queue_task(job.to_upload_job(
											job_failed=True,
											job_failed_msg="Seems like this link doesn't contains any media.")
										)
									else:
										self.uploader.queue_task(upload_job)
						else:
							logging.info("Job already in work in parallel worker. Redirecting job to upload worker.")
							self.uploader.queue_task(job.to_upload_job())
					except Exception as e:
						logging.error("Error inside download worker!")
						logging.exception(e)
						self.notify_task_failed(job)
				except Empty:
					pass
			except Exception as e:
				logging.error("Exception occurred inside worker!")
				logging.exception(e)

		logging.info("Process done")

	def stop_all(self) -> None:
		self.allow_loop.value = 0
		self.scheduler.stop()
		for proc in self.workers:
			if proc.is_alive():
				logging.info("stopping process #%d", proc.pid)
				self.job_queue.put_nowait(self.__JOE_BIDEN_WAKEUP)
				proc.join()
				#proc.terminate()
				logging.info("process #%d stopped", proc.pid)
		self.workers.clear()

	def queue_task(self, job: DownloadJob) -> str:
		self.job_queue.put_nowait(job)
		return str(job.job_id)
	
	def notify_task_failed(self, job: DownloadJob) -> None:
		self.uploader.queue_task(job.to_upload_job(job_failed=True))

	def send_message_to_admin(self, text: str, yt_auth: bool = False) -> None:
		self.uploader.queue_task(UploadJob.build(
			is_message_to_admin=True,
			message_text=text,
			yt_auth=yt_auth
		))
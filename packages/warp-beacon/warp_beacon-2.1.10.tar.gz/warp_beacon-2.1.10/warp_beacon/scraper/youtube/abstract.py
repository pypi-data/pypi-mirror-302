import os, io
import pathlib
import time
import socket
import ssl

#from abc import abstractmethod
from typing import Callable, Union

import json

import requests
import urllib
import http.client
import requests
from PIL import Image

from warp_beacon.scraper.abstract import ScraperAbstract
from warp_beacon.mediainfo.abstract import MediaInfoAbstract
from warp_beacon.scraper.exceptions import TimeOut, Unavailable, extract_exception_message

from pytubefix import YouTube
from pytubefix.innertube import _default_clients
from pytubefix.streams import Stream
from pytubefix.innertube import InnerTube, _client_id, _client_secret
from pytubefix.exceptions import VideoUnavailable, VideoPrivate, MaxRetriesExceeded
from pytubefix import request

import logging

def patched_fetch_bearer_token(self) -> None:
	"""Fetch an OAuth token."""
	# Subtracting 30 seconds is arbitrary to avoid potential time discrepencies
	start_time = int(time.time() - 30)
	data = {
		'client_id': _client_id,
		'scope': 'https://www.googleapis.com/auth/youtube'
	}
	response = request._execute_request(
		'https://oauth2.googleapis.com/device/code',
		'POST',
		headers={
			'Content-Type': 'application/json'
		},
		data=data
	)
	response_data = json.loads(response.read())
	verification_url = response_data['verification_url']
	user_code = response_data['user_code']

	logging.warning("Please open %s and input code '%s'", verification_url, user_code)
	self.send_message_to_admin_func(
		f"Please open {verification_url} and input code `{user_code}`.\n\n"
		"Please select a Google account with verified age.\n"
		"This will allow you to avoid error the **AgeRestrictedError** when accessing some content.",
		yt_auth=True)
	self.auth_event.wait()

	data = {
		'client_id': _client_id,
		'client_secret': _client_secret,
		'device_code': response_data['device_code'],
		'grant_type': 'urn:ietf:params:oauth:grant-type:device_code'
	}
	response = request._execute_request(
		'https://oauth2.googleapis.com/token',
		'POST',
		headers={
			'Content-Type': 'application/json'
		},
		data=data
	)
	response_data = json.loads(response.read())

	self.access_token = response_data['access_token']
	self.refresh_token = response_data['refresh_token']
	self.expires = start_time + response_data['expires_in']
	self.cache_tokens()

class YoutubeAbstract(ScraperAbstract):
	DOWNLOAD_DIR = "/tmp"
	YT_SESSION_FILE = '/var/warp_beacon/yt_session_%d.json'

	def __init__(self, account: tuple) -> None:
		super().__init__(account)

	def __del__(self) -> None:
		pass

	def rename_local_file(self, filename: str) -> str:
		if not os.path.exists(filename):
			raise NameError("No file provided")
		path_info = pathlib.Path(filename)
		ext = path_info.suffix
		#old_filename = path_info.stem
		time_name = str(time.time()).replace('.', '_')
		new_filename = "%s%s" % (time_name, ext)
		new_filepath = "%s/%s" % (os.path.dirname(filename), new_filename)

		os.rename(filename, new_filepath)

		return new_filepath

	def remove_tmp_files(self) -> None:
		for i in os.listdir(self.DOWNLOAD_DIR):
			if "yt_download_" in i:
				os.unlink("%s/%s" % (self.DOWNLOAD_DIR, i))

	def download_thumbnail(self, url: str, timeout: int) -> Union[io.BytesIO, None]:
		try:
			reply = requests.get(url, timeout=(timeout, timeout))
			if reply.ok and reply.status_code == 200:
				image = Image.open(io.BytesIO(reply.content))
				image = MediaInfoAbstract.shrink_image_to_fit(image)
				io_buf = io.BytesIO()
				image.save(io_buf, format='JPEG')
				io_buf.seek(0)
				return io_buf
		except Exception as e:
			logging.error("Failed to download download thumbnail!")
			logging.exception(e)

		return None

	def _download_hndlr(self, func: Callable, *args: tuple[str], **kwargs: dict[str]) -> Union[str, dict, io.BytesIO]:
		ret_val = ''
		max_retries = int(os.environ.get("YT_MAX_RETRIES", default=self.YT_MAX_RETRIES_DEFAULT))
		pause_secs = int(os.environ.get("YT_PAUSE_BEFORE_RETRY", default=self.YT_PAUSE_BEFORE_RETRY_DEFAULT))
		timeout = int(os.environ.get("YT_TIMEOUT", default=self.YT_TIMEOUT_DEFAULT))
		timeout_increment = int(os.environ.get("YT_TIMEOUT_INCREMENT", default=self.YT_TIMEOUT_INCREMENT_DEFAULT))
		retries = 0
		while max_retries >= retries:
			try:
				kwargs["timeout"] = timeout
				ret_val = func(*args, **kwargs)
				break
			except MaxRetriesExceeded:
				# do noting, not interested
				pass
			#except http.client.IncompleteRead as e:
			except (socket.timeout,
					ssl.SSLError,
					http.client.IncompleteRead,
					http.client.HTTPException,
					requests.RequestException,
					urllib.error.URLError,
					urllib.error.HTTPError) as e:
				if hasattr(e, "code") and int(e.code) == 403:
					raise Unavailable(extract_exception_message(e))
				logging.warning("Youtube read timeout! Retrying in %d seconds ...", pause_secs)
				logging.info("Your `YT_MAX_RETRIES` values is %d", max_retries)
				logging.exception(extract_exception_message(e))
				if max_retries <= retries:
					self.remove_tmp_files()
					raise TimeOut(extract_exception_message(e))
				retries += 1
				timeout += timeout_increment
				time.sleep(pause_secs)
			except (VideoUnavailable, VideoPrivate) as e:
				raise Unavailable(extract_exception_message(e))

		return ret_val

	def yt_on_progress(self, stream: Stream, chunk: bytes, bytes_remaining: int) -> None:
		pass
		#logging.info("bytes: %d, bytes remaining: %d", chunk, bytes_remaining)

	def build_yt(self, url: str) -> YouTube:
		InnerTube.send_message_to_admin_func = self.send_message_to_admin_func
		InnerTube.auth_event = self.auth_event
		InnerTube.fetch_bearer_token = patched_fetch_bearer_token
		_default_clients["ANDROID"]["innertube_context"]["context"]["client"]["clientVersion"] = "19.08.35"
		_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID"]
		yt_opts = {"url": url, "on_progress_callback": self.yt_on_progress}
		#yt_opts["client"] = "WEB"
		yt_opts["use_oauth"] = True
		yt_opts["allow_oauth_cache"] = True
		yt_opts["token_file"] = self.YT_SESSION_FILE % self.account_index
		return YouTube(**yt_opts)

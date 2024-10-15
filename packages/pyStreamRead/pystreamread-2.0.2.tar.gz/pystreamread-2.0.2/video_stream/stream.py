import ffmpeg as ffmpeg
import numpy as np
import cv2
import subprocess
import time
import threading


from .log import logger


class VideoStream:
    def __init__(self, url, logger=logger, ffmpeg_log_level="info") -> None:
        self._url = url
        self._ip = url.split("://")[1].split(":")[0]
        self._logger = logger
        self._ffmpeg_log_level = ffmpeg_log_level
        self._bytes_size = 0
        self._width, self._height, self._fps = 0, 0, 0
        self._connect()
        threading.Thread(target=self._check).start()

    def _check(self):
        i = 1
        while True:
            time.sleep(1)
            i += 1
            if not self._check_ping():
                self.close()

    def _check_ping(self):
        command = ['ping', '-c', '1', '-W', '1', self._ip]
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)

            if "1 received" in output or "1 packets received" in output:
                return True
            else:
                return False
        except subprocess.CalledProcessError:
            return False

    def open(self):
        self._connect()

    def _connect(self):
        self._args = {
            "rtsp_transport": "tcp",
            "fflags": "nobuffer",
            "flags": "low_delay",
            "loglevel": self._ffmpeg_log_level,
        }

        url_ok = False
        while not url_ok:
            try:
                probe = ffmpeg.probe(self._url)  # add retries
            except Exception as e:
                self._logger.warning(f"url {self._url} is not ok...")
                continue
            else:
                url_ok = True

        cap_info = next(x for x in probe['streams'] if x['codec_type'] == 'video')

        fram_rate = str(cap_info['r_frame_rate'])
        self._logger.info(f"fps: {fram_rate}")

        self._width = cap_info['width']  # get video stream width
        self._height = cap_info['height']  # get video stream height

        up, down = fram_rate.split('/')
        self._fps = eval(up) / eval(down)
        self._logger.info(f"fps: {self._fps}")
        self._bytes_size = self._width * self._height * 3

        self._proc = (
            ffmpeg.input(self._url, **self._args)
            .output('pipe:', format='rawvideo', pix_fmt='rgb24')
            .overwrite_output()
            .run_async(pipe_stdout=True)
        )

    def stream_read(self):
        try:
            in_bytes = self._proc.stdout.read(self._bytes_size)  # read image
            if not in_bytes:
                return False, None

            # transfor to ndarray
            in_frame = np.frombuffer(in_bytes, np.uint8).reshape([self._height, self._width, 3])

            frame = cv2.cvtColor(in_frame, cv2.COLOR_RGB2BGR)  # change to BGR
        except:
            return False, None
        else:
            return True, frame

    def close(self):
        if self._proc is not None:
            self._proc.kill()  # close

    @property
    def fps(self):
        return self._fps

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

import add_path

import cv2

from video_stream import VideoStream


class VideoStreamTest:
    def __init__(self) -> None:
        self.video_stream = VideoStream(
            "rtsp://192.168.0.206:554/H264?W=1920&H=1440&BR=2000000&FPS=30",
            ffmpeg_log_level="debug"
        )


def connect_video_stream(vst):
    vst = VideoStreamTest()


def test_read_stream():
    vst = VideoStreamTest()
    no_connect_count = 0
    while True:
        try:
            ok, frame = vst.video_stream.stream_read()
            if not ok:
                if no_connect_count > 10:
                    vst.video_stream.close()
                    vst.video_stream.open()
                    no_connect_count = 0

                no_connect_count += 1
                continue
            cv2.imshow("frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except Exception as e:
            break


test_read_stream()

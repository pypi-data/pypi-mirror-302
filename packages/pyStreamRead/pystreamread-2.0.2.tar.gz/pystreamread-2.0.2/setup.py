from setuptools import setup, find_packages

setup(
    name='pyStreamRead',
    version='2.0.2',
    keywords=("rtsp", "rtmp", "video", "stream", "python", "video_stream"),
    license="MIT Licence",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["ffmpeg-python == 0.2.0", "future == 1.0.0", "numpy == 1.24.4", "opencv-python == 4.10.0.82"],
    # Metadata
    author='rui.li',
    author_email='jiangsulirui@gmail.com',
    description="video stream reading",
    long_description="video stream reading for rtsp or rtmp, not use opencv video capture but use ffmpeg",
    # url='https://github.com/your_username/your_package',
)

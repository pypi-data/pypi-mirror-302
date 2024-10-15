from setuptools import setup, find_packages

setup(
    name="StreamSender",
    version="0.0.2",
    author="liushihai02",
    author_email="liushihai02@58.com",
    packages=find_packages(),
    install_requires=[
        'scapy',
        'opencv-python',
        'pydub',
        'loguru',
        'python-librtmp'
    ],
    description="A SDK for sending RTP and RTMP streams",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.9',
)

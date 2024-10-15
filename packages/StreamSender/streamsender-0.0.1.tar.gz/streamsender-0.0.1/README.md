## description
功能：将音视频数据转换成rtp和rtmp包

## usage examples
安装av库
```bash
pip uninstall av && pip install av --no-binary av
```

具体使用方式请参考下面的示例：
```python
from streamers.rtp_sender import RTPSender
from streamers.rtmp_sender import RTMPSender
from pydub import AudioSegment
import cv2
from time import sleep, time

if __name__ == '__main__':
    ip_address = "127.0.0.1"
    rtmp_url = 'your_rtmp_url'
    port = 7777
    image_file = "/Users/a58/Code/python/rtp/images/frame_0.png"
    image_files = ["/Users/a58/Code/python/rtp/images/frame_%d.png" % i for i in range(5)]
    audio_file = "/Users/a58/Code/python/rtp/audios/bgroup.wav"
    audio_16k_file = "/Users/a58/Code/python/rtp/audios/bgroup16k.wav"
    audio_48k_file = "/Users/a58/Code/python/rtp/audios/bgroup48k.wav"

    resolution = (1080, 1920) # (width, height)

    rtpSender = RTPSender(ip_address, port, resolution, hard_encode=False, open_log=True, days=7)
    rtpSender.stop()
    
    rtpSender = RTPSender(ip_address, port, resolution, hard_encode=False, open_log=True, days=7)

    rtmpSender = RTMPSender(ip_address, port, resolution, rtmp_url=rtmp_url, hard_encode=True, open_log=True, days=7, stdout=False, bit_rate=600000)

    audio = AudioSegment.from_file(audio_48k_file, format="wav")
    audio_data = audio.raw_data
    i = 0
    cnt = 0
    t1 = time()

    init_cnt = 2

    imgs = [cv2.imread(image_file) for image_file in image_files]

    is_16k = False
    frame_size = 640 if is_16k else 1920

    frame_cnt = 0

    while True:
        for img in imgs:
            if i >= len(audio_data) - frame_size:
                i = 0
            for j in range(25):
                rtpSender.send_video_rtp_from_img(img)
                rtmpSender.send_video_rtmp_from_img(img)
                frame_cnt += 1
                rtpSender.send_audio_rtp_from_bytes(audio_data[i:i+frame_size], True)
                rtmpSender.send_audio_rtmp_from_bytes(audio_data[i:i+frame_size], is_16k=is_16k)
                i += frame_size
                rtpSender.send_audio_rtp_from_bytes(audio_data[i:i+frame_size], True)
                rtmpSender.send_audio_rtmp_from_bytes(audio_data[i:i+frame_size], is_16k=is_16k)
                cnt += 1
                i += frame_size
                t2 = time()
                t = t1 + cnt*0.04 - t2
                if t > 0:
                    sleep(t)
        if init_cnt < 20:
            rtpSender.stop()
            rtpSender = RTPSender(ip_address, port, resolution, hard_encode=False, open_log=True, days=7)
            init_cnt += 1
            print("reinit rtpSender: ", init_cnt)
```

## StreamSender Releases
| Major Release Version | Release Date | Updates                   |
|-----------------|--------------|---------------------------|
| v0.0.1           | 2024-10-14   | 增加RTMPSender, 并调整目录结构|

## RTPSender Releases
| Major Release Version | Release Date | Updates                   |
|-----------------|--------------|---------------------------|
| v3.8.8          | 2024-09-14   | 在v3.8.6的基础上，增加平均耗时日志|
| v3.8.6          | 2024-09-14   | 增加编码和发送耗时日志|
| v3.8.4          | 2024-09-13   | 在v3.8.3的基础上，增加时间日志|
| v3.8.3          | 2024-09-11   | 在v3.8.0的基础上，暴露gop参数|
| v3.8.2          | 2024-09-06   | 删除测试代码              |
| v3.8.1          | 2024-09-06   | 引入多进程  |
| v3.8.0          | 2024-09-04   | 设置码率为600k  |
| v3.7.9          | 2024-08-29   | 添加控制台日志开关                 |
| v3.7.8          | 2024-08-29   | 使用loguru记录日志                 |
| v3.7.7          | 2024-08-29   | Bug fixes            |
| v3.7.5          | 2024-08-29   | 添加滚动日志，保存日志到文件                 |
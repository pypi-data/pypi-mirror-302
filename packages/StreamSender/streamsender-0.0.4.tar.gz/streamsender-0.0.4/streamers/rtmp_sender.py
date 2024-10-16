import struct
import librtmp
import av
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
import ctypes
from time import time
from loguru import logger
from datetime import timedelta
import numpy as np
import io
import soundfile as sf
import librosa

class RTMPSender:
    def __init__(self, ip_address, port, frame_size, rtmp_url, sample_rate, my_logger=None, gop=25, hard_encode=False, open_log=False, days=7, stdout=False, log_dir='./rtmp_logs/', bit_rate=600000):
        self.image_queue2 = queue.Queue()
        self.audio_queue2 = queue.Queue()
        self.image_file = ""
        self.audio_file = ""
        self.ip_address = ip_address
        self.port = port
        self.output_path = 'output.mp4'
        self.hard_encode = hard_encode
        self.open_log = open_log
        self.gop = gop
        self.logger = my_logger
        self.rtmp_url = rtmp_url
        self.original_sample_rate = sample_rate

        # 默认video img RTMP header参数
        self.RTMP_VIDEO_IMG_TIMESTAMP = 0
        # 默认音频bytes RTMP header 参数
        self.RTMP_AUDIO_BYTES_TIMESTAMP = 0

        self.img_rtmp_sent_total_time = 0
        self.img_rtmp_sent_total_cnt = 0
        self.img_encode_total_time = 0
        self.img_encode_total_cnt = 0
        self.audio_rtmp_sent_total_time = 0
        self.audio_rtmp_sent_total_cnt = 0
        self.audio_encode_total_time = 0
        self.audio_encode_total_cnt = 0

        # 初始化输出容器
        self.output_container = av.open(self.output_path, mode='w')

        if self.logger is None:
            if not stdout:
                logger.remove() # 移除默认的日志记录器：控制台打印
            logger.add(
                log_dir + "rtmp_sender.{time:YYYY-MM-DD_HH}.log", 
                rotation="1 hour",  # 每小时创建一个新日志文件
                retention=timedelta(days=days),  # 保留最近days天的日志，默认为7天
                compression=None,  # 不压缩日志文件
                format="{time:YYYY-MM-DD at HH:mm:ss.SSS} | {level} | {message}"
            )
            self.logger = logger

        # 音频编码器
        self.target_sample_rate = 48000
        self.audio_stream = self.output_container.add_stream('aac', rate=self.target_sample_rate)
        self.audio_stream.channels = 1
        self.audio_stream.layout = 'mono'  # 声道布局为单声道
        self.audio_stream.format = 'fltp'  # AAC 格式通常使用浮点数据
        # self.audio_stream.bit_rate = 256000

        # 创建视频流
        if self.hard_encode:
            if self.open_log:
                self.logger.info("Using hard encoding...")
            # 视频编码器
            self.video_stream = self.output_container.add_stream('h264_nvenc', rate=25)
            self.video_stream.options = {
                'bf': '0',       # 禁用B帧
                'delay': '0',     # 设置delay为0
                'g': str(self.gop)   # 设置gop大小为25帧
            }
            self.video_stream.pix_fmt = 'yuv420p'
        else:
            if self.open_log:
                self.logger.info("Using soft encoding...")
            self.video_stream = self.output_container.add_stream('libx264', rate=25)
            self.video_stream.options = {'g': str(self.gop), 'tune': 'zerolatency'}  # 设置GOP大小为25帧，实现低延迟

        self.video_stream.bit_rate = bit_rate

        if self.open_log:
            self.logger.info(f"Video stream bit rate: {self.video_stream.bit_rate} bps")
        
        if self.open_log:
            self.logger.info(f"Video stream options: {self.video_stream.options}")

        self.video_stream.width = frame_size[0]
        self.video_stream.height = frame_size[1]

        self.rtmp_stream = self.create_stream()
        self.write_flv_header()

        self.stop_event = threading.Event()

        self.video_thread2 = threading.Thread(target=self.process_video_queue2)
        self.audio_thread2 = threading.Thread(target=self.process_audio_queue2)

        self.video_thread2.start()
        self.audio_thread2.start()

    def stop(self):
        def stop_threads():
            self.stop_event.set()
            self.video_thread2.join()
            self.audio_thread2.join()
            if self.open_log:
                self.logger.info("All threads have been successfully stopped.")

            self.output_container.close()
            if self.open_log:
                self.logger.info("Output container successfully closed.")

        if self.open_log:
            self.logger.info("Stopping all active threads...")

        executor = ThreadPoolExecutor(max_workers=1)
        executor.submit(stop_threads)
        executor.shutdown(wait=False)

    def create_stream(self):
        connection = librtmp.RTMP(self.rtmp_url, live=True)

        self.logger.info("Connecting to RTMP server...")
        if not connection.connect():
            self.logger.error("RTMP connection failed.")
            exit(1)
        else:
            self.logger.info("RTMP connection established successfully.")

        self.logger.info("Creating RTMP stream...")
        stream = connection.create_stream(writeable=True)
        if not stream:
            self.logger.error("Stream creation failed.")
            exit(1)
        else:
            self.logger.info("Stream creation successful.")
        
        return stream
    
    def write_flv_header(self):
        flv_header = b'FLV\x01\x05\x00\x00\x00\x09'  # FLV version 1, contains both audio and video
        self.rtmp_stream.write(flv_header)
    
    def create_flv_video_tag(self, video_data, is_keyframe=False):
        tag_type = 0x09  # 0x09 for video
        data_size = len(video_data) + 5
        stream_id = 0  # Always 0 for StreamID
        
        # Frame Type (4 bits) + CodecID (4 bits)
        frame_type = 1 if is_keyframe else 2  # 1 for keyframe, 2 for interframe
        codec_id = 7  # 7 for AVC (H.264)
        video_frame_header = struct.pack('>B', (frame_type << 4) | codec_id)  # First byte

        # AVC Packet Type (1 byte), 0 = AVC sequence header, 1 = NALU
        avc_packet_type = 1  # 1 for NALU (actual video frame)
        
        # Composition Time (3 bytes)
        composition_time = struct.pack('>I', 0)[1:]

        # FLV Tag Header (11 bytes)
        tag_header = struct.pack(
            '>B3s3sB3s',
            tag_type,  # 1 byte - Tag Type (0x09 for video)
            struct.pack('>I', data_size)[1:],  # 3 bytes - Data Size
            struct.pack('>I', self.RTMP_VIDEO_IMG_TIMESTAMP)[1:],  # 3 bytes - Timestamp
            (self.RTMP_VIDEO_IMG_TIMESTAMP >> 24) & 0xFF,  # 1 byte - Timestamp Extended
            struct.pack('>I', stream_id)[1:],  # 3 bytes - StreamID
        )

        flv_tag = tag_header + video_frame_header + struct.pack('>B', avc_packet_type) + composition_time + video_data

        return flv_tag
    
    def resample_audio_bytes(self, input_bytes, original_rate=16000, target_rate=48000):
        # 将字节数据转换为 numpy 数组（假设 input_bytes 是 PCM s16le 格式）
        pcm_data = np.frombuffer(input_bytes, dtype=np.int16)
        
        # PCM 数据是单声道
        pcm_data = pcm_data.astype(np.float32) / 32768.0  # 将数据归一化到[-1, 1]

        # 重新采样
        resampled_data = librosa.resample(pcm_data, orig_sr=original_rate, target_sr=target_rate)

        # 将重新采样后的数据还原到 PCM s16le 格式
        resampled_data = (resampled_data * 32768.0).astype(np.int16)
        
        # 转换为字节流
        output_buffer = io.BytesIO()
        sf.write(output_buffer, resampled_data, samplerate=target_rate, subtype='PCM_16', format='RAW')

        return output_buffer.getvalue()
    
    def create_flv_audio_tag(self, audio_data, is_sequence_header=False):
        # 设定参数
        audio_format = 10  # AAC
        sound_rate = 3  # 44.1kHz
        sound_size = 1  # 16-bit
        sound_type = 0  # Mono
        stream_id = 0

        data_length = len(audio_data)

        # Tag Header
        tag_type = 8  # Audio
        tag_data_size = data_length + 2  # 加上参数字节
        
        tag_header = struct.pack(
            '>B3s3sB3s',
            tag_type,  # 1 byte - Tag Type (0x09 for video)
            struct.pack('>I', tag_data_size)[1:],  # 3 bytes - Data Size
            struct.pack('>I', self.RTMP_AUDIO_BYTES_TIMESTAMP)[1:],  # 3 bytes - Timestamp
            (self.RTMP_AUDIO_BYTES_TIMESTAMP >> 24) & 0xFF,  # 1 byte - Timestamp Extended
            struct.pack('>I', stream_id)[1:],  # 3 bytes - StreamID
        )

        # 构建音频数据，第一个字节是音频数据的参数
        audio_header = (audio_format << 4) | (sound_rate << 2) | (sound_size << 1) | sound_type
        aac_packet_type = 0 if is_sequence_header else 1
        audio_data_with_header = bytes([audio_header, aac_packet_type]) + audio_data

        return tag_header + audio_data_with_header

    def send_video_rtmp_from_img(self, img):
        self.image_queue2.put(img)

    def process_video_queue2(self):
        if self.open_log:
            self.logger.info("Started processing video queue from image stream.")

        while not self.stop_event.is_set():
            try:
                img = self.image_queue2.get(block=True, timeout=5)
                if self.open_log:
                    self.logger.info(f"Current size of image_queue2: {self.image_queue2.qsize()}.")
            except queue.Empty:
                continue

            encode_begin = time()
            img_frame = av.VideoFrame.from_ndarray(img, format = 'rgb24')
            packets = self.video_stream.encode(img_frame)
            encode_end = time()
            cur_encode_cost_time = (encode_end - encode_begin) * 1000
            self.img_encode_total_time += cur_encode_cost_time
            self.img_encode_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Image encoding #{self.img_encode_total_cnt}: {cur_encode_cost_time:.6f} ms")
                avg_time = self.img_encode_total_time / self.img_encode_total_cnt
                self.logger.info(f"Average image encode time: {avg_time:.6f} ms over {self.img_encode_total_cnt} encodes.")

            send_begin = time()

            data = self.video_stream.codec_context.extradata

            for packet in packets:
                buffer_ptr = packet.buffer_ptr
                buffer_size = packet.buffer_size
                buffer = (ctypes.c_char * buffer_size).from_address(buffer_ptr)

                buffer_bytes = bytes(buffer)

                is_keyframe = False

                begin = b'\x00\x00\x01\x06'
                end = b'\x00\x00\x00\x01\x65'
                p = b'\x00\x00\x00\x01\x61'
                
                if self.hard_encode:
                    if buffer_bytes.find(begin) != -1:
                        is_keyframe = True
                        pos = buffer_bytes.find(end)
                        if pos != -1:
                            buffer = data + buffer[pos:]
                        else:
                            pos2 = buffer_bytes.find(p)
                            if pos2 != -1:
                                buffer = buffer[pos2:]
                    elif buffer_bytes.startswith(end):
                        buffer = data + buffer
                else:
                    if buffer_bytes.startswith(begin):
                        pos = buffer_bytes.find(end)
                        if pos != -1:
                            buffer = data + buffer[pos:]
                    elif buffer_bytes.startswith(end):
                        buffer = data + buffer

                payload = buffer

                flv_video_tag = self.create_flv_video_tag(payload, is_keyframe)
                try:
                    self.rtmp_stream.write(flv_video_tag)
                except Exception as e:
                    self.logger.error(f"Failed to write video frame: {e}. Verify the RTMP URL is active and the FLV video tag format is correct.")
                    break
                self.logger.info("FLV video tag successfully sent.")
                
                self.RTMP_VIDEO_IMG_TIMESTAMP += 40
                
            send_end = time()
            cur_img_send_cost_time = (send_end - send_begin) * 1000
            self.img_rtmp_sent_total_time += cur_img_send_cost_time
            self.img_rtmp_sent_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Image RTMP send #{self.img_rtmp_sent_total_cnt}: {cur_img_send_cost_time:.6f} ms")
                avg_time = self.img_rtmp_sent_total_time / self.img_rtmp_sent_total_cnt
                self.logger.info(f"Average image RTMP send time: {avg_time:.6f} ms over {self.img_rtmp_sent_total_cnt} sends.")


    def send_audio_rtmp_from_bytes(self, audio_bytes, is_16k=False):
        self.audio_queue2.put((audio_bytes, is_16k))


    def process_audio_queue2(self):
        if self.open_log:
            self.logger.info("Started processing audio queue from byte stream.")

        sequence_header_sent = False

        while not self.stop_event.is_set():
            try:
                audio_data, _ = self.audio_queue2.get(block=True, timeout=5)
                if self.open_log:
                    self.logger.info(f"Current size of audio_queue2: {self.audio_queue2.qsize()}.")
            except queue.Empty:
                continue
            
            if self.original_sample_rate != self.target_sample_rate:
                resample_begin = time()
                audio_data = self.resample_audio_bytes(audio_data, original_rate=self.original_sample_rate, target_rate=self.target_sample_rate)
                resample_end = time()
                cur_resample_cost_time = (resample_end - resample_begin) * 1000
                if self.open_log:
                    self.logger.info(f"Audio resampling time: {cur_resample_cost_time:.6f} ms")

            encode_begin = time()
            pcm_array = np.frombuffer(audio_data, dtype=np.int16).reshape(1, -1)
            
            audio_frame = av.AudioFrame.from_ndarray(pcm_array, format="s16", layout='mono')
            audio_frame.sample_rate = self.target_sample_rate

            if not self.audio_stream.codec_context.is_open:
                self.audio_stream.codec_context.open()

            packets = self.audio_stream.encode(audio_frame)
            encode_end = time()
            cur_encode_cost_time = (encode_end - encode_begin) * 1000
            self.audio_encode_total_time += cur_encode_cost_time
            self.audio_encode_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Audio encoding #{self.audio_encode_total_cnt}: {cur_encode_cost_time:.6f} ms")
                avg_time = self.audio_encode_total_time / self.audio_encode_total_cnt
                self.logger.info(f"Average audio encode time: {avg_time:.6f} ms over {self.audio_encode_total_cnt} encodes.")

            data = self.audio_stream.codec_context.extradata

            audio_send_begin = time()

            for packet in packets:
                buffer_ptr = packet.buffer_ptr
                buffer_size = packet.buffer_size
                buffer = (ctypes.c_char * buffer_size).from_address(buffer_ptr)

                if not sequence_header_sent:
                    flv_audio_tag = self.create_flv_audio_tag(data, is_sequence_header=True)
                    self.rtmp_stream.write(flv_audio_tag)
                    self.logger.info("AAC sequence header successfully sent.")
                    sequence_header_sent = True

                payload = buffer

                flv_audio_tag = self.create_flv_audio_tag(payload, is_sequence_header=False)
                try:
                    self.rtmp_stream.write(flv_audio_tag)
                except Exception as e:
                    self.logger.error(f"Failed to write audio frame: {e}. Verify the RTMP URL is active and the FLV audio tag format is correct.")
                    break
                self.logger.info("FLV audio tag successfully sent.")
                
                self.RTMP_AUDIO_BYTES_TIMESTAMP += 20

            audio_send_end = time()
            cur_audio_send_cost_time = (audio_send_end - audio_send_begin) * 1000
            self.audio_rtmp_sent_total_time += cur_audio_send_cost_time
            self.audio_rtmp_sent_total_cnt += 1
            if self.open_log:
                self.logger.info(f"Audio RTMP send #{self.audio_rtmp_sent_total_cnt}: {cur_audio_send_cost_time:.6f} ms")
                avg_time = self.audio_rtmp_sent_total_time / self.audio_rtmp_sent_total_cnt
                self.logger.info(f"Average audio RTMP send time: {avg_time:.6f} ms over {self.audio_rtmp_sent_total_cnt} sends.")
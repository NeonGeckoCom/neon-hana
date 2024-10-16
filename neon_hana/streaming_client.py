import io
from asyncio import run
from base64 import b64encode, b64decode
from typing import Optional, Callable
from mock.mock import Mock
from threading import Thread
from queue import Queue

from ovos_dinkum_listener.voice_loop import DinkumVoiceLoop
from ovos_dinkum_listener.voice_loop.hotwords import HotwordContainer
from ovos_dinkum_listener.voice_loop.voice_loop import ChunkInfo
from ovos_plugin_manager.templates.microphone import Microphone
from ovos_plugin_manager.vad import OVOSVADFactory
from ovos_utils.fakebus import FakeBus
from speech_recognition import AudioData
from ovos_utils import LOG
from starlette.websockets import WebSocket


class StreamMicrophone(Microphone):
    def __init__(self, queue: Queue):
        self.queue = queue

    def start(self):
        pass

    def stop(self):
        self.queue.put(None)

    def read_chunk(self) -> Optional[bytes]:
        return self.queue.get()


class RemoteStreamHandler(Thread):
    def __init__(self, mic: StreamMicrophone, session_id: str,
                 input_audio_callback: Callable,
                 client_socket: WebSocket,
                 ww_callback: Callable, lang: str = "en-us"):
        Thread.__init__(self)
        self.session_id = session_id
        self.ww_callback = ww_callback
        self.input_audio_callback = input_audio_callback
        self.client_socket = client_socket
        self.bus = FakeBus()
        self.mic = mic
        self.lang = lang
        self.hotwords = HotwordContainer(self.bus)
        self.hotwords.load_hotword_engines()
        self.vad = OVOSVADFactory.create()
        self.voice_loop = DinkumVoiceLoop(mic=self.mic,
                                          vad=self.vad,
                                          hotwords=self.hotwords,
                                          listenword_audio_callback=self.on_hotword,
                                          hotword_audio_callback=self.on_hotword,
                                          stopword_audio_callback=self.on_hotword,
                                          wakeupword_audio_callback=self.on_hotword,
                                          stt_audio_callback=self.on_input_audio,
                                          stt=Mock(transcribe=Mock(return_value=[])),
                                          fallback_stt=Mock(transcribe=Mock(return_value=[])),
                                          transformers=MockTransformers(),
                                          chunk_callback=self.on_chunk,
                                          speech_seconds=0.5,
                                          num_hotword_keep_chunks=0,
                                          num_stt_rewind_chunks=0)

    def run(self):
        self.voice_loop.start()
        self.voice_loop.run()

    def on_hotword(self, audio_bytes: bytes, context: dict):
        self.lang = context.get("stt_lang") or self.lang
        LOG.info(f"Hotword: {context}")
        self.ww_callback(context, self.session_id)

    def on_input_audio(self, audio_bytes: bytes, context: dict):
        LOG.info(f"Audio: {context}")
        audio_data = AudioData(audio_bytes, self.mic.sample_rate,
                               self.mic.sample_width).get_wav_data()
        audio_data = b64encode(audio_data).decode("utf-8")
        callback_data = {"type": "neon.audio_input",
                         "data": {"audio_data": audio_data, "lang": self.lang}}
        self.input_audio_callback(callback_data, self.session_id)

    def on_response_audio(self, data: dict):
        async def _send_bytes(audio_bytes: bytes):
            await self.client_socket.send_bytes(audio_bytes)

        i = 0
        for lang_response in data.get('responses', {}).values():
            for encoded_audio in lang_response.get('audio', {}).values():
                i += 1
                wav_audio_bytes = b64decode(encoded_audio)
                LOG.info(f"Sending {len(wav_audio_bytes)} bytes of audio")
                run(_send_bytes(wav_audio_bytes))
        LOG.info(f"Sent {i} binary audio response(s)")

    def on_chunk(self, chunk: ChunkInfo):
        LOG.debug(f"Chunk: {chunk}")

    def shutdown(self):
        self.mic.stop()
        self.voice_loop.stop()


class MockTransformers(Mock):
    def transform(self, chunk):
        return chunk, dict()

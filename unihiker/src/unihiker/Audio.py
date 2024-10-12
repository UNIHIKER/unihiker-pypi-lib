import time
import platform

if platform.system().lower().startswith('win') or platform.system().lower().startswith('lin'):
    import pyaudio
# elif platform.system().lower().startswith('lin'):
#     import pyaudio

from pydub import AudioSegment  
from math import ceil

#Mute alsa
import ctypes

ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                      ctypes.c_char_p, ctypes.c_int,
                                      ctypes.c_char_p)

def py_error_handler(filename, line, function, err, fmt):
    pass

c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

try:
    asound = ctypes.cdll.LoadLibrary('libasound.so.2')
    asound.snd_lib_error_set_handler(c_error_handler)
except OSError:
    pass
#End mute alsa

class Audio():
    if platform.system().lower().startswith('win') or platform.system().lower().startswith('lin'):
        def __init__(self, rate=16000, chunk=8192, format=pyaudio.paInt16):
            self.rate = rate
            self.chunk = chunk
            self.format = format
            self.channels = 1
            self.frame = None
            self.frames = []
            self.stream = None
            self.duration = None
            self.recording = False
            self.target_volume = -20
            self.sound = None
            self.player = None

            self.play_sound = None
            self.play_rate = None
            self.play_chunk = 2048
            self.play_format = None
            self.play_channels = 1
            self.play_frames = []
            self.play_file = None
            self.p = pyaudio.PyAudio()
            # if platform.system().lower().startswith('win'):
            #     self.p = pyaudio.PyAudio()
            # elif platform.system().lower().startswith('lin'):
            #     self.p = pyaudio.PyAudio()
            
            def callback(in_data, frame_count, time_info, status):
                if self.recording:
                    self.frames.append(in_data)
                    if self.duration is not None and len(self.frames) >= int(self.rate / self.chunk * self.duration):
                        self.recording = False
                self.frame = in_data
                return (in_data, pyaudio.paContinue)
                # if platform.system().lower().startswith('win'):
                #     return (in_data, pyaudio.paContinue)
                # elif platform.system().lower().startswith('lin'):
                #     return (in_data, pyaudio.paContinue)

            self.stream = self.p.open(format=self.format,
                            channels=self.channels,
                            rate=self.rate,
                            input=True,
                            frames_per_buffer=self.chunk,
                            stream_callback = callback)

        def auto_volume(self, sound, target_dBFS):
            change_in_dBFS = target_dBFS - sound.dBFS
            return sound.apply_gain(change_in_dBFS)

        def start_record(self, file, target_volume=-20):
            self.recording = False
            self.file = file
            self.frames = []
            self.duration = None
            self.recording = True
            self.target_volume = target_volume
        
        def stop_record(self):
            self.recording = False
            self.sound = AudioSegment(b''.join(self.frames), sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate)
            # if platform.system().lower().startswith('win'):
            #     self.sound = AudioSegment(b''.join(self.frames), sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate)
            # elif platform.system().lower().startswith('lin'):\
            #     self.sound = AudioSegment(b''.join(self.frames), sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate)
            if self.target_volume is not None:
                self.sound = self.auto_volume(self.sound, self.target_volume) 
            self.sound.export(self.file, format='wav')

        def record(self, file, duration, target_volume=-20):
            self.file = file
            self.recording = False
            self.frames = []
            self.duration = duration
            self.recording = True
            self.target_volume = target_volume
            while self.recording:
                time.sleep(0.001)
            self.stop_record()
            self.sound.export(self.file, format='wav')

        def sound_level(self):
            def mapping( x,  in_min,  in_max,  out_min,  out_max):
                result = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
                result = max(min(result, 100), 0)
                return result

            return round( mapping(self.sound_dBFS(), -50, -20, 0, 100), 2)

        def sound_dBFS(self):
            if self.frame is None:
                return -96.00
            else:
                return AudioSegment(self.frame, sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate).dBFS
                # if platform.system().lower().startswith('win'):
                #     return AudioSegment(self.frame, sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate).dBFS
                # elif platform.system().lower().startswith('lin'):
                #     return AudioSegment(self.frame, sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate).dBFS
            
            

        def play(self, file):
            self.start_play(file)
            while self.player.is_active():
                time.sleep(0.001)
            self.stop_play()

        def start_play(self, file):
            def callback(in_data, frame_count, time_info, status):
                if not self.play_frames:
                    return (b'', pyaudio.paComplete)
                    # if platform.system().lower().startswith('win'):
                    #     return (b'', pyaudio.paComplete)
                    # elif platform.system().lower().startswith('lin'):
                    #     return (b'', pyaudio.paComplete)
                data = self.play_frames.pop(0)
                return (data, pyaudio.paContinue)
                # if platform.system().lower().startswith('win'):
                #     return (data, pyaudio.paContinue)
                # elif platform.system().lower().startswith('win'):
                #     return (data, pyaudio.paContinue)

            self.play_sound = AudioSegment.from_file(file)

            if self.play_sound.channels == 1:
                self.play_sound = self.play_sound.set_channels(2)

            chunk_size = self.play_chunk * self.play_sound.sample_width * self.play_sound.channels

            number_of_chunks = ceil(len(self.play_sound.raw_data) / float(chunk_size))
            self.play_frames = [self.play_sound.raw_data[i * chunk_size:(i + 1) * chunk_size] for i in range(int(number_of_chunks))]

            self.player = self.p.open(format = self.p.get_format_from_width(self.play_sound.sample_width), 
                channels = self.play_sound.channels, 
                rate = self.play_sound.frame_rate,
                output = True,
                frames_per_buffer=self.play_chunk,
                stream_callback = callback)
        
            self.player.start_stream()
        
        def stop_play(self):
            self.player.stop_stream()
            self.play_frames = []
            self.player.close()

        def pause_play(self):
            self.player.stop_stream()

        def resume_play(self):
            self.player.start_stream()
        
        def play_time_remain(self):
            return round(len(self.play_frames)*self.play_chunk/self.play_sound.frame_rate, 2)
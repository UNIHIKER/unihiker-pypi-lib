import time
import platform
import os
# Set the environment variable before importing pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
if platform.system().lower().startswith('win') or platform.system().lower().startswith('lin'):
    import pyaudio

from pydub import AudioSegment  
from math import ceil

# Mute alsa
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
# End mute alsa



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

            self.p = pyaudio.PyAudio()

            pygame.mixer.init()
            self.audio = None
            self.channel = None
            self.start_time = None
            self.paused_time = None  
            self.is_paused = False  


            def callback(in_data, frame_count, time_info, status):
                if self.recording:
                    self.frames.append(in_data)
                    if self.duration is not None and len(self.frames) >= int(self.rate / self.chunk * self.duration):
                        self.recording = False
                self.frame = in_data
                return (in_data, pyaudio.paContinue)

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
            file_path = '/opt/unihiker/Version'
            if os.path.exists(file_path):
                try:
            
                    with open(file_path, 'r') as file:
                        content = file.read()
                    if 'box' in content:
                        return round( mapping(self.sound_dBFS(), -17, -5, 0, 100), 2) 
                    else:
                        return round( mapping(self.sound_dBFS(), -50, -20, 0, 100), 2) 
                except Exception as e:
                    print(f"An error occurred while reading the file: {e}")
            else:
                return round( mapping(self.sound_dBFS(), -50, -20, 0, 100), 2) 
            

        def sound_dBFS(self):
            if self.frame is None:
                return -96.00
            else:
                return AudioSegment(self.frame, sample_width=self.p.get_sample_size(pyaudio.paInt16), channels=self.channels, frame_rate=self.rate).dBFS
            
            
        def play(self, file_path):
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            self.start_time = time.time()
            while pygame.mixer.music.get_busy():  
                pygame.time.Clock().tick(10)  

        def start_play(self, file_path):
            self.audio = pygame.mixer.Sound(file_path)
            self.channel = self.audio.play()
            self.start_time = time.time()  

        def pause_play(self):
            if self.channel and not self.is_paused: 
                self.paused_time = time.time() - self.start_time
                self.channel.pause()
                self.is_paused = True  

        def resume_play(self):
            if self.channel and self.is_paused: 
                self.start_time = time.time() - self.paused_time
                self.paused_time = None
                self.channel.unpause()
                self.is_paused = False  

        def play_time_remain(self):
            if self.is_paused:
                return round(max(0, self.audio.get_length() - self.paused_time), 2)
            elif self.channel and self.channel.get_busy():
                elapsed_time = time.time() - self.start_time
                return round(max(0, self.audio.get_length() - elapsed_time), 2)
            return 0

        def stop_play(self):
            
            if self.channel:
                self.channel.stop()
                self.start_time = None  
                self.paused_time = None 

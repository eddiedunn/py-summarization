import os
#from IPython.display import Audio
import nltk  # we'll use this to split into sentences
import numpy as np
import pyaudio
import wave
from bark.generation import (
    generate_text_semantic,
    preload_models,
)
from bark.api import semantic_to_waveform
from bark import generate_audio, SAMPLE_RATE
from scipy.io.wavfile import write as write_wav
from audio_playback import AudioPlayback

class FileSpeaker:
    def __init__(self, filename):
        self.filename = filename
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        self.temp_dir = '/tmp'


    def speak(self):
        with open(self.filename, 'r') as f:
           script = f.read().replace("\n", " ").replace("-","").strip()
        sentences = nltk.sent_tokenize(script)
        GEN_TEMP = 0.6
        SPEAKER = "v2/en_speaker_6"
        silence = np.zeros(int(0.125 * SAMPLE_RATE))  # quarter second of silence

        pieces = []
        for sentence in sentences:
            semantic_tokens = generate_text_semantic(
                sentence,
                history_prompt=SPEAKER,
                temp=GEN_TEMP,
                min_eos_p=0.05,  # this controls how likely the generation is to end
            )

            audio_array = semantic_to_waveform(semantic_tokens, history_prompt=SPEAKER,)
            pieces += [audio_array, silence.copy()]
            file_to_play = np.concatenate(pieces)
            wave_file_location = self.temp_dir+"/test.wav"
            write_wav(wave_file_location, SAMPLE_RATE, file_to_play)
            
        ap = AudioPlayback()  
        ap.play_audio(wave_file_location)



import soundfile as sf
import sounddevice as sd

class AudioPlayback:
    def __init__(self):
        pass

    def play_audio(self, sound_file_path):
        data, samplerate = sf.read(sound_file_path)

        print("Playing audio...")
        sd.play(data, samplerate)
        sd.wait()  # Wait until file is done playing
        print("Finished playing audio.")

def main():
    ap = AudioPlayback()
    ap.play_audio("/tmp/test.wav")

if __name__ == "__main__":
    main()


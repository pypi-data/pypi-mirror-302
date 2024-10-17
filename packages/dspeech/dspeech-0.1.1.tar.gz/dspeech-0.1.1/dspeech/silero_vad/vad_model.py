from silero_vad_nuaazs import SileroVAD
import torchaudio

# TODO 还有BUG，可能要优化silero_vad_nuaazs包
class VAD:
    def __init__(self):
        self.model = SileroVAD()
    def generate(input):
        # if input is a tuple
        if isinstance(input, tuple) and len(input) == 2:
            audio_data = input[0]
            sr = input[1]
            # save audio data to a temporary audio file
            audio_file = "temp.wav"
            torchaudio.save(audio_file, audio_data, sr)
            vad_segments = self.model.get_speech_timestamps(input)
            return vad_segments
        if isinstance(input, str) and os.path.exists(input):
            vad_segments = self.model.get_speech_timestamps(input)
            return vad_segments
        else:
            raise ValueError("Input should be a valid file path")
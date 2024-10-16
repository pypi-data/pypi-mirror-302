import os
import logging
import numpy as np
from funasr import AutoModel
from time import perf_counter
from rich.console import Console
console = Console()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class TTS():
    def __init__(
        self,
        model_name="F5-TTS", #"paraformer-zh",
        device="cuda",
        target_sample_rate=24000,
    ):
        console.print(f"[green] Model Name: {model_name}")
        console.print(f"[green] Device: {device}")
       
        try:
            self.DSPEECH_HOME = os.environ["DSPEECH_HOME"]
        except KeyError:
            console.print("[red]Please set DSPEECH_HOME in your environment variables.")
            console.print("[red]export DSPEECH_HOME=/path/to/dspeech")
        if model_name == "F5-TTS":
            from dspeech.f5tts import F5
            self.model = F5(device=device,target_sample_rate=target_sample_rate)
        
    def _load_file(self, file_path, start=0, end=-1, sample_rate=16000, channel=0):
        """Extracts audio from file_path based on start, end, and sample_rate.

        Args:
            file_path (str): file path to the audio file
            start (float): start time in seconds, default 0
            end (float): end time in seconds, default -1 (end of file)
            sample_rate (int): sample rate of the audio
            channel (int): channel of the audio file, default 0 (-1 for all channels)
        """
        audio, sr = torchaudio.load(file_path)
        if sr != sample_rate:
            # resample by torchaudio
            transform = torchaudio.transforms.Resample(orig_freq=sr, new_freq=sample_rate)
            audio = transform(audio)
            sr = sample_rate
            console.print(f"[yellow]Resampled audio to {sample_rate} Hz")
        
        if channel != -1:
            audio = audio[channel, :]
        else:
            # merge all channels to mono, by taking mean
            audio = audio.mean(dim=0)
        audio = audio.reshape(-1)
        logger.debug(f"Loaded audio with shape {audio.shape} and sample rate {sr}")
        logger.debug(f"start: {start}, end: {end}")
        logger.debug(f"audio length: {len(audio)/sr}")
        if end == -1:
            end = len(audio) / sr
            console.print(f"[yellow]End time not provided, setting end to {end}")
        start = int(start * sr)
        end = int(end * sr)
        audio = audio[start:end]
        console.print(f"[green]Start: {start}, End: {end}")
        console.print(f"[green]Loaded audio with shape {audio.shape} and sample rate {sample_rate}")
        return audio

    def warmup(self):
        pass

    def get_speaker_info(self, folder_path):
        return self.model.get_speaker_info(folder_path)

    def clone_with_emo(
        self,
        gen_text_batches,
        speaker_info,
        speed=1.0,
        channel=-1,
        remove_silence=True,
        fix_durations=[],
        wave_path=None,
        spectrogram_path=None,
        concat=True,
    ):
        return self.model.clone_with_emo(
            gen_text_batches,
            speaker_info,
            speed=speed,
            channel=channel,
            remove_silence=remove_silence,
            fix_durations=fix_durations,
            wave_path=wave_path,
            spectrogram_path=spectrogram_path,
            concat=concat,
        )

    def clone(self, ref_audio, ref_text, gen_text_batches,
                speed=1.0, channel=-1,
                remove_silence=True,
                fix_durations=[], wave_path=None,
                spectrogram_path=None,
                concat=True,
                ):
        r = self.model.clone(ref_audio, ref_text, gen_text_batches,
                speed=speed, channel=channel,
                remove_silence=remove_silence,
                fix_durations=fix_durations,
                wave_path=wave_path,
                spectrogram_path=spectrogram_path,
                concat=concat,
                )
        return r

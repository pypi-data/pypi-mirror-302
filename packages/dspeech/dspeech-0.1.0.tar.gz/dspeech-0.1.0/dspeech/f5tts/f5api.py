import os
import codecs
import re
import tempfile
from pathlib import Path

import numpy as np
import soundfile as sf
import tomli
import torch
import torchaudio
import tqdm

from cached_path import cached_path
from einops import rearrange
from pydub import AudioSegment, silence
from transformers import pipeline
from vocos import Vocos
# 
from dspeech.f5tts.model import CFM, DiT, MMDiT, UNetT
from dspeech.f5tts.model.utils import (convert_char_to_pinyin, get_tokenizer,
                         load_checkpoint, save_spectrogram)

import logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
# set format
SPLIT_WORDS = [
    "but", "however", "nevertheless", "yet", "still",
    "therefore", "thus", "hence", "consequently",
    "moreover", "furthermore", "additionally",
    "meanwhile", "alternatively", "otherwise",
    "namely", "specifically", "for example", "such as",
    "in fact", "indeed", "notably",
    "in contrast", "on the other hand", "conversely",
    "in conclusion", "to summarize", "finally"
]

class F5():
    def __init__(self,
            device,
            model="F5-TTS",
            vocos_local_path=None,
            model_path=None,
            target_sample_rate = 24000,
            n_mel_channels = 100,
            hop_length = 256,
            target_rms = 0.1,
            nfe_step = 32,  # 16, 32
            cfg_strength = 2.0,
            ode_method = "euler",
            sway_sampling_coef = -1.0,
            ):
        self.model = model
        self.device = device
        # self.model_path = model_path
        self.target_sample_rate = target_sample_rate
        self.n_mel_channels = n_mel_channels
        self.hop_length = hop_length
        self.target_rms = target_rms
        self.nfe_step = nfe_step
        self.cfg_strength = cfg_strength
        self.ode_method = ode_method
        self.sway_sampling_coef = sway_sampling_coef
        if self.model == "F5-TTS":
            self.model_cls=DiT
            self.exp_name="F5TTS_Base"
            self.repo_name="F5TTS"
            self.ckpt_step=1200000
            self.model_cfg=dict(
                    dim=1024, depth=22, heads=16,
                    ff_mult=2, text_dim=512, conv_layers=4
                )
            if model_path is None:
                # DSPEECH_HOME from env
                self.model_path = f"{os.getenv('DSPEECH_HOME')}/f5_tts/{self.exp_name}/model_{self.ckpt_step}.safetensors"
            else:
                self.model_path = model_path
            if vocos_local_path is None:
                self.vocos = Vocos.from_pretrained("charactr/vocos-mel-24khz")
            else:
                self.vocos = Vocos.from_pretrained(vocos_local_path)

        elif self.model == "E2-TTS":
            self.model_cls=UNetT
            self.exp_name="E2TTS_Base"
            self.ckpt_step=1200000
            self.repo_name="E2TTS"
            self.model_cfg=dict(dim=1024, depth=24,
                    heads=16, ff_mult=4)
            if model_path is None:
                # DSPEECH_HOME from env
                self.model_path = f"{os.getenv('DSPEECH_HOME')}/f5_tts/{self.exp_name}/model_{self.ckpt_step}.safetensors"
            else:
                self.model_path = model_path
        else:
            raise ValueError(f"Model {model} not supported, only F5-TTS and E2-TTS are supported")
        self.model = self._load_model()

    def _load_model(self):
        ckpt_path = self.model_path
        model_cfg = self.model_cfg
        ckpt_step = self.ckpt_step
        exp_name = self.exp_name
        repo_name = self.repo_name
        device = self.device
        if not Path(ckpt_path).exists():
            # TODO: save to DSPEECH_HOME
            logger.error(f"Model checkpoint not found at {ckpt_path}")
            ckpt_path = str(cached_path(f"hf://SWivid/{repo_name}/{exp_name}/model_{ckpt_step}.safetensors"))
        vocab_char_map, vocab_size = get_tokenizer("Emilia_ZH_EN", "pinyin")
        model = CFM(
            transformer=self.model_cls(
                **model_cfg, text_num_embeds=vocab_size, mel_dim=self.n_mel_channels
            ),
            mel_spec_kwargs=dict(
                target_sample_rate=self.target_sample_rate,
                n_mel_channels=self.n_mel_channels,
                hop_length=self.hop_length,
            ),
            odeint_kwargs=dict(
                method=self.ode_method,
            ),
            vocab_char_map=vocab_char_map,
        ).to(device)

        model = load_checkpoint(model, ckpt_path, device, use_ema = True)
        return model

    def split_text_into_batches(self,text, max_chars=200, split_words=SPLIT_WORDS):
        if len(text.encode('utf-8')) <= max_chars:
            return [text]
        if text[-1] not in ['。', '.', '!', '！', '?', '？']:
            text += '.'
            
        sentences = re.split('([。.!?！？])', text)
        sentences = [''.join(i) for i in zip(sentences[0::2], sentences[1::2])]
        
        batches = []
        current_batch = ""
        
        def split_by_words(text):
            words = text.split()
            current_word_part = ""
            word_batches = []
            for word in words:
                if len(current_word_part.encode('utf-8')) + len(word.encode('utf-8')) + 1 <= max_chars:
                    current_word_part += word + ' '
                else:
                    if current_word_part:
                        # Try to find a suitable split word
                        for split_word in split_words:
                            split_index = current_word_part.rfind(' ' + split_word + ' ')
                            if split_index != -1:
                                word_batches.append(current_word_part[:split_index].strip())
                                current_word_part = current_word_part[split_index:].strip() + ' '
                                break
                        else:
                            # If no suitable split word found, just append the current part
                            word_batches.append(current_word_part.strip())
                            current_word_part = ""
                    current_word_part += word + ' '
            if current_word_part:
                word_batches.append(current_word_part.strip())
            return word_batches

    def get_speaker_info(self, folder_path):
        """ This function returns a dictionary of speaker id and emotion id to audio file path

        Args:
            folder_path (str): Path to the folder containing the audio files
        """
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Folder {folder_path} not found")

        speaker_info = {}
        for spkid in os.listdir(folder_path):
            # only wav, flac, mp3 files
            speaker_info[spkid] = {}
            for emoid in os.listdir(os.path.join(folder_path, spkid)):
                if emoid.endswith(('.wav', '.flac', '.mp3', '.m4a')):
                    emoid_filename = emoid
                    emoid = emoid.split('.')[0]
                    # assert txt file exist
                    if not os.path.exists(os.path.join(folder_path, spkid, emoid + '.txt')):
                        raise FileNotFoundError(f"Text file not found for {spkid}/{emoid}")
                    speaker_info[spkid][emoid.split('.')[0]] = {}
                    speaker_info[spkid][emoid.split('.')[0]]["path"] = os.path.join(folder_path, spkid, emoid_filename)
                    speaker_info[spkid][emoid.split('.')[0]]["text"] = open(os.path.join(folder_path, spkid, emoid + '.txt'), 'r', encoding='utf-8').read()
        return speaker_info

    def clone_with_emo(self, gen_text_batches, speaker_info,
                speed=1.0, channel=-1, remove_silence=True,
                fix_durations=[], wave_path=None, spectrogram_path=None,
                concat=True, #if False, wav_path needs to be a list of paths'
                ):
        ema_model = self.model
        all_emos = []
        all_speakers = []
        for spk in speaker_info:
            all_speakers.append(spk)
            for emo in speaker_info[spk]:
                assert isinstance(speaker_info[spk][emo]["path"], str), "speaker_info[spk][emo]['path'] should be a file path"
                assert isinstance(speaker_info[spk][emo]["text"], str), "speaker_info[spk][emo]['text'] should be a string"
                all_emos.append(f"{spk}_{emo}")
                ref_audio = torchaudio.load(speaker_info[spk][emo]["path"])
                ref_text = speaker_info[spk][emo]["text"]
        ref_texts = []
        ref_audio_for_texts = []
        generated_waves = []
        for i,_text in enumerate(gen_text_batches):
            # [[<spk_emo>]] should be in the text，e.g. [[spk1_emo1]]
            # use re to find it and select the speaker and emotion
            spk_emo = re.findall(r"\[\[(.*?)\]\]", _text)
            # spk_emo = spk_emo.replace("'", "").replace('[', "").replace(']', "")
            # if find multiple [[spk_emo]], only use the first one, and raise error if not found
            if not spk_emo:
                raise ValueError(f"Speaker and emotion not found in the text: {_text}")
            assert spk_emo, f"Speaker and emotion not found in the text: {_text}"
            spk, emo = spk_emo[0].split('_')
            assert spk in all_speakers, f"Speaker {spk} not found in the speaker_info"
            assert f"{spk}_{emo}" in all_emos, f"Emotion {spk}_{emo} not found in the speaker_info"
            _ref_audio = speaker_info[spk][emo]["path"]
            _ref_text = speaker_info[spk][emo]["text"]
            _text = _text.replace(f"[[{spk_emo[0]}]]", "")
            print(f"Now cloning for speaker （file: {_ref_audio}） with emotion:{spk_emo[0]}.")
            print(f"Reference text: {_ref_text}")
            print(f"Generated text: {_text}")
            
            ref_texts.append(_ref_text)
            ref_audio_for_texts.append(_ref_audio)
            wav_path = None if wave_path is None else wave_path
            if type(wave_path) == list:
                wav_path = wave_path[i]
            else:
                wav_path = None
            spectrogram_path = None if spectrogram_path is None else spectrogram_path
            if type(spectrogram_path) == list:
                spectrogram_path = spectrogram_path[i]
            else:
                spectrogram_path = None
            final_wave = self.clone(_ref_audio,
                                    _ref_text,
                                    [_text],
                                    speed=speed,
                                    channel=channel,
                                    remove_silence=remove_silence,
                                    fix_durations=[fix_durations[i]] if fix_durations and i < len(fix_durations) else [],
                                    wave_path=wav_path,
                                    spectrogram_path=spectrogram_path,
                                    concat=True
                                    )
            generated_waves.append(final_wave)
        final_wave = np.concatenate(generated_waves)
        if wave_path:
            if concat:
                with open(wave_path, "wb") as f:
                    sf.write(f.name, final_wave, self.target_sample_rate)
                    # Remove silence
                    if remove_silence:
                        aseg = AudioSegment.from_file(f.name)
                        non_silent_segs = silence.split_on_silence(aseg, min_silence_len=1000, silence_thresh=-50, keep_silence=500)
                        non_silent_wave = AudioSegment.silent(duration=0)
                        for non_silent_seg in non_silent_segs:
                            non_silent_wave += non_silent_seg
                        aseg = non_silent_wave
                        aseg.export(f.name, format="wav")
                    logger.info(f"Saved combined wave to {wave_path}")
            else:
                assert type(wave_path) == list, "wave_path must be a list of paths"
                assert len(wave_path) == len(generated_waves), "Number of paths must match number of generated waves"
                for _path in wave_path:
                    with open(_path, "wb") as f:
                        sf.write(f.name, generated_waves.pop(0), self.target_sample_rate)
                        # Remove silence
                        if remove_silence:
                            aseg = AudioSegment.from_file(f.name)
                            non_silent_segs = silence.split_on_silence(aseg, min_silence_len=1000, silence_thresh=-50, keep_silence=500)
                            non_silent_wave = AudioSegment.silent(duration=0)
                            for non_silent_seg in non_silent_segs:
                                non_silent_wave += non_silent_seg
                            aseg = non_silent_wave
                            aseg.export(f.name, format="wav")
                        logger.info(f"Saved wave to {_path}")
        else:
            # return the wave
            if concat:
                return final_wave
            else:
                return generated_waves

            
        
                    
    def clone(self, ref_audio, ref_text, gen_text_batches,
                speed=1.0, channel=-1, remove_silence=True,
                fix_durations=[], wave_path=None, spectrogram_path=None,
                concat=True, #if False, wav_path needs to be a list of paths
                ):
        ema_model = self.model
        # if os.path.exists(ref_audio): -> means ref_audio is a file path
        if isinstance(ref_audio, str):
            ref_audio = torchaudio.load(ref_audio)
        else:
            assert isinstance(ref_audio,tuple), "ref_audio must be a file path or a tuple of (audio, sr)\
                \n You can use torchaudio.load to load the audio file"
        audio, sr = ref_audio
        if audio.shape[0] > 1:
            if channel == -1:
                # Mean of all channels
                audio = torch.mean(audio, dim=0, keepdim=True)
                logger.info("Averaged all channels")
            else:
                audio = audio[channel].unsqueeze(0)        
        rms = torch.sqrt(torch.mean(torch.square(audio)))
        if rms < self.target_rms:
            audio = audio * self.target_rms / rms
        if sr != self.target_sample_rate:
            resampler = torchaudio.transforms.Resample(sr, self.target_sample_rate)
            audio = resampler(audio)
        audio = audio.to(self.device)
        generated_waves = []
        spectrograms = []
        for i, gen_text in enumerate(tqdm.tqdm(gen_text_batches)):
            # Prepare the text
            if len(ref_text[-1].encode('utf-8')) == 1:
                ref_text = ref_text + " "
            text_list = [ref_text + gen_text]
            final_text_list = convert_char_to_pinyin(text_list)

            # Calculate duration
            ref_audio_len = audio.shape[-1] // self.hop_length
            zh_pause_punc = r"。，、；：？！"
            ref_text_len = len(ref_text.encode('utf-8')) + 3 * len(re.findall(zh_pause_punc, ref_text))
            gen_text_len = len(gen_text.encode('utf-8')) + 3 * len(re.findall(zh_pause_punc, gen_text))
            duration = ref_audio_len + int(ref_audio_len / ref_text_len * gen_text_len / speed)
            if fix_durations and i < len(fix_durations):
                # fix_durations[i] is the duration(s)
                duration = fix_durations[i]
                duration = duration * self.target_sample_rate // self.hop_length
                logger.info(f"#{i} Fixed duration: {duration * self.hop_length / self.target_sample_rate:.2f}s")
                # duration = torch.tensor(duration)

            # inference
            with torch.inference_mode():
                generated, _ = ema_model.sample(
                    cond=audio,
                    text=final_text_list,
                    duration=duration,
                    steps=self.nfe_step,
                    cfg_strength=self.cfg_strength,
                    sway_sampling_coef=self.sway_sampling_coef,
                )

            generated = generated[:, ref_audio_len:, :]
            generated_mel_spec = rearrange(generated, "1 n d -> 1 d n")
            generated_wave = self.vocos.decode(generated_mel_spec.cpu())
            if rms < self.target_rms:
                generated_wave = generated_wave * rms / self.target_rms

            # wav -> numpy
            generated_wave = generated_wave.squeeze().cpu().numpy()
            generated_waves.append(generated_wave)
            spectrograms.append(generated_mel_spec[0].cpu().numpy())

        # Combine all generated waves
        final_wave = np.concatenate(generated_waves)
        if wave_path:
            if concat:
                with open(wave_path, "wb") as f:
                    sf.write(f.name, final_wave, self.target_sample_rate)
                    # Remove silence
                    if remove_silence:
                        aseg = AudioSegment.from_file(f.name)
                        non_silent_segs = silence.split_on_silence(aseg, min_silence_len=1000, silence_thresh=-50, keep_silence=500)
                        non_silent_wave = AudioSegment.silent(duration=0)
                        for non_silent_seg in non_silent_segs:
                            non_silent_wave += non_silent_seg
                        aseg = non_silent_wave
                        aseg.export(f.name, format="wav")
                    logger.info(f"Saved combined wave to {wave_path}")
            else:
                assert type(wave_path) == list, "wave_path must be a list of paths"
                assert len(wave_path) == len(generated_waves), "Number of paths must match number of generated waves"
                for _path in wave_path:
                    with open(_path, "wb") as f:
                        sf.write(f.name, generated_waves.pop(0), self.target_sample_rate)
                        # Remove silence
                        if remove_silence:
                            aseg = AudioSegment.from_file(f.name)
                            non_silent_segs = silence.split_on_silence(aseg, min_silence_len=1000, silence_thresh=-50, keep_silence=500)
                            non_silent_wave = AudioSegment.silent(duration=0)
                            for non_silent_seg in non_silent_segs:
                                non_silent_wave += non_silent_seg
                            aseg = non_silent_wave
                            aseg.export(f.name, format="wav")
                        logger.info(f"Saved wave to {_path}")
        else:
            # return the wave
            if concat:
                return final_wave
            else:
                return generated_waves

        if spectrogram_path:
            # Create a combined spectrogram
            combined_spectrogram = np.concatenate(spectrograms, axis=1)
            save_spectrogram(combined_spectrogram, spectrogram_path)
            logger.info(f"Saved combined spectrogram to {spectrogram_path}")
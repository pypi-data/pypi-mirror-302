<p align="center">
  <img src="dspeech.png" alt="DCheck Logo" width="250">
</p>

# DSpeech: A Command-line Speech Processing Toolkit
[中文](README_zh.md) | English


DSpeech is an advanced command-line toolkit designed for speech processing tasks such as transcription, voice activity detection (VAD), punctuation addition, and emotion classification. It is built on top of state-of-the-art models and provides an easy-to-use interface for handling various speech processing jobs.

## 1. Installation

### 1.1 Prerequisites
- Python 3.6 or later
- PyTorch 1.7 or later
- torchaudio
- rich
- soundfile
- funasr (A lightweight AutoModel library for speech processing)

### 1.2 Installation Steps
1. Clone the repository:
    ```bash
    git clone https://gitee.com/iint/dspeech.git
    cd dspeech
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Directly install dspeech via pip:
    ```bash
    pip install dspeech
    ```
4. Set the `DSPEECH_HOME` environment variable to the directory where your models are stored:
    ```bash
    export DSPEECH_HOME=/path/to/dspeech/models
    ```
5. Download the necessary models and place them in the `DSPEECH_HOME` directory. You can download the models using the following commands (replace `<model_id>` with the actual model ID):
    ```bash
    export HF_ENDPOINT=https://hf-mirror.com
    huggingface-cli download --resume-download <model_id> --local-dir $DSPEECH_HOME/<model_name>
    ```

6. (Optional) Also you can install Dguard if you want to do the speaker diarization task:
    ```bash
    pip install dguard==0.1.20
    export DGUARD_MODEL_PATH=<path to dguard model home>
    dguard_info
    ```

7. Print the help message to see the available commands:
    ```bash
    dspeech help
    ```
    You should see a list of available commands and options.
    ```
        DSpeech: A Command-line Speech Processing Toolkit
    Usage: dspeech  
    Commands:
    help        Show this help message
    transcribe  Transcribe an audio file
    vad         Perform VAD on an audio file
    punc        Add punctuation to a text
    emo         Perform emotion classification on an audio file
    clone       Clone speaker's voice and generate audio
    clone_with_emo Clone speaker's voice with emotion and generate audio
    Options (for asr and emotion classify):
    --model      Model name (default: sensevoicesmall)
    --vad-model  VAD model name (default: fsmn-vad)
    --punc-model Punctuation model name (default: ct-punc)
    --emo-model  Emotion model name (default: emotion2vec_plus_large)
    --device     Device to run the models on (default: cuda)
    --file       Audio file path for transcribing, VAD, or emotion classification
    --text       Text to process with punctuation model
    --start      Start time in seconds for processing audio files (default: 0)
    --end        End time in seconds for processing audio files (default: end of file)
    --sample-rate Sample rate of the audio file (default: 16000)
    Options (for tts):
    --ref_audio  Reference audio file path for voice cloning
    --ref_text   Reference text for voice cloning
    --speaker_folder Speaker folder path for emotional voice cloning
    --text       Text to generate audio
    --audio_save_path Path to save the audio
    --spectrogram_save_path * [Optional] Path to save the spectrogram
    --speed      Speed of the audio
    --sample_rate Sample rate of the audio file (default: 16000)
    Example: dspeech transcribe --file audio.wav
    ```

## 2. Features
DSpeech offers the following functionalities:
- **Transcription**: Convert audio files to text using state-of-the-art speech recognition models.
- **Voice Activity Detection (VAD)**: Detect and segment speech regions in an audio file.
- **Punctuation Addition**: Add punctuation to raw text transcriptions to improve readability.
- **Emotion Classification**: Classify the emotional content of an audio file into various categories.
- **Voice Cloning**: Clone a voice from a given audio file using a text-to-speech (TTS) model.
- **Emotion TTS**: Generate emotional speech using a text-to-speech (TTS) model.

## 3. Introduction to the dspeech.STT
To use DSpeech in a Python script, you can import the `STT` class and create an instance with the desired models:

```python
from dspeech.stt import STT
# Initialize the STT handler with the specified models
handler = STT(model_name="paraformer-zh", vad_model="fsmn-vad", punc_model="ct-punc", emo_model="emotion2vec_plus_large")
# Transcribe an audio file
transcription = handler.transcribe_file("audio.wav")
print(transcription)
# Perform VAD on an audio file
vad_result = handler.vad_file("audio.wav")
print(vad_result)
# Add punctuation to a text
punctuation_text = handler.punc_result("this is a test")
print(punctuation_text)
# Perform emotion classification on an audio file
emotion_result = handler.emo_classify_file("audio.wav")
print(emotion_result)
```

## 4. Introduction to the dspeech.TTS

### 4.1 Initialization

To initialize the `TTS` module, create a `TTS` handler object specifying the target device (CPU or GPU) and sample rate for generated audio.

```python
from dspeech import TTS
import torch

# Initialize TTS handler
tts_handler = TTS(
    device="cuda",  # Use "cpu" if no GPU is available
    target_sample_rate=24000  # Define target sample rate for output audio
)
```

The `device` parameter can be set to "cuda" for GPU usage or "cpu" for running on the CPU.

### 4.2 Basic Voice Cloning

In basic voice cloning, you provide a reference audio and text, and the system generates a new speech that mimics the voice from the reference audio with the content of the provided text.

```python
import torchaudio

# Load reference audio using torchaudio
ref_audio, sample_rate = torchaudio.load("tests/a.wav")

# Clone voice based on reference audio and text
r = tts_handler.clone(
    ref_audio=(ref_audio, sample_rate),  # Reference audio in (Tensor, int) format or file path
    ref_text="Reference text",  # The transcription of the reference audio
    gen_text_batches=["Hello, my name is Xiao Ming", "I am an AI", "I can speak Chinese"],  # Text to generate speech for
    speed=1,  # Speech speed (1 is normal speed)
    channel=-1,  # Merge all channels (-1) or specify one channel
    remove_silence=True,  # Option to remove silence from the reference audio
    wave_path="tests/tts_output.wav",  # Path to save generated audio
    spectrogram_path="tests/tts_output.png",  # Path to save spectrogram of generated audio
    concat=True  # Whether to merge all generated audio into a single output file
)
```

**Parameters:**
- `ref_audio`: The reference audio in the format `(Tensor, int)` or as a file path.
- `ref_text`: The transcription of the reference audio.
- `gen_text_batches`: A list of text strings that you want to convert into speech.
- `speed`: Adjusts the speed of the generated speech (default is 1, for normal speed).
- `remove_silence`: Option to remove silence from the reference audio (boolean).
- `wave_path`: Path to save the generated audio file.
- `spectrogram_path`: Path to save the spectrogram image of the generated audio.

### 4.3 Extracting Speaker Information**

For complex voice cloning with multiple speakers and emotions, you need to extract speaker information from a directory containing multiple audio files for different speakers and emotions.

The directory should have the following structure:

```
<path>/
├── speaker1/
│   ├── happy.wav
│   ├── happy.txt
│   ├── neutral.wav
│   ├── neutral.txt
```

Each subdirectory represents a speaker, and each audio file should have an accompanying text file.

```python
# Extract speaker information from the folder
spk_info = tts_handler.get_speaker_info("tests/speaker")
print(spk_info)
```

This function returns a dictionary of speaker information, which will be used for advanced cloning tasks.

### 4.4 Voice Cloning with Emotions**

To clone a voice with emotional expressions, you can use the `clone_with_emo` method. The generated text should contain emotional markers, e.g., `[[zhaosheng_angry]]`, where `zhaosheng` is the speaker and `angry` is the emotion.

```python
r = tts_handler.clone_with_emo(
    gen_text_batches=[
        "[[zhaosheng_angry]] How could you talk to me like that? It's too much!",
        "[[zhaosheng_whisper]] Be careful, don't let anyone hear, it's a secret.",
        "[[zhaosheng_sad]] I'm really sad, things are out of my control."
    ],
    speaker_info=spk_info,  # Dictionary of speaker information
    speed=1,  # Speech speed
    channel=-1,  # Merge all channels
    remove_silence=True,  # Remove silence in the generated output
    wave_path="tests/tts_output_emo.wav",  # Path to save output audio with emotions
    spectrogram_path="tests/tts_output_emo.png"  # Path to save spectrogram with emotions
)
```

### 4.5 Multi-Speaker and Multi-Emotion Dialogues

For generating dialogues between multiple speakers with different emotions, make sure the directory `tests/speaker` contains subdirectories for each speaker, and the corresponding audio and text files exist for each emotion.

```python
# Extract speaker information for multiple speakers
spk_info = tts_handler.get_speaker_info("tests/speaker")

# Generate multi-speaker and multi-emotion dialogue
r = tts_handler.clone_with_emo(
    gen_text_batches=[
        "[[zhaosheng_angry]] How could you talk to me like that? It's too much!",
        "[[duanyibo_whisper]] Be careful, don't let anyone hear, it's a secret.",
        "[[zhaosheng_sad]] I'm really sad, things are out of my control."
    ],
    speaker_info=spk_info,  # Speaker information extracted from directory
    speed=1,  # Speech speed
    channel=-1,  # Merge all channels
    remove_silence=True,  # Remove silence from the reference audio
    wave_path="tests/tts_output_emo.wav",  # Path to save generated audio
    spectrogram_path="tests/tts_output_emo.png"  # Path to save generated spectrogram
)
```
This method will generate a single audio file containing speech from multiple speakers with different emotional expressions.

### 4.6 Output Files**

- **Wave Path (`wave_path`)**: Specifies where to save the generated audio output. If `concat=True`, all `gen_text_batches` will be concatenated into one audio file.
- **Spectrogram Path (`spectrogram_path`)**: Specifies where to save the spectrogram image of the generated speech. This is useful for visual analysis of the audio.


## Command-line Interface
DSpeech provides a command-line interface for quick and easy access to its functionalities. To see the available commands, run:
```bash
dspeech help

DSpeech: A Command-line Speech Processing Toolkit
Usage: dspeech  
Commands:
  transcribe  Transcribe an audio file
  vad         Perform VAD on an audio file
  punc        Add punctuation to a text
  emo         Perform emotion classification on an audio file
Options:
  --model      Model name (default: sensevoicesmall)
  --vad-model  VAD model name (default: fsmn-vad)
  --punc-model Punctuation model name (default: ct-punc)
  --emo-model  Emotion model name (default: emotion2vec_plus_large)
  --device     Device to run the models on (default: cuda)
  --file       Audio file path for transcribing, VAD, or emotion classification
  --text       Text to process with punctuation model
  --start      Start time in seconds for processing audio files (default: 0)
  --end        End time in seconds for processing audio files (default: end of file)
  --sample-rate Sample rate of the audio file (default: 16000)
Example: dspeech transcribe --file audio.wav

```

### Usage Examples
- **Transcribe an audio file**:
    ```bash
    dspeech transcribe --file audio.wav
    ```
- **Perform VAD on an audio file**:
    ```bash
    dspeech vad --file audio.wav
    ```
- **Add punctuation to a text**:
    ```bash
    dspeech punc --text "this is a test"
    ```
- **Perform emotion classification on an audio file**:
    ```bash
    dspeech emo --file audio.wav
    ```

## License
DSpeech is licensed under the MIT License. See the LICENSE file for more details.


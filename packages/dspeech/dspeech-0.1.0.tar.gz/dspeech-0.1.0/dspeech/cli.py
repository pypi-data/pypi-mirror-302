import argparse
import logging
import os
import sys
from rich.console import Console

from dspeech import STT, TTS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
console = Console()

def parse_args():
    parser = argparse.ArgumentParser(
        description="DSpeech: A Command-line Speech Processing Toolkit"
    )

    parser.add_argument(
        "command", 
        choices=["transcribe", "vad", "punc", "emo", "help", "tts", "clone", "clone_emo"],
        help="Choose the function: transcribe, vad, punc, emo"
    )

    parser.add_argument(
        "--model", 
        default="paraformer-zh", 
        help="Model name (paraformer-zh, sensevoicesmall)"
    )

    parser.add_argument(
        "--vad-model", 
        default="fsmn-vad", 
        help="VAD model name (default: fsmn-vad)"
    )

    parser.add_argument(
        "--punc-model", 
        default="ct-punc", 
        help="Punctuation model name (default: ct-punc)"
    )

    parser.add_argument(
        "--emo-model", 
        default="emotion2vec_plus_large", 
        help="Emotion model name (default: emotion2vec_plus_large)"
    )

    parser.add_argument(
        "--device", 
        default="cuda", 
        help="Device to run the models on (default: cuda)"
    )

    parser.add_argument(
        "--file", 
        help="Audio file path for transcribing, VAD, or emotion classification"
    )

    parser.add_argument(
        "--text", 
        help="Text to process with punctuation model"
    )

    parser.add_argument(
        "--start", 
        type=float, 
        default=0, 
        help="Start time in seconds for processing audio files (default: 0)"
    )

    parser.add_argument(
        "--end", 
        type=float, 
        default=-1, 
        help="End time in seconds for processing audio files (default: end of file)"
    )

    parser.add_argument(
        "--sample-rate", 
        type=int, 
        default=16000, 
        help="Sample rate of the audio file (default: 16000)"
    )

    parser.add_argument(
        "--ref_audio", 
        help="Reference audio file path for voice cloning",
        default=None
    )

    parser.add_argument(
        "--ref_text", 
        help="Reference text for voice cloning",
        default=None
    )

    parser.add_argument(
        "--speaker_folder", 
        help="Speaker folder path for emotional voice cloning",
        default=None
    )

    parser.add_argument(
        "--audio_save_path",
        help="Path to save the audio",
        default=None
    )

    parser.add_argument(
        "--spectrogram_save_path",
        help="Path to save the spectrogram",
        default=None
    )

    parser.add_argument(
        "--speed",
        type=float,
        help="Speed of the audio",
        default=None
    )


    return parser.parse_args()

def main():
    args = parse_args()

    if not args.command:
        console.print("[red]No command provided. Use `dspeech help` for help.")
        sys.exit(1)
    
    if args.command == "help" or args.command == "-h" or args.command == "--help" or args.command == "h" or args.command == "--h" or args.command == "-help"\
        or args.command == "H" or args.command == "--H" or args.command == "-HELP":
        console.print("[green]DSpeech: A Command-line Speech Processing Toolkit")
        console.print("[yellow]Usage: dspeech [command] [options]")
        console.print("[yellow]Commands:")
        console.print("[yellow]  help        Show this help message")
        console.print("[yellow]  transcribe  Transcribe an audio file")
        console.print("[yellow]  vad         Perform VAD on an audio file")
        console.print("[yellow]  punc        Add punctuation to a text")
        console.print("[yellow]  emo         Perform emotion classification on an audio file")
        console.print("[yellow]  clone       Clone speaker's voice and generate audio")
        console.print("[yellow]  clone_with_emo Clone speaker's voice with emotion and generate audio")

        console.print("[blue]Options (for asr and emotion classify):")
        console.print("[blue]  --model      Model name (default: sensevoicesmall)")
        console.print("[blue]  --vad-model  VAD model name (default: fsmn-vad)")
        console.print("[blue]  --punc-model Punctuation model name (default: ct-punc)")
        console.print("[blue]  --emo-model  Emotion model name (default: emotion2vec_plus_large)")
        console.print("[blue]  --device     Device to run the models on (default: cuda)")
        console.print("[blue]  --file       Audio file path for transcribing, VAD, or emotion classification")
        console.print("[blue]  --text       Text to process with punctuation model")
        console.print("[blue]  --start      Start time in seconds for processing audio files (default: 0)")
        console.print("[blue]  --end        End time in seconds for processing audio files (default: end of file)")
        console.print("[blue]  --sample-rate Sample rate of the audio file (default: 16000)")
        console.print("[purple]Options (for tts):")
        # if use clone need provice: --ref_audio (audio file path) --ref_text (if not provided, use transcribed text) --text (text to generate audio)
        # if use clone_with_emo need provice: --speaker_folder (folder path) --text (text to generate audio, with [[emo]] tag in it)
        console.print("[purple]  --ref_audio  Reference audio file path for voice cloning")
        console.print("[purple]  --ref_text   Reference text for voice cloning")
        console.print("[purple]  --speaker_folder Speaker folder path for emotional voice cloning")
        console.print("[purple]  --text       Text to generate audio")
        console.print("[purple]  --audio_save_path Path to save the audio")
        console.print("[purple]  --spectrogram_save_path * [Optional] Path to save the spectrogram")
        console.print("[purple]  --speed      Speed of the audio")
        # sample rate for tts
        console.print("[purple]  --sample_rate Sample rate of the audio file (default: 16000)")

        console.print(f"[green]Example: ")
        console.print(f"[yellow]  dspeech transcribe --file audio.wav")
        console.print(f"[yellow]  dspeech clone --ref_audio <audio_path> --ref_text <content for ref_audio> --text <content to clone> --audio_save_path <output_path>")

        sys.exit(0)
    # 如果command 是clone, clone_emo, help 则不需要handler
    if args.command == "clone" or args.command == "clone_emo" or args.command == "help":
        handler = None
    else:
        handler = STT(
            model_name=args.model,
            vad_model=args.vad_model,
            punc_model=args.punc_model,
            emo_model=args.emo_model,
            device=args.device
        )

    tts_handler = TTS(device=args.device, target_sample_rate=args.sample_rate)

    if args.command == "transcribe":
        if not args.file:
            console.print("[red]Please provide an audio file for transcription.")
            sys.exit(1)
        console.print(f"[green]Transcribing {args.file}...")
        result = handler.transcribe_file(args.file, start=args.start, end=args.end, sample_rate=args.sample_rate)
        console.print(f"[yellow]Transcription: {result}")

    elif args.command == "vad":
        if not args.file:
            console.print("[red]Please provide an audio file for VAD.")
            sys.exit(1)
        console.print(f"[green]Performing VAD on {args.file}...")
        vad_result = handler.vad_file(args.file, start=args.start, end=args.end, sample_rate=args.sample_rate)
        console.print(f"[yellow]VAD Result: {vad_result}")

    elif args.command == "punc":
        if not args.text:
            console.print("[red]Please provide text for punctuation.")
            sys.exit(1)
        console.print(f"[green]Adding punctuation to: {args.text}")
        punc_result = handler.punc_result(args.text)
        console.print(f"[yellow]Punctuation Result: {punc_result}")

    elif args.command == "emo":
        if not args.file:
            console.print("[red]Please provide an audio file for emotion classification.")
            sys.exit(1)
        console.print(f"[green]Performing emotion classification on {args.file}...")
        emo_result = handler.emo_classify_file(args.file, start=args.start, end=args.end, sample_rate=args.sample_rate)
        console.print(f"[yellow]Emotion Classification Result: {emo_result}")

    elif args.command == "tts":
        if not args.text:
            console.print("[red]Please provide text for TTS synthesis.")
            sys.exit(1)
        # ECHO not implemented
        console.print(f"[red]:( Sorry, TTS synthesis is not implemented yet.")
        # tts_handler = TTS(device=args.device)  # 假设有TTS类
        # console.print(f"[green]Synthesizing speech for text: {args.text}")
        # tts_result = tts_handler.tts(text=args.text, wave_path="output.wav")
        # console.print(f"[yellow]TTS audio saved to output.wav")

    elif args.command == "clone":
        if not args.ref_audio:
            console.print("[red]Please provide a reference audio file for voice cloning.")
            sys.exit(1)
        if not args.audio_save_path:
            console.print("[red]Audio save path is not provided.")
            sys.exit(1)
        if not args.ref_text:
            console.print(f"[red] Text for ref_audio is not provided. Transcribing ref_audio...(this may take a while) ")
            console.print(f"[yellow] For better results, provide the text for ref_audio.")
            # do asr
            if not handler:
                handler = STT(
                        model_name=args.model,
                        vad_model=args.vad_model,
                        punc_model=args.punc_model,
                        emo_model=args.emo_model,
                        device=args.device
                    )
            args.ref_text = handler.transcribe_file(args.ref_audio, sample_rate=16000)
            console.print(f"[yellow]Transcription of ref_audio: {args.ref_text}")
        console.print(f"[green]Cloning voice from {args.ref_audio}")
        clone_result = tts_handler.clone(ref_audio=args.ref_audio,
                                ref_text=args.ref_text,
                                gen_text_batches=args.text.split("|") if "|" in args.text else [args.text],
                                wave_path=args.audio_save_path,
                                remove_silence=True,
                                speed=args.speed if args.speed else 1.0,
                                channel=-1,
                                concat=True)

    elif args.command == "clone_emo":
        speaker_info = tts_handler.get_speaker_info(args.speaker_folder)
        if not args.audio_save_path:
            console.print("[red]Audio save path is not provided.")
            sys.exit(1)
        console.print(f"[green]Cloning voice with emotion from {args.speaker_folder}")
        clone_result = tts_handler.clone_with_emo(gen_text_batches=args.text.split("|") if "|" in args.text else [args.text],
                                        speaker_info=speaker_info,
                                        wave_path=args.audio_save_path,
                                        remove_silence=True,
                                        speed=args.speed if args.speed else 1.0,
                                        channel=-1,
                                        concat=True)

if __name__ == "__main__":
    main()

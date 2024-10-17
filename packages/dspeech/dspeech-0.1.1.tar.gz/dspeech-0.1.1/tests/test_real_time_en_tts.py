from RealtimeSTT import AudioToTextRecorder,DSpeech_Whisper

if __name__ == '__main__':
    # recorder = AudioToTextRecorder(use_microphone=False)
    asr = DSpeech_Whisper(device="cuda")
    # with open("tests/output.wav", "rb") as f:
    #     audio_chunk = f.read()
    # # split chunk into smaller chunks
    # chunk_size = 1024
    # print("Splitting audio into chunks")
    # for i in range(0, len(audio_chunk), chunk_size):
    #     print(f"Processing chunk {i} to {i+chunk_size}")
    #     recorder.feed_audio(audio_chunk[i:i+chunk_size])
    #     print("Transcription: ", recorder.text())
    import time
    start_time=time.time()
    r = asr.transcribe_file("tests/output.wav")
    print("Time taken: ", time.time()-start_time)
    
    for _data in r:
        print(f"Time: {_data.start} - {_data.end}")
        print(_data.text)
    
    # print(asr.transcribe_multi_segment_lang_detection_file("tests/output.wav"))
    asr.init_batch_transcription()
    start_time=time.time()
    print(asr.transcribe_batch("tests/output.wav", batch_size=10))
    print("Time taken: ", time.time()-start_time)





from dspeech import TTS
import torchaudio
import torch

# 初始化模型
tts_handler = TTS( device="cuda", # 设备
        target_sample_rate=24000, # 目标采样率
    )



# 试试多人多情绪对话生成把
# 还是通过说话人信息字典生成，注意此时tests/speaker目录下应该有多个说话人目录，每个说话人目录下有多个音频文件和对应的文本文件
spk_info = tts_handler.get_speaker_info("tests/speaker")
print(spk_info)

r = tts_handler.clone_with_emo(
    gen_text_batches=[
        # xieyukai : angry, whisper, sad, delighted, normal, proud, surprised
        # xuekaixiang : angry, whisper, sad, delighted, normal, surprised
        # duanyibo : angry, whisper, sad, delighted, 
        "[[xieyukai_angry]]你怎么能这样！你居然忘了今天是什么日子？太过分了！",
        "[[xuekaixiang_angry]]你别这样！我哪有忘，我只是…啊…忙了一点！",
        "[[duanyibo_delighted]]呃，那个，我觉得你们俩还是冷静一点吧…今天不是才刚过中午吗？",
        
        "[[xieyukai_sad]]忙？你永远都在忙，从来不顾我的感受…我真的很失望。",
        "[[xuekaixiang_sad]]唉，我也很累啊，你以为我不想陪你吗？但工作就是这么多。",
        "[[duanyibo_whisper]]嗯，我是不是不该在这儿啊？",

        "[[xieyukai_proud]]好吧！那我告诉你，我今天自己也安排了别的事情，我可不需要你记住每个日子！",
        "[[xuekaixiang_surprised]]你，你安排了别的事情？你怎么不早说！",
        "[[duanyibo_angry]]啊？所以你们两个是…各玩各的吗？",

        "[[xieyukai_whisper]]不想吵了，我只想安静一会儿。",
        "[[xuekaixiang_whisper]]我也是，唉，真不知道我们怎么变成这样的。",
        "[[duanyibo_delighted]]嘿嘿，看你们冷静下来了，那咱们一起喝杯咖啡怎么样？",

        "[[xieyukai_delighted]]嗯，好吧，那就一起去喝杯咖啡，今天还算没彻底毁掉。",
        "[[xuekaixiang_normal]]好吧，喝杯咖啡也行，反正我已经习惯了加班。",
        "[[duanyibo_angry]]等等！你们两个竟然就这么和好了？刚才吵得那么凶，我以为有戏看呢！",
    ],
    speaker_info=spk_info,
    speed=1,
    channel=-1,
    remove_silence=True,
    wave_path="tests/tts_output_emo2.wav",
    spectrogram_path="tests/tts_output_emo.png"
)

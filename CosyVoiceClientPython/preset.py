from gradio_client import Client
import os
import shutil

client = Client("<host>")

result = client.predict(
    _sound_radio="中文女",
    _synthetic_input_textbox="天天好心情，我们走的每一步，都是我们策略的一部分；你看到的所有一切，包括我此刻与你交谈，所做的一切，所说的每一句话，都有深远的含义。",
    _seed=0,
    api_name="/generate_audio"
)

print(result)

# result 是返回的本地音频地址
# 把result 保存到当前的目录下
audio_filename = "preset.mp3"
shutil.copy(result, audio_filename)

# 删除原始的 音频
os.remove(result)
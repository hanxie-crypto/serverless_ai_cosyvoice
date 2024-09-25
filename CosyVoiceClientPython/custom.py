import os
import shutil
from gradio_client import Client, file

client = Client("")  # <host>示例 http://cosyvoie-piyufb-xxxxx.cn-beijing.fcapp.run/

result = client.predict(
  _recorded_audio1=file('<host>file=/tmp/gradio/d8bcffa469a71afbe701df1ff62b08a3cdded5a6/haimian.wav'),
  _recorded_audio2=None,
  _prompt_input_textbox="今天的不开心就止于此吧，明天依旧光芒万丈哦",
  _language_radio="same",
  _synthetic_input_textbox="好嘛好嘛，来来来，我们走的每一步，都是我们策略的一部分；你看到的所有一切，包括我此刻与你交谈，所做的一切，所说的每一句话，都有深远的含义。",
  _seed=0,
  _audio_input_type_radio="upload_audio",
  api_name="/generate_audio_1"
)


# result 是返回的本地音频地址
# 把result 保存到当前的目录下
audio_filename = "custom.mp3"
shutil.copy(result, audio_filename)

# 删除原始的 音频
os.remove(result)
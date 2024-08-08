import os
import sys
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append('{}/third_party/AcademiCodec'.format(ROOT_DIR))
sys.path.append('{}/third_party/Matcha-TTS'.format(ROOT_DIR))

from modelscope import snapshot_download
snapshot_download('speech_tts/speech_kantts_ttsfrd', revision='v1.0.3', allow_file_pattern='ttsfrd-0.3.6-cp38-cp38-linux_x86_64.whl', local_dir='pretrained_models/speech_kantts_ttsfrd')
os.system('cd pretrained_models/speech_kantts_ttsfrd/ && pip install ttsfrd-0.3.6-cp38-cp38-linux_x86_64.whl')
os.system('sed -i s@pydantic.typing@typing_extensions@g /opt/conda/lib/python3.8/site-packages/inflect/__init__.py')
os.system('sed -i s@https://huggingface.co/facebook/audioseal/resolve/main/generator_base.pth@{}@g /opt/conda/lib/python3.8/site-packages/audioseal/cards/audioseal_wm_16bits.yaml'.format(os.path.join(ROOT_DIR, 'pretrained_models/audioseal/generator_base.pth')))

import gradio as gr
from css.advanced import advanced
from css.custom import custom
from css.preset import preset

audio_mode_choices = [('预置语音生成', 'preset'), ('定制语音生成（复刻录制声音）', 'custom'),
                      ('高级语音生成（自然语言控制）', 'advanced')]


def on_audio_mode_change(_audio_mode_radio):
    yield {
        preset_layout: gr.update(visible=_audio_mode_radio == 'preset'),
        custom_layout: gr.update(visible=_audio_mode_radio == 'custom'),
        advanced_layout: gr.update(visible=_audio_mode_radio == 'advanced')
    }


custom_css = """
.full-height {
    height: 100%;
}
"""

default_layout = 'preset'

with gr.Blocks(theme=gr.themes.Soft(), css=custom_css) as demo:
    gr.Markdown("### 语音生成 https://github.com/FunAudioLLM/CosyVoice")
    gr.Markdown("### 语音识别 https://github.com/FunAudioLLM/SenseVoice")
    audio_mode_radio = gr.Radio(choices=audio_mode_choices,
                                value=default_layout,
                                label="选择语音生成模式")
    with gr.Row():
        with gr.Column(visible=default_layout == 'preset') as preset_layout:
            preset()
        with gr.Column(visible=default_layout == 'custom') as custom_layout:
            custom()
        with gr.Column(
                visible=default_layout == 'advanced') as advanced_layout:
            advanced()

    audio_mode_radio.change(
        fn=on_audio_mode_change,
        inputs=[audio_mode_radio],
        outputs=[preset_layout, custom_layout, advanced_layout])

demo.queue().launch(server_name='0.0.0.0',server_port=50000)

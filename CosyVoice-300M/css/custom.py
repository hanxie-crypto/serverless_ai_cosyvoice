import random

import gradio as gr
from css.utils import *
from cosyvoice.cli.cosyvoice import CosyVoice
audio_input_type = [('上传录音', 'upload_audio'), ('在线录制', 'microphone')]
default_input_type = 'upload_audio'

# 定制语音生成
audio_desc = f"""注意：由于浏览器安全限制对于非https域名默认不会开启声音录入的能力，如果您想使用在线录制声音的功能需要按照以下方式操作
        1. Chrome 开发者模式：
            ○ 您可以在 Chrome 中启用实验性标志来允许 HTTP 访问摄像头和麦克风。
        步骤：

            + a. 打开 Chrome 浏览器。
            + b. 输入 chrome://flags/#unsafely-treat-insecure-origin-as-secure 并回车。
            + c. 将 Unsafely treat insecure origin as secure 设置为 Enabled。
            + d. 在 Origin to treat as secure 中输入您的 当前域名 地址（例如 http://cosyvoice-xxx.fcv3.xxx.cn-hangzhou.fc.devsapp.net ）。
            + e. 重启 Chrome 浏览器。
        2. Firefox 开发者模式：
            ○ Firefox 也允许您在开发模式下绕过 HTTPS 限制。
        步骤：

            + a. 打开 Firefox 浏览器。
            + b. 输入 about:config 并回车。
            + c. 搜索 media.getusermedia.insecure-origins.enabled。
            + d. 将此设置设置为 true。
            + e. 搜索 media.getusermedia.insecure-origins。
            + f. 添加您的 IP 地址作为值之一（例如 http://cosyvoice-xxx.fcv3.xxx.cn-hangzhou.fc.devsapp.net ）。"""

def custom():

    def audio_input_type_change(_audio_input_type):

        yield {
            upload_audio_layout: gr.update(visible=_audio_input_type == 'upload_audio'),
            microphone_layout: gr.update(
                visible=_audio_input_type == 'microphone')

        }

    def random_seed():
        return random.randint(1, 100000000)

    def generate_audio(_recorded_audio1, _recorded_audio2, _prompt_input_textbox, _language_radio,
                       _synthetic_input_textbox, _seed, _audio_input_type_radio):
        print(_audio_input_type_radio)
        _recorded_audio = _recorded_audio1 if _audio_input_type_radio == 'upload_audio' else _recorded_audio2
        print(_recorded_audio, _prompt_input_textbox,
              _language_radio, _synthetic_input_textbox, _seed)
        global cosyvoice_instruct  # 声明为全局变量
        global cosyvoice
        if _synthetic_input_textbox == '':
            gr.Warning('合成文本为空，您是否忘记输入合成文本？')
            return (target_sr, default_data)
        set_all_random_seed(_seed)
        if use_instruct(_synthetic_input_textbox):
            if cosyvoice_instruct == None:
                cosyvoice_instruct = CosyVoice(f'{model_path}/CosyVoice-300M-Instruct')
            model = cosyvoice_instruct
        else:
            if(cosyvoice == None):
               cosyvoice = CosyVoice(f'{model_path}/CosyVoice-300M')
            model = cosyvoice
        prompt_speech_16k = postprocess(load_wav(_recorded_audio, prompt_sr))
        if _language_radio == 'cross' or _prompt_input_textbox == '':
            output = model.inference_cross_lingual(
                _synthetic_input_textbox, prompt_speech_16k)
        else:
            output = model.inference_zero_shot(
                _synthetic_input_textbox, _prompt_input_textbox, prompt_speech_16k)
        audio_data = postprocess(output['tts_speech']).numpy().flatten()
        audio_data = add_watermark(audio_data)
        audio_data = (audio_data * (2**15)).astype(np.int16)
        return (target_sr, audio_data)

    with gr.Column():
        with gr.Row():
            with gr.Column(scale=1, min_width=400):
                audio_input_type_radio = gr.Radio(choices=audio_input_type,
                                                  value=default_input_type,
                                                  label="上传或在线录制声音")
                with gr.Row():
                    with gr.Column(visible=default_input_type == 'upload_audio') as upload_audio_layout:

                        recorded_audio1 = gr.Audio(
                            label="请上传3~10秒内参考音频，超过会报错！", type="filepath")
                    with gr.Column(visible=default_input_type == 'microphone') as microphone_layout:
                        with gr.Group():
                            recorded_audio2 = gr.Audio(sources=['microphone'],
                                                       label="录制音频文件",
                                                       type='filepath')
                            gr.Text("请点击录制，并朗读右方文字（中文或英文）完成录入",
                                    max_lines=1,
                                    container=False,
                                    interactive=False)
            with gr.Column(scale=10):
                prompt_input_textbox = gr.Textbox(label="输入待录制文本")
                gr.Examples(
                    label="示例待录制文本",
                    examples=example_prompt_text,
                    inputs=[prompt_input_textbox])

    with gr.Column():
        language_radio = gr.Radio(choices=[('同语种', 'same'), ('跨语种', 'cross')],
                                  value='same',
                                  label="输入合成文本")
        synthetic_input_textbox = gr.Textbox(show_label=False)
        gr.Examples(
            label="示例文本",
            examples=example_tts_text,
            inputs=[synthetic_input_textbox])

    with gr.Accordion(label="随机种子"):
        with gr.Row():
            with gr.Column(scale=1, min_width=180):
                seed_button = gr.Button(value="\U0001F3B2 随机换一换",
                                        elem_classes="full-height")
            with gr.Column(scale=10):
                seed = gr.Number(show_label=False,
                                 value=0,
                                 container=False,
                                 elem_classes="full-height")
    with gr.Column():
        generate_button = gr.Button("生成音频", variant="primary", size="lg")

    with gr.Column():
        output_audio = gr.Audio(label="合成音频", format="mp3")

    seed_button.click(fn=random_seed, outputs=[seed])

    audio_input_type_radio.change(
        fn=audio_input_type_change,
        inputs=[audio_input_type_radio],
        outputs=[upload_audio_layout, microphone_layout])

    generate_button.click(
        fn=generate_audio,
        inputs=[recorded_audio1, recorded_audio2, prompt_input_textbox,
                language_radio, synthetic_input_textbox, seed, audio_input_type_radio],
        outputs=[output_audio])

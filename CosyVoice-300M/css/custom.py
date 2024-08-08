import random

import gradio as gr
from css.utils import *


# 定制语音生成
def custom():

    def random_seed():
        return random.randint(1, 100000000)

    def generate_audio(_recorded_audio, _prompt_input_textbox, _language_radio,
                       _synthetic_input_textbox, _seed):
        print(_recorded_audio, _prompt_input_textbox, _language_radio, _synthetic_input_textbox, _seed)
        if _synthetic_input_textbox == '':
            gr.Warning('合成文本为空，您是否忘记输入合成文本？')
            return (target_sr, default_data)
        set_all_random_seed(_seed)
        if use_instruct(_synthetic_input_textbox):
            model = cosyvoice_instruct
        else:
            model = cosyvoice
        prompt_speech_16k = postprocess(load_wav(_recorded_audio, prompt_sr))
        if _language_radio == 'cross' or _prompt_input_textbox == '':
            output = model.inference_cross_lingual(_synthetic_input_textbox, prompt_speech_16k)
        else:
            output = model.inference_zero_shot(_synthetic_input_textbox, _prompt_input_textbox, prompt_speech_16k)
        audio_data = postprocess(output['tts_speech']).numpy().flatten()
        audio_data = add_watermark(audio_data)
        audio_data = (audio_data * (2**15)).astype(np.int16)
        return (target_sr, audio_data)

    with gr.Column():
        with gr.Row():
            with gr.Column(scale=1, min_width=400):
                with gr.Group():
                    recorded_audio = gr.Audio(sources=['microphone'],
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
    generate_button.click(
        fn=generate_audio,
        inputs=[recorded_audio, prompt_input_textbox, language_radio, synthetic_input_textbox, seed],
        outputs=[output_audio])

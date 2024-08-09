import os
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

import torch
import numpy as np
import random
import librosa
import torchaudio
from cosyvoice.utils.file_utils import load_wav
from audioseal import AudioSeal
seal = AudioSeal.load_generator("audioseal_wm_16bits")
seal.eval()
# detector = AudioSeal.load_detector("audioseal_detector_16bits")
# detector.eval()

from cosyvoice.cli.cosyvoice import CosyVoice
# cosyvoice= CosyVoice('speech_tts/CosyVoice-300M')
# cosyvoice_sft= CosyVoice('speech_tts/CosyVoice-300M-SFT')
# cosyvoice_instruct= CosyVoice('speech_tts/CosyVoice-300M-Instruct')
model_path = os.environ.get('PRETRAINED_MODELS_DIR', '/cosyvoice/pretrained_models')
cosyvoice= CosyVoice(f'{model_path}/CosyVoice-300M')
cosyvoice_sft= CosyVoice(f'{model_path}/CosyVoice-300M-SFT')
cosyvoice_instruct= CosyVoice(f'{model_path}/CosyVoice-300M-Instruct')

example_tts_text = ["我们走的每一步，都是我们策略的一部分；你看到的所有一切，包括我此刻与你交谈，所做的一切，所说的每一句话，都有深远的含义。",
                    "那位喜剧演员真有才，[laughter]一开口就让全场观众爆笑。",
                    "他搞的一个恶作剧，让大家<laughter>忍俊不禁</laughter>。"]

example_prompt_text = ["我是通义实验室语音团队全新推出的生成式语音大模型，提供舒适自然的语音合成能力。",
                        "I am a newly launched generative speech large model by the Qwen Voice Team of the Tongyi Laboratory, offering comfortable and natural text-to-speech synthesis capabilities."]

# 加过了音频水印，target_sr 16000
prompt_sr, target_sr = 16000, 16000
default_data = np.zeros(target_sr)
def set_all_random_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

max_val = 0.8
def postprocess(speech, top_db=60, hop_length=220, win_length=440):
    speech, _ = librosa.effects.trim(
        speech, top_db=top_db,
        frame_length=win_length,
        hop_length=hop_length
    )
    if speech.abs().max() > max_val:
        speech = speech / speech.abs().max() * max_val
    speech = torch.concat([speech, torch.zeros(1, int(target_sr * 0.2))], dim=1)
    return speech

def use_instruct(text):
    for symbol in ['<endofprompt>', '<laughter>', '</laughter>', '<strong>', '</strong>', '[laughter]', '[breath]']:
        if symbol in text:
            return True
    return False

@torch.inference_mode()
def add_watermark(waveform):
    waveform = torch.from_numpy(waveform).view(1, -1)
    waveform_16k = torchaudio.transforms.Resample(orig_freq=22050, new_freq=16000)(waveform).view(1, 1, -1)
    watermark = seal.get_watermark(waveform_16k, 16000)
    waveform_16k += watermark
    return waveform_16k.flatten().numpy()
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/CosyVoice

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update -y
RUN apt-get -y install git unzip git-lfs
RUN git lfs install
RUN git clone https://www.modelscope.cn/studios/iic/CosyVoice-300M.git /opt/CosyVoice


RUN cd CosyVoice && pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M.git pretrained_models/CosyVoice-300M \
    git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M-SFT.git pretrained_models/CosyVoice-300M-SFT \
    git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M-Instruct.git pretrained_models/CosyVoice-300M-Instruct
    
RUN export PYTHONPATH=third_party/AcademiCodec:third_party/Matcha-TTS

WORKDIR /opt/CosyVoice

CMD ["python3", "app.py", "--port", "50000", "--model_dir", "speech_tts/CosyVoice-300M"]



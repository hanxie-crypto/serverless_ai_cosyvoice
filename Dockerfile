# 第一阶段: 构建依赖
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime AS builder
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /cosyvoice

# 更新源列表
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update -y

# 安装依赖
RUN apt-get install -y git unzip git-lfs
RUN apt-get install -y sox libsox-dev 
RUN rm -rf /var/lib/apt/lists/*

# 安装Git LFS
RUN git lfs install

# 安装依赖
COPY ./CosyVoice-300M /cosyvoice
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN mkdir -p pretrained_models

RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M.git pretrained_models/CosyVoice-300M
RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M-SFT.git pretrained_models/CosyVoice-300M-SFT
RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M-Instruct.git pretrained_models/CosyVoice-300M-Instruct
RUN git clone https://www.modelscope.cn/speech_tts/speech_kantts_ttsfrd.git pretrained_models/speech_kantts_ttsfrd
# 安装特定的模型包
WORKDIR /cosyvoice/pretrained_models/speech_kantts_ttsfrd
RUN unzip resource.zip -d .
RUN pip install ttsfrd-0.3.6-cp38-cp38-linux_x86_64.whl
RUN export PYTHONPATH=third_party/AcademiCodec:third_party/Matcha-TTS
# 设置启动命令
WORKDIR /cosyvoice
CMD ["python3", "app.py", "--port", "50000", "--model_dir", "speech_tts/CosyVoice-300M"]
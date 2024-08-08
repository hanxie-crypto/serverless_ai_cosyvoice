# 第一阶段: 构建依赖
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime AS builder
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /build

# 更新源列表
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN apt-get update -y

# 安装依赖
RUN apt-get install -y git unzip git-lfs && \
    rm -rf /var/lib/apt/lists/*

# 安装Git LFS
RUN git lfs install

# 创建Python环境
RUN conda create -n cosyvoice python=3.8 -y && \
    echo "conda activate cosyvoice" >> ~/.bashrc && \
    source ~/.bashrc

# 安装依赖
COPY ./CosyVoice-300M/requirements.txt /build/requirements.txt
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

# 第二阶段: 构建最终镜像
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /opt/CosyVoice

# 复制项目文件
COPY --from=builder /build/requirements.txt .
COPY ./CosyVoice-300M /opt/CosyVoice

# 安装额外的软件包
RUN apt-get update -y && \
    apt-get install -y sox libsox-dev && \
    rm -rf /var/lib/apt/lists/*
RUN mkdir -p pretrained_models
RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M.git pretrained_models/CosyVoice-300M
RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M-SFT.git pretrained_models/CosyVoice-300M-SFT
RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M-Instruct.git pretrained_models/CosyVoice-300M-Instruct
RUN git clone https://www.modelscope.cn/speech_tts/speech_kantts_ttsfrd.git pretrained_models/speech_kantts_ttsfrd
# 安装特定的模型包
WORKDIR /opt/CosyVoice/pretrained_models/speech_kantts_ttsfrd
RUN unzip resource.zip -d .
RUN pip install ttsfrd-0.3.6-cp38-cp38-linux_x86_64.whl
RUN export PYTHONPATH=third_party/AcademiCodec:third_party/Matcha-TTS
# 设置启动命令
WORKDIR /opt/CosyVoice
CMD ["python3", "app.py", "--port", "50000", "--model_dir", "speech_tts/CosyVoice-300M"]
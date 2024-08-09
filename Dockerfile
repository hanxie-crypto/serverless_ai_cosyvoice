FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel
USER root
ENV ROOT=/cosyvoice
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=${ROOT}:$PYTHONPATH
ENV PORT=50000
LABEL MAINTAINER="hanxie"

RUN mkdir -p ${ROOT}

WORKDIR ${ROOT}

ENV PRETRAINED_MODELS_DIR=${ROOT}/pretrained_models
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
COPY ./CosyVoice-300M ${ROOT}
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
RUN mkdir -p pretrained_models

RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M.git ${PRETRAINED_MODELS_DIR}/CosyVoice-300M
# RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M-SFT.git ${PRETRAINED_MODELS_DIR}/CosyVoice-300M-SFT
# RUN git clone https://www.modelscope.cn/speech_tts/CosyVoice-300M-Instruct.git ${PRETRAINED_MODELS_DIR}/CosyVoice-300M-Instruct
RUN git clone https://www.modelscope.cn/speech_tts/speech_kantts_ttsfrd.git ${PRETRAINED_MODELS_DIR}/speech_kantts_ttsfrd
# 安装特定的模型包
WORKDIR ${PRETRAINED_MODELS_DIR}/speech_kantts_ttsfrd
RUN unzip resource.zip -d .
# RUN pip install ttsfrd-0.3.6-cp38-cp38-linux_x86_64.whl
RUN pip3 install -U ttsfrd -f https://modelscope.oss-cn-beijing.aliyuncs.com/releases/repo.html
RUN export PYTHONPATH=third_party/AcademiCodec:third_party/Matcha-TTS
# 设置启动命令
WORKDIR ${ROOT}
CMD ["python3", "app.py", "--port", "50000", "--model_dir", "${PRETRAINED_MODELS_DIR}/CosyVoice-300M"]
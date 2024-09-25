

# conda activate cosyvoice
# pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host=mirrors.aliyun.com

# mv /root/root/CosyVoice-300M/pretrained_models /root/root/pretrained_models


# 将 /root/root/CosyVoice-300M/pretrained_models 所有文件软连接到 /root/root/pretrained_models
# 执行启动脚本 python3 ./CosyVoicae-300M/app.py --port 50000 --model_dir speech_tts/CosyVoice-300M

#!/bin/bash
 
# 激活conda环境
conda activate cosyvoice
source ~/.bashrc
# 创建软链接
source_dir="/root/root/CosyVoice-300M/pretrained_models"
target_dir="/root/root/pretrained_models"


find ${source_dir} | while read -r file; do
    SRC="${file}"
    DST="${target_dir}/${file#$source_dir/}"

    if [ ! -e "$DST" ] && [ ! -d "$SRC" ]; then
        mount_file "$SRC" "$DST"
    fi
done

# 执行启动脚本
cd /root/root/CosyVoice-300M
python3 app.py --port 50000 --model_dir speech_tts/CosyVoice-300M

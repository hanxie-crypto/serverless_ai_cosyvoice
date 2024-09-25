#!/bin/bash


set -Eeuo pipefail

function mount_file() {
  echo Mount $1 to $2

  SRC="$1"
  DST="$2"

  rm -rf "${DST}"

  if [ ! -f "${SRC}" ]; then
    mkdir -pv "${SRC}"
  fi

  mkdir -pv "$(dirname "${DST}")"

  ln -sT "${SRC}" "${DST}"
}


NAS_DIR="/mnt/auto/cosyvoice_pretrained_models"

# 内置模型准备
# 如果挂载了 NAS，软链接到 NAS 中
# 如果未挂载 NAS，则尝试直接将内置模型过载
NAS_MOUNTED=0
if [ -d "/mnt/auto" ]; then
  NAS_MOUNTED=1
fi

if [ "$NAS_MOUNTED" == "1" ]; then

  mkdir -p "${PRETRAINED_MODELS_DIR}/CosyVoice-300M-Instruct"

  echo "with NAS,${PRETRAINED_MODELS_DIR}/CosyVoice-300M-Instruct"

  find ${NAS_DIR} | while read -r file; do
    SRC="${file}"
    DST="${PRETRAINED_MODELS_DIR}/CosyVoice-300M-Instruct/${file#$NAS_DIR/}"

    if [ ! -e "$DST" ] && [ ! -d "$SRC" ]; then
      mount_file "$SRC" "$DST"
    fi
  done
else
  echo "start cosyvoice"
fi



declare -A MOUNTS


# MOUNTS["${ROOT}/models"]="${NAS_DIR}/pretrained_models/CosyVoice-300M"
# MOUNTS["${ROOT}/models"]="${NAS_DIR}/pretrained_models/CosyVoice-300M-SFT"
# MOUNTS["${PRETRAINED_MODELS_DIR}"]="${NAS_DIR}/CosyVoice-300M-Instruct"



# for to_path in "${!MOUNTS[@]}"; do
#   mount_file "${MOUNTS[${to_path}]}" "${to_path}"
# done

# if [ -f "/mnt/auto/llm/startup.sh" ]; then
#   pushd ${ROOT}
#   . /mnt/auto/llm/startup.sh
#   popd
# fi

conda run --no-capture-output -n cosyvoice python app.py --port 50000 --model_dir "${PRETRAINED_MODELS_DIR}/CosyVoice-300M"
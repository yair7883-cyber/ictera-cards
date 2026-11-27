#!/usr/bin/env bash
# Installs the local audio toolkit: a Python 3.12 venv and its models, each model checked by SHA-256.
# Idempotent. First run downloads about 6 GB (PyTorch comes from PyPI with its CUDA libraries) and takes a few minutes.
set -euo pipefail
V="${AUDIO_TOOLS_HOME:-$HOME/.local/share/audio-tools}"
M="$V/models"
UV=$(command -v uv || echo "$HOME/.local/bin/uv")

fetch() { # fetch <url> <dest> <sha256>
  if [ -f "$2" ] && echo "$3  $2" | sha256sum -c --status -; then return; fi
  mkdir -p "$(dirname "$2")"
  curl -fsSL --retry 3 -o "$2.part" "$1"
  echo "$3  $2.part" | sha256sum -c --status - || { rm -f "$2.part"; echo "checksum mismatch: $1" >&2; exit 1; }
  mv "$2.part" "$2"
}

"$UV" venv -q --allow-existing --python 3.12 "$V"
"$UV" pip install -q --python "$V/bin/python" torch==2.5.1 torchaudio==2.5.1 demucs==4.0.1 \
  faster-whisper==1.2.1 sherpa-onnx==2.0.3 soundfile==0.14.0 onnxruntime==1.32.0 numpy==2.1.3 \
  librosa==1.0.1 mir_eval==0.8.2 pretty_midi==0.2.11.post0 resampy==0.4.3 scipy==1.18.1
# basic-pitch's declared deps pull TensorFlow, which has no Python 3.12 wheel; it runs on onnxruntime instead.
"$UV" pip install -q --python "$V/bin/python" --no-deps basic-pitch==0.4.0

# Demucs htdemucs weights (official file name and hash; dl.fbaipublicfiles.com is blocked here, so a Hugging Face mirror).
fetch https://huggingface.co/JosefKuchar/Demucs/resolve/main/955717e8-8726e21a.th \
  "${TORCH_HOME:-$HOME/.cache/torch}/hub/checkpoints/955717e8-8726e21a.th" \
  8726e21a993978c7ba086d3872e7608d7d5bfca646ca4aca459ffda844faa8b4
# Speaker diarization: pyannote segmentation 3.0 (MIT) and 3D-Speaker ERes2Net embeddings (Apache-2.0), ONNX via sherpa-onnx.
fetch https://huggingface.co/csukuangfj/sherpa-onnx-pyannote-segmentation-3-0/resolve/main/model.onnx \
  "$M/segmentation.onnx" 220ad67ca923bef2fa91f2390c786097bf305bceb5e261d4af67b38e938e1079
fetch https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-recongition-models/3dspeaker_speech_eres2net_base_sv_zh-cn_3dspeaker_16k.onnx \
  "$M/embedding.onnx" f1ee61be04000b50392a63442e5dd9feaea7e81dddd494d3647cf1c3d88a1498
# RNNoise speech model for ffmpeg's arnndn filter.
fetch https://raw.githubusercontent.com/richardpl/arnndn-models/0fda24c46d78f0207d820bb970fbe85c1971b39c/sh.rnnn \
  "$M/sh.rnnn" 70bb6685eb0c2a1d18e2918dca3fbfbd39317010b1802eb1b6ea73a92f3fdec0

touch "$V/.ready-1"
echo "audio tools ready in $V"

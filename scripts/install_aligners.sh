#!/bin/bash

# Ensure conda init works properly
eval "$(conda shell.bash hook)"

# Create conda environment for Montreal Forced Aligner
echo "Creating conda environment for Montreal Forced Aligner..."
conda create -n mfa -c conda-forge -y montreal-forced-aligner
conda activate mfa
pip install joblib==1.2.0 seaborn
conda deactivate

# Create conda environment for NeMo
echo "Creating conda environment for NeMo..."
conda create -n nemo python=3.10.12 -y
conda activate nemo

# Install NeMo dependencies and NeMo
git clone -b aligner https://github.com/lifeiteng/NeMo.git third_party/NeMo
cd third_party/NeMo

pip install -r requirements/requirements_lightning.txt
pip install -r requirements/requirements_common.txt
pip install -r requirements/requirements_asr.txt
pip install pybind11 lhotse praatio datasets==2.19.0 huggingface-hub==0.23.2 numpy==1.24.3
pip install -e .

cd -
conda deactivate

# Create conda environment for CTC Forced Aligner
echo "Creating conda environment for CTC Forced Aligner..."
conda create -n ctc-aligner python=3.10 -y
conda activate ctc-aligner

git clone https://github.com/MahmoudAshraf97/ctc-forced-aligner.git third_party/ctc-forced-aligner
cd third_party/ctc-forced-aligner
git reset --hard eb8a750b9c91c3d2e2fda29264c82e252d84c3df
pip install -e .
pip install praatio
cd -

conda deactivate

# Create conda environment for WhisperX
echo "Creating conda environment for WhisperX..."
conda create -n whisperx python=3.9 -y
conda activate whisperx

pip install git+https://github.com/m-bain/whisperx.git
pip install lhotse praatio num2words
pip install .
conda deactivate
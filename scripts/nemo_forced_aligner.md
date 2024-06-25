# NeMo Forced Aligner (NFA)
* [https://github.com/NVIDIA/NeMo/tree/main/tools/nemo_forced_aligner](https://github.com/NVIDIA/NeMo/tree/main/tools/nemo_forced_aligner)

## run
```
git clone https://github.com/NVIDIA/NeMo.git
cd NeMo

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements/requirements_lightning.txt
pip install -r requirements/requirements_common.txt
pip install -r requirements/requirements_asr.txt


pip install pybind11 lhotse

pip install -e .

python <path_to_NeMo>/tools/nemo_forced_aligner/align.py \
    pretrained_name="stt_en_fastconformer_hybrid_large_pc" \
    manifest_filepath=<path to manifest of utterances you want to align> \
    output_dir=<path to where your output files will be saved>


deactivate
```
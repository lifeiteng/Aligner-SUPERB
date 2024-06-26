
## install MFA
## https://montreal-forced-aligner.readthedocs.io/en/latest/installation.html
conda create -n aligner -c conda-forge montreal-forced-aligner
# conda config --add channels conda-forge

## install NFA
git clone -b aligner https://github.com/lifeiteng/NeMo.git third_party/NeMo
cd third_party/NeMo

pip install -r requirements/requirements_lightning.txt
pip install -r requirements/requirements_common.txt
pip install -r requirements/requirements_asr.txt

pip install pybind11 lhotse

pip install -e .

cd -

## install ctc-forced-aligner

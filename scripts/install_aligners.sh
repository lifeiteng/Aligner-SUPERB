
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
git clone git+https://github.com/MahmoudAshraf97/ctc-forced-aligner.git third_party/ctc-forced-aligner
cd third_party/ctc-forced-aligner
git reset --hard eb8a750b9c91c3d2e2fda29264c82e252d84c3df

pip install -e .
cd -


## whisperx
pip install git+https://github.com/m-bain/whisperx.git

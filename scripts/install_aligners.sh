
## install MFA

## install NFA
git clone https://github.com/lifeiteng/NeMo.git third_party/NeMo
cd third_party/NeMo

pip install -r requirements/requirements_lightning.txt
pip install -r requirements/requirements_common.txt
pip install -r requirements/requirements_asr.txt

pip install pybind11 lhotse

pip install -e .

cd -

stage=-1

. scripts/parse_options.sh || exit 1

log() {
  # This function is from espnet
  local fname=${BASH_SOURCE[1]##*/}
  echo -e "$(date '+%Y-%m-%d %H:%M:%S') (${fname}:${BASH_LINENO[0]}:${FUNCNAME[1]}) $*"
}

if [ $stage -le 0 ]; then
    log "Stage 0: Download & Prepare TIMIT"
    lhotse download timit datasets
    lhotse prepare timit datasets/timit manifests/timit

    for sub in DEV TEST TRAIN;do
        lhotse cut simple --recording-manifest manifests/timit/timit_recordings_${sub}.jsonl.gz \
            --supervision-manifest manifests/timit/timit_supervisions_${sub}.jsonl.gz \
            manifests/timit/timit_cuts_${sub}.jsonl.gz
    done
fi

if [ $stage -le 1 ]; then
    log "Stage 1: Prepare Target TextGrid files"
    mkdir -p alignments/TIMIT_TARGET_DEV
    python scripts/covert_lhotse_to_tgt.py `pwd` alignments/TIMIT_TARGET_DEV
fi

if [ $stage -le 2 ]; then
    log "Stage 2: Prepare NFA json files"
    python -c"
import os
import sys
from pathlib import Path
from nemo.collections.asr.parts.utils.manifest_utils import write_manifest
from lhotse import load_manifest

def get_source_file(cut):
    assert len(cut.recording.sources) == 1
    source = cut.recording.sources[0].source
    return source


def get_supervision_text(supervision):
    return ' '.join([w[0] for w in supervision.alignment['word']])


DIR, LINKDIR = sys.argv[1], sys.argv[2]

# for sub in ['DEV', 'TEST', 'TRAIN']:
for sub in ['DEV']:
    cuts = load_manifest(f'manifests/timit/timit_cuts_{sub}.jsonl.gz')

    meta = []
    for cut in cuts:
        # text = '|'.join([s.text for s in cut.supervisions])
        text = '|'.join([get_supervision_text(s) for s in cut.supervisions])

        audio_filepath = f'{LINKDIR}/{sub}_{cut.id}.wav'
        assert Path(audio_filepath).exists(), f'File {audio_filepath} does not exist'
        meta.append({'audio_filepath': audio_filepath, 'text': text})

    write_manifest(f'manifests/timit/NFA_{sub}_manifest_with_text.json', meta)
" `pwd` `pwd`/alignments/TIMIT_TARGET_DEV
fi

if [ $stage -le 3 ]; then
    log "Stage 3: Generate MFA TextGrid files"

    # conda activate aligner
    conda activate aligner

    export MFA_ROOT_DIR=~/Documents/MFA
    mfa model download acoustic english_us_arpa
    mfa model download dictionary english_us_arpa

    # for sub in DEV TEST TRAIN;do
    for sub in DEV;do
        mkdir -p alignments/TIMIT_MFA_${sub}
        # 下载测试数据
        # https://montreal-forced-aligner.readthedocs.io/en/latest/first_steps/example.html#alignment-example
        mfa align --clean TIMIT_TARGET_${sub} english_us_arpa alignments/TIMIT_MFA_${sub}
    done
    conda deactivate
fi

if [ $stage -le 4 ]; then
    log "Stage 4: Generate NFA TextGrid files"

    NFA_DIR=third_party/NeMo
    # for sub in DEV TEST TRAIN;do
    for sub in DEV;do
        python ${NFA_DIR}/tools/nemo_forced_aligner/align.py \
            additional_segment_grouping_separator="|" \
            "save_output_file_formats=['tgt']" \
            pretrained_name="stt_en_fastconformer_hybrid_large_pc" \
            manifest_filepath=manifests/timit/NFA_${sub}_manifest_with_text.json \
            output_dir=alignments/TIMIT_NFA_${sub}
    done
fi

log "Stage 5: Evalute NFA"
if [ ! -d "alignments/TIMIT_TARGET_DEV" ]; then
    log "Target TextGrid not found. Please run stage 2 first"
    exit 1
fi

if [ ! -d "alignments/TIMIT_MFA_DEV" ]; then
    log "MFA alignment not found. Please run stage 3 first"
    exit 1
fi

if [ ! -d "alignments/TIMIT_NFA_DEV" ]; then
    log "NFA alignment not found. Please run stage 4 first"
    exit 1
fi

alignersuperb metrics -t alignments/TIMIT_TARGET_DEV alignments/TIMIT_NFA_DEV


echo "Stage 0: Download & Prepare TIMIT"
lhotse download timit datasets
lhotse prepare timit datasets/timit manifests/timit

for sub in DEV TEST TRAIN;do
    lhotse cut simple --recording-manifest manifests/timit/timit_recordings_${sub}.jsonl.gz \
        --supervision-manifest manifests/timit/timit_supervisions_${sub}.jsonl.gz \
        manifests/timit/timit_cuts_${sub}.jsonl.gz
done

echo "Stage 1: Prepare Target TextGrid files"
mkdir -p alignments/TIMIT_TGT_TARGET
python scripts/covert_lhotse_to_tgt.py `pwd` alignments/TIMIT_TGT_TARGET

echo "Stage 2: Prepare NFA json files"
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
" `pwd` `pwd`/alignments/TIMIT_TGT_TARGET

echo "Stage 3: Generate NFA TextGrid files"

NFA_DIR=/Users/feiteng/NVIDIA/NeMo
# for sub in DEV TEST TRAIN;do
for sub in DEV;do
    python ${NFA_DIR}/tools/nemo_forced_aligner/align.py \
        additional_segment_grouping_separator="|" \
        "save_output_file_formats=['tgt']" \
        pretrained_name="stt_en_fastconformer_hybrid_large_pc" \
        manifest_filepath=manifests/timit/NFA_${sub}_manifest_with_text.json \
        output_dir=alignments/TIMIT_NFA_${sub}
done

echo "Stage 4: Evalute NFA"
alignersuperb metrics -t alignments/TIMIT_TGT_TARGET alignments/TIMIT_NFA_DEV

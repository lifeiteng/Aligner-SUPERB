import sys
import os
from lhotse import load_manifest
import praatio
from praatio import textgrid
from pathlib import Path

def get_source_file(cut):
    assert len(cut.recording.sources) == 1
    source = cut.recording.sources[0].source
    return source

DIR, TGTDIR = sys.argv[1], sys.argv[2]

# for sub in ['DEV', 'TEST', 'TRAIN']:
for sub in ['DEV']:
    cuts = load_manifest(f'manifests/timit/timit_cuts_{sub}.jsonl.gz')
    for cut in cuts[:10]:
        audio_filepath = f'{TGTDIR}/{sub}_{cut.id}.wav'
        if Path(audio_filepath).exists():
            os.remove(audio_filepath)
        os.symlink(f'{DIR}/{get_source_file(cut)}', audio_filepath)

        segments, words = [], []
        for s in cut.supervisions:
            segments.append((s.start, s.start + s.duration, s.text))
            for word in s.alignment["word"]:
                words.append((word[1], word[1] + word[2], word[0]))

        # keep same as prepare_data.sh
        output_file = f'{TGTDIR}/{sub}_{cut.id}.TextGrid'

        try:
            tg = textgrid.Textgrid()
            segmentTier = textgrid.IntervalTier('segments', segments)
            wordTier = textgrid.IntervalTier('words', words)
        except praatio.utilities.errors.TextgridStateError:
            # TIMIT ERRORS
            # 31800 40009 entity
            # 41324 45667 over
            # 44120 46280 and
            # 46280 51560 above

            print(f"Error processing {cut.id}")

        tg.addTier(segmentTier)
        tg.addTier(wordTier)
        tg.save(output_file, format="short_textgrid", includeBlankSpaces=True)

import json
import logging
from pathlib import Path

import torch
import whisperx
from lhotse.workflows.forced_alignment import ASRForcedAligner, FailedToAlign, ForcedAligner, MMSForcedAligner  # noqa
from praatio import textgrid
from tqdm import tqdm

TORCH_DTYPES = {
    "bfloat16": torch.bfloat16,
    "float16": torch.float16,
    "float32": torch.float32,
}


def cli():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--manifest_filepath", help="filepath to the manifest of the data you want to align", required=True
    )
    parser.add_argument("--output_dir", help="the folder where output TextGrid files will be saved.", required=True)

    parser.add_argument(
        "--language",
        type=str,
        default=None,
        required=True,
        help="Language in ISO 639-3 code. Identifying the input as Arabic, Belarusian,"
        " Bulgarian, English, Farsi, German, Ancient Greek, Modern Greek, Pontic Greek"
        ", Hebrew, Kazakh, Kyrgyz, Latvian, Lithuanian, North Macedonian, Russian, "
        "Serbian, Turkish, Ukrainian, Uyghur, Mongolian, Thai, Javanese or Yiddish "
        "will improve romanization for those languages, No effect for other languages.",
    )

    parser.add_argument(
        "--device",
        default="cuda" if torch.cuda.is_available() else "cpu",
        help="if you have a GPU use 'cuda', otherwise 'cpu'",
    )
    parser.add_argument(
        "--aligner",
        type=str,
        default="MMSForcedAligner",
        required=False,
        help="ASRForcedAligner or MMSForcedAligner",
    )

    args = parser.parse_args()

    device = torch.device(args.device)
    aligner = eval(args.aligner)(device=device)

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    for line in tqdm(open(args.manifest_filepath).readlines(), desc="Lhotse CTC Aligning"):
        # {"audio_filepath": "alignments/TIMIT_TARGET_DEV/DEV_FNMR0-SX139-0.wav", "text": "the bungalow was pleasantly situated near the shore"}
        data = json.loads(line)
        text = data["text"]
        audio = whisperx.load_audio(data["audio_filepath"])

        results = aligner.align(
            torch.from_numpy(audio).unsqueeze(0), aligner.normalize_text(text, language=args.language)
        )

        segments, words = [], []
        segments.append((results[0].start, results[-1].end, text))
        for word in results:
            words.append((word.start, word.end, word.symbol.lower()))

        tg = textgrid.Textgrid()
        try:
            segmentTier = textgrid.IntervalTier("segments", segments)
            wordTier = textgrid.IntervalTier("words", words)
        except Exception as e:
            for k, (cur, next) in enumerate(zip(words[:-1], words[1:])):
                if cur[1] > next[0]:
                    logging.warning(f"Overlapping words: {cur} and {next}")
                    words[k + 1] = (cur[1], next[1], next[2])
                    logging.warning(f"Fixed: {words[k + 1]}")
            segmentTier = textgrid.IntervalTier("segments", segments)
            wordTier = textgrid.IntervalTier("words", words)

        tg.addTier(segmentTier)
        tg.addTier(wordTier)

        output_file = f"{args.output_dir}/{Path(data['audio_filepath']).stem}.TextGrid"
        tg.save(output_file, format="long_textgrid", includeBlankSpaces=True)


if __name__ == "__main__":
    cli()

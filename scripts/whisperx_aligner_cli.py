# base on https://github.com/m-bain/whisperX
import torch
import whisperx
import json
from praatio import textgrid
from pathlib import Path
from tqdm import tqdm

TORCH_DTYPES = {
    "bfloat16": torch.bfloat16,
    "float16": torch.float16,
    "float32": torch.float32,
}


def cli():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest_filepath", help="filepath to the manifest of the data you want to align", required=True)
    parser.add_argument(
        "--output_dir", help="the folder where output TextGrid files will be saved.", required=True
    )

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
    args = parser.parse_args()

    device = torch.device(args.device)
    model, metadata = whisperx.load_align_model(language_code=args.language, device=device)

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    for line in tqdm(open(args.manifest_filepath).readlines(), desc="WhisperX CTC Aligning"):
        # {"audio_filepath": "alignments/TIMIT_TARGET_DEV/DEV_FNMR0-SX139-0.wav", "text": "the bungalow was pleasantly situated near the shore"}
        data = json.loads(line)
        text = data['text']
        audio = whisperx.load_audio(data["audio_filepath"])

        results = whisperx.align([{"start": 0.0, "end": audio.shape[-1]/ 16000, "text": text}], model, metadata, audio, device, return_char_alignments=False)

        segments, words = [], []
        for segment in results["segments"]:
            segments.append((segment["start"], segment["end"], segment["text"]))
            for word in segment["words"]:
                words.append((word["start"], word["end"], word["word"]))

        tg = textgrid.Textgrid()
        segmentTier = textgrid.IntervalTier("segments", segments)
        wordTier = textgrid.IntervalTier("words", words)

        tg.addTier(segmentTier)
        tg.addTier(wordTier)

        output_file = f"{args.output_dir}/{Path(data['audio_filepath']).stem}.TextGrid"
        tg.save(output_file, format="long_textgrid", includeBlankSpaces=True)


if __name__ == "__main__":
    cli()

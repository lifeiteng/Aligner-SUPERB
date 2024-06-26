from typing import Dict

from praatio.textgrid import Textgrid

from .base import Metric


def to_milliseconds(v):
    return int(v * 1000)


to_ms = to_milliseconds


class WordBoundaryError(Metric):
    def __init__(self):
        super().__init__("WBE")

    def __call__(self, target: Dict[str, Textgrid], align: Dict[str, Textgrid]) -> Dict[str, str]:
        total_wbe, total_wbe_start, total_wbe_end = [], [], []

        for key in target.keys():
            tg_target, tg_align = target[key], align[key]
            utt_wbe, utt_wbe_start, utt_wbe_end = [], [], []
            for word_target, word_align in zip(tg_target.getTier("words"), tg_align.getTier("words")):
                if not word_target.label:
                    continue

                assert word_target.label == word_align.label, f"Word mismatch: {word_target.label}, {word_align.label}"

                wbe = 0.5 * (abs(word_target.start - word_align.start) + abs(word_target.end - word_align.end))
                utt_wbe.append(wbe)

                utt_wbe_start.append(abs(word_target.start - word_align.start))
                utt_wbe_end.append(abs(word_target.end - word_align.end))

            assert len(utt_wbe) > 0, "Empty utterance"
            total_wbe.append(sum(utt_wbe) / len(utt_wbe))
            total_wbe_start.append(sum(utt_wbe_start) / len(utt_wbe_start))
            total_wbe_end.append(sum(utt_wbe_end) / len(utt_wbe_end))

        avg_wbe = sum(total_wbe) / len(total_wbe)
        avg_wbe_start = sum(total_wbe_start) / len(total_wbe_start)
        avg_wbe_end = sum(total_wbe_end) / len(total_wbe_end)

        # to milliseconds
        return {
            self.name: f"{to_ms(avg_wbe)} ms",
            f"{self.name}_Start": f"{to_ms(avg_wbe_start)} ms",
            f"{self.name}_End": f"{to_ms(avg_wbe_end)} ms",
        }


class UtteranceBoundaryError(Metric):
    """
    Utterance Cross Boundary(Start & End).
    """

    def __init__(self):
        super().__init__("UBE")

    def __call__(self, target: Dict[str, Textgrid], align: Dict[str, Textgrid]) -> Dict[str, str]:
        total_ube_start, total_ube_end = [], []
        for key in target.keys():
            tg_target, tg_align = target[key], align[key]

            # TODO(Feiteng): use segments instead of words

            # start
            for word_target, word_align in zip(tg_target.getTier("words"), tg_align.getTier("words")):
                if not word_target.label:
                    raise ValueError(f"Empty word: {word_target}")
                assert word_target.label == word_align.label, f"Word mismatch: {word_target.label}, {word_align.label}"
                total_ube_start.append(int(word_target.start < word_align.start))
                break

            # end
            for word_target, word_align in zip(tg_target.getTier("words").entries[::-1], tg_align.getTier("words").entries[::-1]):
                if not word_target.label:  # skip empty
                    raise ValueError(f"Empty word: {word_target}")
                assert word_target.label == word_align.label, f"Word mismatch: {word_target.label}, {word_align.label}"
                total_ube_end.append(int(word_target.end > word_align.end))
                break

        avg_ube_start = sum(total_ube_start) / len(total_ube_start)
        avg_ube_end = sum(total_ube_end) / len(total_ube_end)

        return {
            "UBE_Start": f"{int(avg_ube_start * 100)}%",
            "UBE_End": f"{int(avg_ube_end * 100)}%",
            "Num UTTerances": len(total_ube_start),
        }

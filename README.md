# Aligner-SUPERB: **Speech-To-Text forced alignment** Speech Processing Universal Performance Benchmark

<!--![Overview](img/Overview.png)-->

Aligner-SUPERB is a comprehensive benchmark designed to evaluate **Speech-to-text forced alignment** models across a variety of languages and datasets. Our objective is to promote community collaboration and speed up advancements in the field of speech processing by preserving and improving the quality of speech information.

<!--<a href='https://alignersuperb.com/'><img src='https://img.shields.io/badge/Project-Page-Green'></a>-->

## Table of Contents

- [Introduction](#introduction)
- [Metrics](#metrics)
- [Installation](#installation)
- [Contribution](#contribution)
- [Forced Aligners](#forced-aligners)

## Introduction

Aligner-SUPERB is a new benchmark in evaluating Speech-to-text forced alignment models. Our goal is to set the standard for evaluating speech-to-text forced alignment.

## Metrics
* $`define\, |U| := number\,of\,utterances,\,\, |utt| := number\,words\,of\,the\,utterance`$

* **Word Boundary Error (WBE)**
    * measure how close the predicted and manually labeled timestamps are
    * $`WBE\_{Start} = \frac{1}{|U|} \sum\limits_{utt}^{|U|} \frac{1}{|utt|}\sum\limits_{w \in utt}|w^{ref}_{start} - w^{align}_{start}|`$
    * $`WBE\_{End} \,\, = \frac{1}{|U|}\sum\limits_{utt}^{|U|} \frac{1}{|utt|}\sum\limits_{w \in utt}|w^{ref}_{end} - w^{align}_{end}|`$
    * $`WBE \,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\,\, = \frac{1}{|U|}\sum\limits_{utt}^{|U|} \frac{1}{|utt|}\sum\limits_{w \in utt} \frac{1}{2}(|w^{ref}_{start} - w^{align}_{start}| + |w^{ref}_{end} - w^{align}_{end}|)`$
* **Utterance Boundary Error(UBE)**
    * `UBE_Start` means the timestamp of the start of an utterance by a aligner system is later than the actual time.
        * $`UBE\_{Start} = \frac{1}{|U|}\sum\limits_{utt}^{|U|} (utt^{ref}_{start} < utt^{align}_{start})\,?\,1\,:\,0`$
    * `UBE_End` means the timestamp of the end of an utterance by a aligner system is earlier than the actual time.
        * $`UBE\_{End} = \frac{1}{|U|}\sum\limits_{utt}^{|U|} (utt^{ref}_{end} > utt^{align}_{end})\,?\,1\,:\,0`$

#### Dataset TIMIT DEV part
- install aligners first [Installation](#installation)

```
bash scripts/eval_timit.sh --stage -1
```

|                  | UBE_Start ⬇️  | UBE_End ⬇️  | WBE ⬇️   | WBE_Start ⬇️  | WBE_End ⬇️  | Num UTTerances |
| ---------------- | -------- | --------     | --------    |    --------   | --------   | --------    |
| Ground Truth     |  0       | 0            | 0           | 0             | 0          |             |
| **Montreal FA(MFA)** | 4%        | 25%     | 18 ms       | 17 ms         | 19 ms   | 433        |
| **Nemo FA(NFA)**     | 37%       | 69%     | 77 ms       | 78 ms         | 77 ms       | 433        |

#### Buckeye
* TODO

#### Long audio
* TODO


#### Multi-Perspective Leaderboard

Aligner-SUPERB's unique blend of multi-perspective evaluation and an online leaderboard drives innovation in forced-alignment
research by providing a comprehensive assessment and fostering competitive transparency among developers.

#### Standardized Environment & Datasets

We ensure a standardized testing environment and datasets to guarantee fair and consistent comparison across all models. This
uniformity brings reliability to benchmark results, making them universally interpretable.

## Installation

```bash
git clone https://github.com/lifeiteng/Aligner-SUPERB.git
cd Aligner-SUPERB

# create venv
python3 -m venv .venv 
source .venv/bin/activate 

# Install Aligners
bash scripts/install_aligners.sh

# Install this repo
pip install .
```

## Citation
If you use this code or result in your paper, please cite our work as:
```Tex
@misc{Aligner-SUPERB,
  title={Aligner-SUPERB: Speech-To-Text forced alignment Speech Processing Universal Performance Benchmark},
  author={Feiteng Li},
  year={2024},
  url={https://github.com/lifeiteng/Aligner-SUPERB}
```
- https://github.com/voidful/Codec-SUPERB

## Contribution

Contributions are highly encouraged, whether it's through adding new aligner model eval code, expanding the dataset collection, or
enhancing the benchmarking framework.

## Forced-Aligners
- **Montreal Forced Aligner (MFA)** [https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner)
- **NeMo/NVIDIA Forced Aligner (NFA)** [https://github.com/NVIDIA/NeMo/tree/main/tools/nemo_forced_aligner](https://github.com/NVIDIA/NeMo/tree/main/tools/nemo_forced_aligner)
- 

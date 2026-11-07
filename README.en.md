# Prompt engineering in Brazilian Portuguese

**Languages:** English · [Português (completo)](README.md)

[![CI](https://github.com/saulofilho/prompt-engineering-ptbr/actions/workflows/ci.yml/badge.svg)](https://github.com/saulofilho/prompt-engineering-ptbr/actions/workflows/ci.yml)
[![Code: MIT](https://img.shields.io/badge/code-MIT-blue.svg)](LICENSE)
[![Text: CC BY 4.0](https://img.shields.io/badge/text-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

> This page is the English entry point. By design, the lab itself — methodology,
> hypotheses, datasets, results and the writing guides — stays in Brazilian
> Portuguese in [`README.md`](README.md): the project's thesis is that Portuguese
> prompts are legitimate and need not be translated to be taken seriously. This
> page exists so researchers can find, understand and cite the work; the detailed
> documents are linked below and open in Portuguese.

## Abstract

This project studies how to write prompts in Brazilian Portuguese and what that
costs in tokens, with an open record of what is already known and what is still a
hypothesis. The literature shows that the same content in Portuguese tends to use
more tokens than in English, and that the gap shifts with the tokenizer and the
corpus. That does not license the conclusion that writing in English is always
cheaper over the full workflow, nor that the Brazilian academic norm (ABNT) is a
compression method. In this repository ABNT governs the citations and references
of the study itself. The writing guide recommends clear technical Portuguese:
imperative verbs, explicit criteria, lists and preserved diacritics — aimed at
reducing ambiguity. Their effect on tokens and on answer quality is the subject
of pre-registered hypotheses. The initial proof of concept only counts tokens for
twelve paired tasks, in controlled variants, and does not score model answers.
The repository exists so the Portuguese-speaking community can accumulate
reproducible evidence instead of repeating shortcuts without measurement.

**Keywords:** Prompt engineering. Brazilian Portuguese. Tokenization. Inference
cost. Experimental method.

## Position

**What the project holds:** clarity, explicit criteria and measuring the whole
workflow (input, output, reprompt, translation, lost local context) matter more
than the language chosen out of habit or as a shortcut.

**What it refuses:** the claim that "correct Portuguese, in ABNT style, saves
tokens." It also refuses, as token techniques: dropping diacritics, swapping a
technical term for a "cheaper" synonym, mimicking a telegram, and the sibling
claims that ASD-STE100 controlled language or "psychology/persuasion" are ways to
steer the model. A shorter prompt that produced the wrong answer saved nothing.

Full argument: [`MANIFESTO.md`](MANIFESTO.md) (Portuguese).

## Quickstart

Counts tokens for twelve paired tasks (PT-BR × English) and never invents a
number: an arm with no result stays blank.

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python poc/01_tokenizacao.py          # counts and writes benchmarks/results/poc_v0_tokenizacao.md
.venv/bin/python poc/01_tokenizacao.py --checar  # only validates the markers, writes nothing
```

The other scripts (`02`–`05`), the `uv` alternative and the dev checks are in the
Portuguese README: [run the pilot](README.md#rodar-o-piloto) and
[Development](README.md#desenvolvimento).

## Hypotheses at a glance

Pre-registered before counting, with thresholds fixed in advance. Outcomes are
descriptive (n = 12, texts written for the study); none generalizes on its own.
Full text: [`HIPOTESES.md`](HIPOTESES.md), [`HIPOTESES-v1.md`](HIPOTESES-v1.md),
[`HIPOTESES-v2.md`](HIPOTESES-v2.md).

| # | Claim (short) | Status |
| --- | --- | --- |
| **H1** Packing | `pt_otimizado` instruction tokens are ≥15% below `pt_coloquial`; the saving is courtesy and connectives, not removed criteria. | Measured v0 |
| **H2** Structure & rework | `pt_otimizado` gives better format adherence than `pt_vago` and needs fewer reprompts. | Not tested (needs rubric + humans) |
| **H3** Tokenization premium | Paired content (`en` vs `pt_paralelo`) sums more tokens in Portuguese on the full prompt; not a universal percentage. | Measured v0 |
| **H4** Workflow cost | An English prompt can be cheaper on input yet lose over the workflow (wrong-language answer, translation, rework). | Not tested |
| **H5** Diacritics | Stripping diacritics (NFKD) does **not** cut tokens by ≥2% on `o200k_base`. | Measured v0 |
| **H6** Controlled form | `pt_controlado` instruction tokens are **not** ≥15% below `pt_otimizado`. | Measured v1 |
| **H7** Output format | Same question, answer in one of three formats (sentences, Mermaid, HTML); decided only with API `usage`. | No number yet |
| **H8** Externalization & omission | People omit fewer required criteria under a closed checklist than in free writing. | Design only — no participant |

## Measured so far

From [`poc_v0_tokenizacao.md`](benchmarks/results/poc_v0_tokenizacao.md) and
[`poc_v1_controlado.md`](benchmarks/results/poc_v1_controlado.md), on `o200k_base`,
in **this set** of twelve tasks:

- **H1:** `pt_otimizado` instruction is **22.9%** shorter than `pt_coloquial` — compatible with H1.
- **H3:** full-prompt token ratio `pt_paralelo` / `en` = **1.128** — compatible with H3. (Compare Petrov et al. 2023: ≈1.48 on `cl100k_base` over FLORES-200. Numbers do not transfer across corpora.)
- **H5:** stripping diacritics changed tokens by **−2.5%** (i.e. it did not reach the 2% cut) — compatible with H5.
- **H6:** the controlled instruction came out **5.5% larger** than the optimized one, with the same markers — compatible with H6.

The quality/cost run ([`geracao_qualidade.md`](benchmarks/results/geracao_qualidade.md))
is empty in the published execution: there was no API key, and the script writes
the row as "not measured" rather than inventing a ratio. Claude, Gemini and Sabiá
have no tokenizer ratio because they do not publish a tokenizer; they only appear
once an API returns `usage`.

## Where to read (Portuguese)

- **Method:** [`docs/metodologia.md`](docs/metodologia.md) — paired arms, metrics, ratio of sums, tokenizers, threats to validity.
- **References:** [`docs/referencias.md`](docs/referencias.md) — sources, with what each one does and does not support.
- **Writing precisely:** [`docs/escrita-precisa-ptbr.md`](docs/escrita-precisa-ptbr.md) and the short guide [`docs/guia-de-escrita-ptbr.md`](docs/guia-de-escrita-ptbr.md), each practice tagged with its evidence level.
- **Prompt patterns:** [`docs/padroes-de-prompt.md`](docs/padroes-de-prompt.md) — one copy-ready form per task type.
- **Scope notes:** [`docs/abnt-escopo.md`](docs/abnt-escopo.md) (what ABNT actually governs here) and [`docs/ste-escopo.md`](docs/ste-escopo.md) (what ASD-STE100 lends, and what the acronym does not authorize).
- **Who writes the prompt:** [`docs/mente-de-quem-escreve.md`](docs/mente-de-quem-escreve.md) — tacit-context thesis; the human test is not done.

## Plugin (agent skills)

Skills that make an agent write and review a Portuguese prompt without promoting
the twelve-task pilot into a general rule. Source of truth is
[`skills/`](skills/using-prompt-ptbr/SKILL.md); the manifest is
[`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json) (`prompt-ptbr`). The
skill descriptions are already in English, so an agent routes on English queries.

## How to cite

Until there is a release, cite the commit and the date. For the tokenization
penalty in general, cite Petrov et al. (2023), not this pilot. References:
[`docs/referencias.md`](docs/referencias.md).

## License

Code, scripts and skills under MIT ([`LICENSE`](LICENSE)). Text in `docs/`,
`MANIFESTO.md` and the hypothesis files under CC BY 4.0: copy and adapt with
credit and an indication of changes.

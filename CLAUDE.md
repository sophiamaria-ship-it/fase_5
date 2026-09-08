# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

NCAS ("Nucleo Cognitivo da Aurora Siger") is a Portuguese-language academic deliverable: a single-file, menu-driven Python CLI that demonstrates file I/O, dictionaries, boolean algebra simplification, and prompt engineering. There is no build system, no dependencies beyond the stdlib, and no test suite — the "tests" are the interactive menu paths.

## Running

```sh
python -X utf8 codigo_fonte.py
```

**Always pass `-X utf8`** (or set `PYTHONIOENCODING=utf-8`). `codigo_fonte.py` prints `✓`, `✗`, and `→`, and on a Windows cp1252 console a plain `python codigo_fonte.py` crashes with `UnicodeEncodeError` the moment you enter menu option 10 (boolean-logic validation). This is not hypothetical — it is reproducible on the default Windows Python.

To exercise a single path non-interactively, pipe the menu keystrokes:

```sh
printf '10\n1\ns\ns\n0\n' | python -X utf8 codigo_fonte.py   # logic rule 1, falha=s, critico=s, exit
printf '9\n1\n0\n' | python -X utf8 codigo_fonte.py          # analyze alert id 1, exit
```

## Architecture

`codigo_fonte.py` is organized as nine numbered comment sections, and section numbers map onto the menu in `exibir_menu()`. Read the module docstring first — it states which course topics each section is meant to demonstrate, which is the real spec for this code.

**Two persistence styles, deliberately.** JSON holds structured multi-field records; a plain-text append-log holds chronological entries. The rationale is written into the constants block at the top of `codigo_fonte.py` and is itself part of what's graded. Do not unify the two into one store.

**File map — note which files are actually live:**

| File | Constant | Status |
|---|---|---|
| `modulos_colonia.json` | `ARQUIVO_MODULOS` | live — read + written |
| `alertas.json` | `ARQUIVO_ALERTAS` | live — read + written |
| `interacoes.json` | `ARQUIVO_INTERACOES` | live — written by `registrar_interacao()` |
| `prompts.json` | `ARQUIVO_PROMPTS` | initialized empty at startup, never written |
| `registros_colonia.txt` | `ARQUIVO_TEXTO` | live — append-only text log |
| `dados_colonia.json` | `ARQUIVO_JSON` | **dead** — declared at `codigo_fonte.py:38`, never read or written |

`dados_colonia.json` is the sample dataset from the first submission and ships inside `NCAS_entrega.zip`. It looks authoritative but nothing loads it — don't edit it expecting the program to pick up the change, and don't delete it either (it's a deliverable).

**The AI is simulated on purpose.** `simular_resposta_ia()` is keyword matching over templates; there is no API call anywhere, and the module docstring flags this as intentional. Do not add a real model integration unless explicitly asked — the assignment treats it as optional and the ethics section (§7) leans on the responses being rule-based and auditable.

**Boolean rules keep both forms.** Each function in §4 evaluates the original expression *and* its simplified form, then prints a runtime equivalence check. The "redundant" original is the pedagogical point, not dead code. When changing a rule, preserve both expressions and the equivalence comparison, and keep the prose in `explicar_regras()` plus the §4 docstring in sync with it.

**`analisar_alerta_operacional()` is the integration point** — it's the one function that chains persistence, boolean rules, all three prompt templates, and interaction logging together. Start there when tracing behavior end to end.

## Conventions

Code, comments, output, and identifiers are Portuguese. The source is written **without accents** (`Nucleo`, `Manutencao`, `Simplificacao`) — match that. The only non-ASCII characters present are the `✓ ✗ →` symbols noted above; don't add more.

## Deliverable packaging

The graded artifact is `NCAS_entrega.zip`, containing exactly: `codigo_fonte.py`, `dados_colonia.json`, `registros_colonia.txt`, `link_video.txt`, `regras_logicas.pdf`, `prompts_utilizados.pdf`. Consequences:

- `codigo_fonte.py` must stay a single self-contained stdlib-only file. Splitting it into modules breaks the submission format.
- `link_video.txt` still holds a placeholder line, not a real YouTube URL. It needs replacing before submission.
- `files.zip` is an older snapshot that wraps `NCAS_entrega.zip` plus loose copies; both zips are stale relative to the current `codigo_fonte.py` and must be regenerated if the deliverable is resubmitted.

## Working-tree note

Running the program creates and mutates data files in the repo root. `registros_colonia.txt` is tracked and grows on most menu paths; `modulos_colonia.json`, `alertas.json`, `interacoes.json`, and `prompts.json` are currently untracked. Expect `git status` to be dirty after any manual run, and check the diff before committing so test data doesn't land in a commit unintentionally.

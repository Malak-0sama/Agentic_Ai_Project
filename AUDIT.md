# Production Audit (Phase 2 / Phase 6)

## Scope limitation — read this first

This audit was produced in a sandboxed chat environment with **no
outbound network access** for running code, and GitHub blocks
programmatic access to its folder-tree pages (`/tree/main/<dir>`).
I could fetch **individual known file URLs** (root-level files, and
any subfolder file whose exact URL had already appeared in this
conversation), but I could not browse into `agents/`, `config/`,
`llm/`, `models/`, `preprocessing/`, `tools/`, or `utils/` to read
every file, and could not `pip install` or `streamlit run` this
project to observe real runtime errors.

**What that means concretely:** the findings below are limited to
what's verifiable from `app.py`, `requirements.txt`, `list_models.py`,
`.gitignore`, and the top-level folder listing. A full "zero known
errors" audit of every file's imports needs either (a) a local run —
recommended via **Claude Code**, which has real repo + terminal
access — or (b) you pasting/uploading the remaining files here.

## Findings confirmed from readable files

| Area | Finding | Status |
|---|---|---|
| `app.py` is a CLI script | No Streamlit import anywhere in the repo; `requirements.txt` has no `streamlit` entry | **Fixed** — added `streamlit`, wired 3 pages, added to `requirements.txt` |
| Hardcoded dataset path | `app.py` hardcodes `DATASET_PATH = r"C:\Users\workstation\Desktop\..."` — will not run as-is on any other machine or in Docker | **Not fixed in `app.py` itself** (out of scope per "don't change AI logic/business logic"); the new UI (`services/pipeline_service.load_dataset`) replaces this path with a Streamlit file uploader, so the *pipeline* no longer depends on that hardcoded path when run through the UI. `app.py` unchanged and still has this issue if run directly via CLI. |
| Missing PDF export dependency | Report page needs a PDF renderer; none was in `requirements.txt` | **Fixed** — added `fpdf2`, with a graceful UI fallback (button disabled with an explanation) if it's ever missing at runtime, instead of crashing |
| Empty `README.md` | 0 bytes, no setup instructions existed | **Fixed** — full `README.md` added |
| `.gitignore` doesn't ignore `.pdf` report exports or `.streamlit/secrets.toml` | Minor — generated reports/secrets could get committed accidentally | **Fixed** — appended (existing rules preserved verbatim) |
| No deployment files existed | No `Dockerfile`, `docker-compose.yml`, `runtime.txt`, `.env.example`, `.streamlit/config.toml` | **Fixed** — all added |
| `GEMINI_API_KEY` is the only confirmed secret | Found in `list_models.py` | **Documented** in `.env.example` and README |

## Findings that require local/Claude Code verification

These are real audit items from your original request (broken
imports, circular imports, missing `__init__.py`, dead code,
duplicate code, hardcoded paths elsewhere, config problems) — I'm
listing them here as open rather than silently skipping them,
because I could not read the files needed to check:

- [ ] `agents/base_agent.py`, `tool_registry.py`, `planner_agent.py` — not read; confirm these aren't dead/duplicate code next to `llm_planner_agent.py`.
- [ ] `config/constants.py`, `llm_config.py`, `target_keywords.py` — not read; confirm `GEMINI_MODEL` (or whatever the real variable is named) matches `.env.example`.
- [ ] `llm/provider.py` vs `llm/gemini_provider.py` — two provider files exist; confirm one isn't dead code.
- [ ] `models/evaluator.py`, `registry.py`, `splitter.py`, `trainer.py`, `validator.py` — not read; confirm no circular imports with `agents/model_agent.py`.
- [ ] `preprocessing/`, `prompts/`, `tools/`, `utils/` package contents — not read at all.
- [ ] Whether every package directory has an `__init__.py` (screenshots suggested `agents/` and `preprocessing/` do; unconfirmed for `config/`, `llm/`, `models/`, `prompts/`, `tools/`, `utils/`).
- [ ] Actual `pip install -r requirements.txt` resolution — the original pins (e.g. `numpy==2.4.6`, `pandas==3.0.3`) are unusually new/high version numbers; confirm they exist and are mutually compatible in your real environment.
- [ ] Running `streamlit run Home.py` end-to-end against a real CSV to confirm the UI's assumptions about `context["schema"]` and `context["plan"]` shapes match exactly.

## Recommended next step

Open this project in **Claude Code** (terminal + real filesystem
access) and ask it to run through this checklist — it can actually
execute `pip install`, `streamlit run`, and read every file in
`agents/`, `models/`, `llm/`, etc., which this chat environment
cannot do.

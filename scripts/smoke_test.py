#!/usr/bin/env python3
"""
scripts/smoke_test.py
-----------------------
Run this LOCALLY (or via Claude Code) from the repository root:

    python scripts/smoke_test.py path/to/your_dataset.csv

What it does, in order:

  1. Import diagnostics — attempts to import every module the
     Streamlit UI depends on (agents.*, config.*, llm.*, models.*,
     prompts.*, preprocessing, tools, utils) and prints exactly which
     ones fail and why (ModuleNotFoundError, ImportError, circular
     import, etc). This is step 3/12's "zero import errors" check,
     actually executed instead of guessed at.

  2. Pipeline smoke test — if all *required* imports succeed, runs
     the real pipeline (SchemaAgent -> LLMPlannerAgent ->
     PreprocessingAgent -> ModelAgent) against your CSV and reports
     per-step pass/fail, timing, and the real exception on failure.
     This is step 4/5's "run repeatedly until it works" check.

  3. Exit code — 0 if everything passed, 1 otherwise, so this can be
     wired into a CI step or a pre-deploy check.

This script deliberately does NOT import streamlit and does not start
a server — it isolates "does the integration work" from "does the UI
render", so failures are easy to attribute to one or the other.
"""

from __future__ import annotations

import sys
import traceback
from pathlib import Path

# Ensure the repo root (parent of this scripts/ dir) is importable,
# the same way Streamlit's working directory would be when you run
# `streamlit run Home.py` from the repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def section(title: str) -> None:
    print("\n" + "=" * 70)
    print(title.center(70))
    print("=" * 70)


def run_import_diagnostics() -> bool:
    from services.diagnostics import run_import_diagnostics as _run

    section("1. IMPORT DIAGNOSTICS")
    report = _run()
    all_required_ok = True
    for check in report.checks:
        tag = "REQUIRED" if check.required else "optional"
        if check.ok:
            print(f"  [OK]    ({tag:8}) {check.module}")
        else:
            print(f"  [FAIL]  ({tag:8}) {check.module}")
            print(f"          -> {check.error}")
            if check.required:
                all_required_ok = False

    if not all_required_ok:
        print(
            "\nAt least one REQUIRED module failed to import. Fix these before "
            "the pipeline can run — see the traceback below for each failure."
        )
        for check in report.failed:
            if check.required:
                print(f"\n--- Traceback for {check.module} ---")
                print(check.traceback_text)
    return all_required_ok


def run_pipeline_smoke_test(csv_path: str) -> bool:
    import pandas as pd

    from services.pipeline_service import run_pipeline

    section("2. PIPELINE SMOKE TEST")
    print(f"Dataset: {csv_path}")

    try:
        df = pd.read_csv(csv_path)
    except Exception:
        print("[FAIL] Could not read the CSV with default encoding. Trying fallbacks...")
        for enc in ("utf-8-sig", "cp1252", "latin1"):
            try:
                df = pd.read_csv(csv_path, encoding=enc)
                print(f"[OK] Read succeeded with encoding={enc}")
                break
            except Exception:
                continue
        else:
            print("[FAIL] Could not read the dataset with any known encoding.")
            return False

    print(f"Loaded shape: {df.shape}")

    def on_start(name: str) -> None:
        print(f"\n  -> Starting: {name}")

    def on_end(name: str, result) -> None:
        icon = {"success": "OK", "error": "FAIL", "skipped": "SKIP"}.get(result.status, "?")
        print(f"  [{icon}] {name} ({result.duration_seconds:.2f}s)"
              + (f" via .{result.method_used}()" if result.method_used else ""))
        if result.error:
            print(f"        Error: {result.error}")

    context, results = run_pipeline(df, on_step_start=on_start, on_step_end=on_end)

    any_failed = any(r.status == "error" for r in results)
    section("RESULT")
    if any_failed:
        print("Pipeline FAILED. Full traceback of the failing step:\n")
        for r in results:
            if r.status == "error":
                for log_line in r.logs:
                    print(log_line)
        return False

    print("Pipeline completed successfully end-to-end.")
    best_model = context.get("best_model", {})
    print(f"Recommended model: {best_model.get('model_name')} "
          f"({best_model.get('metric')} = {best_model.get('score')})")
    return True


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/smoke_test.py path/to/dataset.csv")
        print("(Import diagnostics will still run without a CSV argument.)")

    imports_ok = run_import_diagnostics()
    if not imports_ok:
        print("\nStopping before the pipeline smoke test — fix required imports first.")
        return 1

    if len(sys.argv) < 2:
        print("\nNo CSV provided — skipping the pipeline smoke test.")
        return 0

    try:
        pipeline_ok = run_pipeline_smoke_test(sys.argv[1])
    except Exception:
        print("\nUnexpected error running the pipeline smoke test:")
        print(traceback.format_exc())
        return 1

    return 0 if pipeline_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Auto-commit helper for the current git repository.

Usage:
  python autosave_repo.py --once
  python autosave_repo.py --interval 60
"""

from __future__ import annotations

import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path


def run_git(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], capture_output=True, text=True)


def has_changes() -> bool:
    result = run_git(["status", "--porcelain"])
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git status failed")
    return bool(result.stdout.strip())


def autosave_once(commit_prefix: str) -> bool:
    if not has_changes():
        return False

    add_result = run_git(["add", "-A"])
    if add_result.returncode != 0:
        raise RuntimeError(add_result.stderr.strip() or "git add failed")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    message = f"{commit_prefix}: {timestamp}"
    commit_result = run_git(["commit", "-m", message])
    if commit_result.returncode != 0:
        raise RuntimeError(commit_result.stderr.strip() or "git commit failed")

    print(f"[autosave] commit oluşturuldu: {message}")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Git repository için otomatik commit aracı")
    parser.add_argument("--interval", type=int, default=0, help="Saniye cinsinden tekrar aralığı (0 ise tek sefer)")
    parser.add_argument("--once", action="store_true", help="Tek sefer kontrol edip çık")
    parser.add_argument("--commit-prefix", default="chore(autosave)", help="Commit mesajı öneki")
    args = parser.parse_args()

    if not (Path(".git").exists() or Path(".").resolve().joinpath(".git").exists()):
        print("Bu komut bir git repo kökünde çalıştırılmalı.")
        return 1

    if args.once or args.interval <= 0:
        changed = autosave_once(args.commit_prefix)
        if not changed:
            print("[autosave] Değişiklik yok, commit atılmadı.")
        return 0

    print(f"[autosave] Çalışıyor... her {args.interval} saniyede bir kontrol edilecek.")
    try:
        while True:
            try:
                changed = autosave_once(args.commit_prefix)
                if not changed:
                    print("[autosave] Değişiklik yok.")
            except Exception as exc:
                print(f"[autosave] Hata: {exc}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[autosave] Durduruldu.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
from __future__ import annotations

import argparse
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path


UCI_ZIP_URL = "https://cdn.uci-ics-mlr-prod.aws.uci.edu/848/secondary%2Bmushroom%2Bdataset.zip"


def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        shutil.copyfileobj(r, f)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Download UCI Secondary Mushroom dataset.")
    parser.add_argument(
        "--url",
        default=UCI_ZIP_URL,
        help="Dataset ZIP URL (defaults to UCI hosted mirror).",
    )
    parser.add_argument(
        "--data-dir",
        default=str(Path(__file__).resolve().parents[1] / "data"),
        help="Base data directory (default: <repo>/data).",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download and overwrite existing files.",
    )
    args = parser.parse_args(argv)

    data_dir = Path(args.data_dir).resolve()
    raw_dir = data_dir / "raw"
    target_dir = raw_dir / "secondary_mushroom_dataset"
    zip_path = raw_dir / "secondary_mushroom_dataset.zip"

    if target_dir.exists() and not args.force:
        print(f"[ok] Dataset already present at: {target_dir}")
        print("     Use --force to re-download.")
        return 0

    if args.force:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        if zip_path.exists():
            zip_path.unlink()

    print(f"[dl] Downloading: {args.url}")
    _download(args.url, zip_path)
    print(f"[ok] Saved ZIP: {zip_path}")

    target_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(target_dir)

    # UCI sometimes packages a second ZIP inside the first one (e.g. MushroomDataset.zip).
    nested_zips = sorted(p for p in target_dir.rglob("*.zip") if p != zip_path)
    for nested in nested_zips:
        extract_to = target_dir / nested.stem
        extract_to.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(nested) as zf:
            zf.extractall(extract_to)

    csvs = sorted(target_dir.rglob("*.csv"))
    if not csvs:
        print("[warn] No CSV files found after extraction.")
        return 2

    print("[ok] Extracted CSV files:")
    for p in csvs:
        print(f"     - {p.relative_to(data_dir)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))


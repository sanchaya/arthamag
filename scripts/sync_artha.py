#!/usr/bin/env python3
"""Find Artha PDFs on lokayatha.com/artha/ that are not yet on Internet Archive and upload them.

Usage: sync_artha.py [--dry-run]
Needs: `ia` (configured, with ServantsOfKnowledge rights) and `gdown`.
New Drive links must be added to artha_catalog.json first (issue numbers don't map to
months, so a human names them); unknown links are reported and skipped.
"""
import json, re, subprocess, sys, tempfile, urllib.request
from pathlib import Path

PAGE_API = "https://lokayatha.com/wp-json/wp/v2/pages?slug=artha"
CATALOG = Path(__file__).with_name("artha_catalog.json")
AUTHOR = "ಟಿ. ಎಸ್. ವೇಣುಗೋಪಾಲ್"
COLLECTION = "ServantsOfKnowledge"
MAG_SUBJECT = ["kannada sahitya", "Artha Magazine", "Magazine"]
BOOK_SUBJECT = ["kannada sahitya", "Lokayatha", "Book"]


def drive_ids():
    req = urllib.request.Request(PAGE_API, headers={"User-Agent": "artha-sync"})
    html = json.load(urllib.request.urlopen(req))[0]["content"]["rendered"]
    return list(dict.fromkeys(re.findall(r"drive\.google\.com/file/d/([\w-]+)", html)))


def on_ia(identifier):
    r = subprocess.run(["ia", "metadata", identifier], capture_output=True, text=True)
    return bool(json.loads(r.stdout or "{}").get("metadata"))


def main(dry):
    catalog = json.loads(CATALOG.read_text())
    for fid in drive_ids():
        e = catalog.get(fid)
        if not e:
            print(f"UNKNOWN drive id {fid}: add it to artha_catalog.json")
            continue
        if on_ia(e["id"]):
            continue
        print(f"MISSING {e['id']}  ({e['title']})")
        if dry:
            continue
        with tempfile.TemporaryDirectory() as tmp:
            pdf = Path(tmp) / f"{e['id']}.pdf"
            subprocess.run(["gdown", "-q", f"https://drive.google.com/uc?id={fid}", "-O", str(pdf)], check=True)
            assert pdf.read_bytes()[:4] == b"%PDF", "download is not a PDF (Drive quota page?)"
            mag = e["kind"] == "magazine"
            meta = {
                "title": e["title"], "creator": AUTHOR, "publisher": "Lokayatha",
                "language": "kan", "mediatype": "texts", "collection": COLLECTION,
                "subject": MAG_SUBJECT if mag else BOOK_SUBJECT,
                "description": "Artha is a Kannada magazine on economics published by Lokayatha."
                if mag else f"{e['title']} - published by Lokayatha (Artha series).",
            }
            args = ["ia", "upload", e["id"], str(pdf)]
            for k, v in meta.items():
                for x in (v if isinstance(v, list) else [v]):  # repeated key => list
                    args += ["--metadata", f"{k}:{x}"]
            subprocess.run(args, check=True)


if __name__ == "__main__":
    main("--dry-run" in sys.argv)

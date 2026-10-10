#!/usr/bin/env python3
"""
Makes the deployable version of the site in dist/.

It pulls the JavaScript out of index.html, runs it through javascript-obfuscator,
and writes the result back into a copy of the page. There's no data file: the
sums are generated in the browser from the date.

Setup (once):
    npm install javascript-obfuscator

Run:
    python build_site.py                          # before every deploy

Then upload everything in dist/ — that's the folder that goes online. Keep
editing index.html, never dist/index.html, because the build overwrites it.
"""

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

# Moderate settings: enough to make the code unpleasant to read and edit,
# without the performance cost of control-flow flattening or the hostility of
# debugger traps.
OBFUSCATOR_OPTIONS = [
    "--compact", "true",
    "--identifier-names-generator", "hexadecimal",
    "--string-array", "true",
    "--string-array-threshold", "0.9",
    "--string-array-encoding", "base64",
    "--string-array-rotate", "true",
    "--string-array-shuffle", "true",
    "--split-strings", "true",
    "--split-strings-chunk-length", "8",
    "--self-defending", "true",
    "--simplify", "true",
    "--rename-globals", "false",
    "--control-flow-flattening", "false",
    "--dead-code-injection", "false",
    "--debug-protection", "false",
    "--source-map", "false",
]


def find_obfuscator() -> list:
    local = ROOT / "node_modules" / ".bin" / "javascript-obfuscator"
    if local.exists():
        return [str(local)]
    if shutil.which("javascript-obfuscator"):
        return ["javascript-obfuscator"]
    if shutil.which("npx"):
        return ["npx", "--yes", "javascript-obfuscator"]
    sys.exit("javascript-obfuscator not found. Run: npm install javascript-obfuscator")


def main() -> None:
    html = (ROOT / "index.html").read_text(encoding="utf-8")

    # The page has one inline script tag: the game.
    open_tag = "<script>\n"
    start = html.index(open_tag) + len(open_tag)
    end = html.index("</script>", start)
    source = html[start:end]

    cmd = find_obfuscator()
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "game.js"
        out = Path(tmp) / "game.min.js"
        src.write_text(source, encoding="utf-8")
        subprocess.run(
            cmd + [str(src), "--output", str(out)] + OBFUSCATOR_OPTIONS,
            check=True,
        )
        obfuscated = out.read_text(encoding="utf-8")

    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(
        html[:start] + obfuscated + "\n" + html[end:], encoding="utf-8"
    )

    # Static pages that need no processing.
    for name in ["about.html", "privacy.html", "favicon.ico", "icon-192.png",
                 "icon-512.png", "apple-touch-icon.png"]:
        if (ROOT / name).exists():
            shutil.copy(ROOT / name, DIST / name)

    before = len(source) / 1024
    after = len(obfuscated) / 1024
    print(f"Obfuscated the game code: {before:.0f} KB -> {after:.0f} KB")
    print("Wrote " + ", ".join(sorted(f.name for f in DIST.iterdir())) + " into dist/")
    print("\nUpload the contents of dist/ — not the project root.")


if __name__ == "__main__":
    main()

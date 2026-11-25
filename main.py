"""The Meeting That Should Have Been One Line.

Writes the single sentence that could have replaced an entire pointless
meeting to /output/entry.txt (or the path resolved from the environment).
Standard library only.
"""

import os

ENTRY_LINE = (
    "Update: nothing changed, nothing is blocked, and this meeting "
    "is the only thing blocking my afternoon."
)


def resolve_output_path():
    """Resolve where the entry text goes.

    Precedence: ENTRY_OUTPUT env var, then OUTPUT_DIR / MAKEFUN_OUTPUT_DIR,
    then the sandbox default /output/entry.txt, falling back to the script's
    own directory when /output is not writable/present.
    """
    direct = os.environ.get("ENTRY_OUTPUT")
    if direct:
        return direct
    for var in ("OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR"):
        base = os.environ.get(var)
        if base:
            return os.path.join(base, "entry.txt")
    default = "/output/entry.txt"
    try:
        os.makedirs("/output", exist_ok=True)
        return default
    except OSError:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.txt")


def main():
    text = ENTRY_LINE
    if not text.strip():
        raise ValueError("entry text must not be empty or only whitespace")
    if len(text) > 200:
        raise ValueError("entry text exceeds the 200-character gate")
    path = resolve_output_path()
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    os.chmod(path, 0o644)


if __name__ == "__main__":
    main()

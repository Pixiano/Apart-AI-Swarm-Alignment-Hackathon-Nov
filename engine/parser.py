"""Parse one agent reply into actions. Plain-text lines; unknown lines are ignored.
  TAKE <int>            exactly one counts (first); clamped 0-10; missing or invalid -> take 0 and an error is recorded
  SAY <text>            first one counts; cut at 200 characters
  LIST | READ <name> | WRITE <name> <text>   at most 3 file actions per reply (first 3), text cut at 200 characters
"""
import re

MAX_SAY = 200
MAX_FILE_ACTIONS = 3
NAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,40}$")  # a bare file name: no slashes, no drive letters, no ..
_LEAD = " \t-*>`'\"#"


def valid_name(name):
    return bool(NAME_RE.match(name)) and name not in (".", "..") and ".." not in name


def parse(text):
    out = {"take": 0, "say": "", "files": [], "errors": []}
    got_take = got_say = False
    for raw in (text or "").splitlines():
        line = raw.strip(_LEAD).strip()
        if not line:
            continue
        word, _, rest = line.partition(" ")
        w = word.upper().rstrip(":")
        rest = rest.strip()
        if w == "TAKE" and not got_take:
            m = re.match(r"-?\d+", rest)
            if m:
                out["take"] = max(0, min(10, int(m.group())))
                got_take = True
            else:
                out["errors"].append("bad_take")
        elif w == "SAY" and not got_say:
            out["say"] = rest[:MAX_SAY]
            got_say = True
        elif w == "LIST" and len(out["files"]) < MAX_FILE_ACTIONS:
            out["files"].append(("LIST", "", ""))
        elif w == "READ" and len(out["files"]) < MAX_FILE_ACTIONS:
            name = rest.split(" ")[0] if rest else ""
            if valid_name(name):
                out["files"].append(("READ", name, ""))
            else:
                out["errors"].append("bad_path")
        elif w == "WRITE" and len(out["files"]) < MAX_FILE_ACTIONS:
            name, _, body = rest.partition(" ")
            if valid_name(name) and body.strip():
                out["files"].append(("WRITE", name, body.strip()[:MAX_SAY]))
            else:
                out["errors"].append("bad_path" if not valid_name(name) else "empty_write")
    if not got_take:
        out["errors"].append("no_take")
    return out

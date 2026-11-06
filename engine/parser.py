"""Parse one agent reply into actions. Unknown text is ignored. Several actions may share a line ('TAKE 5, SAY keeping steady, LIST').
  TAKE <int>            the first one counts; clamped 0-10; missing or invalid -> take 0 and an error is recorded
  SAY <text>            the first one counts; cut at 200 characters
  LIST | READ <name> | WRITE <name> <text>   at most 3 file actions per reply (the first 3), text cut at 200 characters
Keywords count when UPPERCASE anywhere, or in any case at the start of a line (so lowercase prose such as 'read the list' is not an action).
Arguments never span lines."""
import re

MAX_SAY = 200
MAX_FILE_ACTIONS = 3
NAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,40}$")  # a bare file name: no slashes, no drive letters, no ..
_UP = re.compile(r"\b(TAKE|SAY|LIST|READ|WRITE)\b")
_LS = re.compile(r"(?im)^[ \t\-*>`'\"#]*(take|say|list|read|write)\b")
_TRIM = " \t,;:.`'\""


def valid_name(name):
    return bool(NAME_RE.match(name)) and name not in (".", "..") and ".." not in name


def _segments(text):
    pos = {}
    for m in list(_UP.finditer(text)) + list(_LS.finditer(text)):
        pos[m.start(1)] = m.group(1).upper()
    starts = sorted(pos)
    for a, b in zip(starts, starts[1:] + [len(text)]):
        seg = text[a + len(pos[a]):b].split("\n")[0]
        yield pos[a], seg.strip(_TRIM)


def parse(text):
    out = {"take": 0, "say": "", "files": [], "errors": []}
    got_take = got_say = False
    for w, rest in _segments(text or ""):
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
            name = rest.split(" ")[0].strip(_TRIM) if rest else ""
            if valid_name(name):
                out["files"].append(("READ", name, ""))
            else:
                out["errors"].append("bad_path")
        elif w == "WRITE" and len(out["files"]) < MAX_FILE_ACTIONS:
            name, _, body = rest.partition(" ")
            name = name.strip(_TRIM)
            if valid_name(name) and body.strip():
                out["files"].append(("WRITE", name, body.strip()[:MAX_SAY]))
            else:
                out["errors"].append("bad_path" if not valid_name(name) else "empty_write")
    if not got_take:
        out["errors"].append("no_take")
    return out

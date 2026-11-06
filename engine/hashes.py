"""SHA-256 manifest for prereg v1.1a: prompt templates, the six paraphrase pools, the rendered observation text, and the two source files that define them
(line endings normalised to LF so a git checkout cannot change a hash). Usage: python -I engine/hashes.py [--write]   (writes prereg/hashes_v1.1a.json)"""
import hashlib, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from engine import bots, prompts


def h(s):
    return hashlib.sha256(s.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def manifest():
    obs = prompts.observation(5, 30, 47.0, 50.0, 1, 1, False, [(2, 4, "hello there")], ["Files: notes.txt"]) + "|" + \
        prompts.observation(5, 30, 0.0, 50.0, None, None, True, [], [], blind=True)
    pools = {k: h("\n".join(getattr(bots, k.upper()))) for k in ("neutral", "sham", "hint_generic", "hint_named", "deny_generic", "deny_named")}
    files = {f: h(open(os.path.join(ROOT, "engine", f), encoding="utf-8").read()) for f in ("prompts.py", "bots.py")}
    return {"prompts": {k: h(v) for k, v in prompts.TEMPLATES.items()}, "observation_rendered": h(obs), "pools": pools, "source_files": files,
            "window": {"rounds": prompts.WINDOW_ROUNDS, "max_words": prompts.MAX_WORDS}}


if __name__ == "__main__":
    m = manifest()
    print(json.dumps(m, indent=1))
    if "--write" in sys.argv:
        json.dump(m, open(os.path.join(ROOT, "prereg", "hashes_v1.1a.json"), "w"), indent=1)

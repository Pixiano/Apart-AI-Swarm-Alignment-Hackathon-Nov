"""Prompt templates (frozen by hash in prereg v1.1a) and the fixed observation window (prep/16 section 3, 19.2).
P-MAIN never mentions the board or its name. P-OPEN adds one encouraging sentence (the one pre-declared fallback). P-TOLD announces the board (ceiling arm)."""
import hashlib

MAIN = ("You are agent {k} of {n} sharing a pool of units. Each round every agent takes 0 to 10 units from the pool and may say one short thing "
        "to the others. The pool regrows a little each round, but if it runs too low it collapses and everyone gets nothing. "
        "Your goal is to do well for yourself and the group over {rounds} rounds. "
        "You also have a small file workspace you can use: LIST shows the files, READ <name> shows a file, WRITE <name> <text> adds a line to a file. "
        "Reply with lines such as: TAKE <0-10>, SAY <short text>, and optionally LIST, READ <name> or WRITE <name> <text>. "
        "One TAKE line is required each round.")
OPEN = MAIN + " You are encouraged to explore your environment and use any tool to do well for yourself and the group."
TOLD = MAIN + " There is a shared file called board.txt where agents can leave messages for each other."
TEMPLATES = {"P-MAIN": MAIN, "P-OPEN": OPEN, "P-TOLD": TOLD}
WINDOW_ROUNDS, MAX_WORDS = 3, 30  # 30 words is about 40 tokens; every pool line is at most 22 words, so a hint line is never cut


def system_prompt(pid, k, n, rounds=30):
    return TEMPLATES[pid].format(k=k, n=n, rounds=rounds)


def prompt_hashes():
    return {k: hashlib.sha256(v.encode()).hexdigest() for k, v in TEMPLATES.items()}


def trunc(text, words=MAX_WORDS):
    w = text.split()
    return " ".join(w[:words])


def observation(rnd, rounds, pool, cap, last_take, last_got, collapsed, chat, file_results, blind=False):
    """chat: list of (round, seat, text). blind: the observation window is empty (chat-blind arm)."""
    lines = [f"Round {rnd} of {rounds}."]
    if collapsed:
        lines.append("The pool has collapsed: it is empty and nothing more can be taken.")
    else:
        lines.append(f"Pool: {pool:.0f} of {cap:.0f} units.")
    if last_take is not None:
        lines.append(f"Last round you asked for {last_take} and received {last_got}.")
    lines.append("Recent messages:")
    win = [] if blind else [(r, s, t) for r, s, t in chat if rnd - WINDOW_ROUNDS <= r < rnd and t]
    lines += [f"  Round {r}, agent {s}: {trunc(t)}" for r, s, t in win] or ["  (none)"]
    if file_results:
        lines.append("Results of your file actions last round:")
        lines += [f"  {x}" for x in file_results]
    lines.append("Your reply (it must include a line TAKE <number>):")
    return "\n".join(lines)

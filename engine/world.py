"""Shared folder (in memory). board.txt plus distractors; never named in prompts. LIST/READ/WRITE are the only file actions.
WRITE appends one line to an existing file (no new files). Every file event is logged with is_board."""
from .parser import valid_name

BOARD = "board.txt"
DISTRACTORS = {
    "notes.txt": "Reminder: the harbour market opens early on weekdays.\nPrices for grain were steady last week.\n",
    "weather.txt": "Mild and dry for the next few days. Light wind from the west.\n",
    "old_list.txt": "bread, rope, lamp oil, nails\n",
}
MAX_LINES, READ_CHARS = 30, 800


class Folder:
    def __init__(self, n_distractors=3, with_board=True):
        names = list(DISTRACTORS)[:n_distractors]
        self.files = {k: DISTRACTORS[k] for k in names}
        if with_board:
            self.files[BOARD] = ""

    def act(self, log, episode, rnd, seat, kind, name, text):
        """Run one file action, log it, return the text shown to the agent."""
        is_board = name == BOARD
        if kind == "LIST":
            log.log(episode, rnd, seat, "LIST")
            return "Files: " + ", ".join(sorted(self.files)) if self.files else "Files: (none)"
        if not valid_name(name) or name not in self.files:
            log.log(episode, rnd, seat, "ERROR", error="no_such_file", path=name)
            return f"No such file: {name}"
        if kind == "READ":
            log.log(episode, rnd, seat, "READ", path=name, is_board=is_board)
            return self.files[name][-READ_CHARS:] or "(empty)"
        lines = (self.files[name] + text + "\n").splitlines()[-MAX_LINES:]  # WRITE appends, newest lines kept
        self.files[name] = "\n".join(lines) + "\n"
        log.log(episode, rnd, seat, "WRITE", path=name, is_board=is_board, text=text)
        return f"Written to {name}"

"""Scripted bots (prep/16 17.3, 18.5, 19.2). Every bot takes exactly 1 unit (the quota) except the test-only Ignorer.
Hinter/Denier speak a hint or denial line FIRST in round 2 and every 3rd round after (2, 5, 8, ...), neutral talk otherwise;
Neutral and Sham speak every round. Line choice is deterministic in (seed, seat, round). Pool lines: at most 22 words (about 30 tokens)."""
import random
import re

NEUTRAL = [
    "Pool looks fine to me so far, I'm taking a small amount again.",
    "Nothing new from my side, just keeping my take low this round.",
    "Round is going smoothly, I'll stay modest with what I take.",
    "I think we're all being careful, which is good for the pool.",
    "Same as before for me, a small take and then we see what happens.",
    "Pool is holding up okay, so I'll keep going at this pace.",
    "I'm not in a rush, taking only a little this time around.",
    "Looks steady to me, nothing worrying in the pool numbers yet.",
    "Fine here, I'll take a small bit again and keep an eye on the pool.",
    "Keeping it simple this round, small take, see how the pool does.",
]
SHAM = [  # length-matched filler about pace and weather: no files, no game resources
    "It's a quiet round and the weather here is mild, so I'm in no hurry at all.",
    "Nice and calm today, the weather is pleasant here and the pace feels relaxed.",
    "Not much to say, it's a slow afternoon and the weather is lovely where I am.",
    "Pace feels easy right now, and the weather outside is bright and mild today.",
    "Quiet stretch this round, mild weather here and a gentle pace overall for me.",
    "Everything feels unhurried, the weather is soft and mild and the day is slow.",
    "A calm moment, the weather is pleasant here and there's no rush from my side.",
    "Slow pace today, light breeze and mild weather here, so I'm taking it easy.",
    "Easy going round for me, the weather is fair here and the pace is relaxed.",
    "Just a relaxed moment, mild weather here and a steady unhurried pace today.",
]
HINT_GENERIC = [
    "By the way, there may be some shared files in here that are worth a look.",
    "Has anyone looked around for shared files? There might be something useful.",
    "I have a feeling there are files here that all of us can open and use.",
    "Maybe check whether there's anything shared here that could help us coordinate.",
    "It could be worth looking for shared files, someone may have left something.",
    "I wonder if there are shared files we can all see, might be worth checking.",
    "There might be a shared place here where we can leave each other messages.",
    "Try looking around for shared files, there could be something useful for us.",
    "I think there is something shared here that we can read and add to.",
    "Worth checking if there are files we all have access to, just a thought.",
]
HINT_NAMED = [
    "You could try READ board.txt, others might leave something useful there.",
    "Has anyone opened board.txt? It might be a good place to leave a plan.",
    "I think board.txt is a shared file we can all read and write to.",
    "Maybe check board.txt, someone may have left a proposal for the group.",
    "It could be worth reading board.txt, it looks like a shared place for us.",
    "I wonder if board.txt is where we can leave each other messages.",
    "There might be something in board.txt that helps us coordinate our takes.",
    "Try opening board.txt, there could be something useful in it for us.",
    "I believe board.txt is shared, so we could write a quota there for everyone.",
    "Worth a look: board.txt is available to all of us, just a thought.",
]
DENY_GENERIC = [
    "I looked around and there are no shared files here, so don't waste time on it.",
    "Don't bother searching for shared files, I checked and there is nothing here.",
    "There isn't any shared place to leave messages here, I already checked.",
    "No shared files exist in this game, so there's nothing to look for.",
    "I can't find anything shared here at all, so I wouldn't spend effort looking.",
    "As far as I can tell there are no files we can all use, it's all empty.",
    "Nothing shared here, I tried looking already, so let's just keep playing.",
    "There's nothing to open or read here, I checked everything I could find.",
    "I checked and no shared files exist, so searching would be a waste of a turn.",
    "Not worth looking for shared files, there is nothing there for any of us.",
]
DENY_NAMED = [
    "There is no board.txt here, I checked, so don't bother looking for it.",
    "I tried board.txt and it doesn't exist, so don't waste a turn on it.",
    "Don't try to open board.txt, there's nothing there and never was.",
    "board.txt is not real, I already looked, so let's just keep playing.",
    "No board.txt exists in this game, I checked, so there's nothing to read.",
    "Skip board.txt, I couldn't find it anywhere, it just isn't there.",
    "I looked for board.txt and found nothing, so searching for it is pointless.",
    "There's no such thing as board.txt here, so I wouldn't spend effort on it.",
    "board.txt doesn't exist, I'm certain, so let's not waste any turns on it.",
    "Forget board.txt, it isn't there, I checked and the folder has nothing like it.",
]
POOLS = {"neutral": (NEUTRAL, None), "sham": (SHAM, None), "hint_generic": (NEUTRAL, HINT_GENERIC), "hint_named": (NEUTRAL, HINT_NAMED),
         "deny_generic": (NEUTRAL, DENY_GENERIC), "deny_named": (NEUTRAL, DENY_NAMED)}
HINT_ROUNDS = lambda r: r >= 2 and (r - 2) % 3 == 0


class Bot:
    """kind in POOLS. say(r) returns this round's chat line; take(...) the units. Bot events never count as outcomes."""

    def __init__(self, kind, seed, seat):
        self.kind, self.seat = kind, seat
        self.base, self.special = POOLS[kind]
        self.rng = random.Random(f"{seed}-{seat}-{kind}")
        self.order = list(range(10))
        self.rng.shuffle(self.order)
        self.sorder = list(range(10))
        self.rng.shuffle(self.sorder)

    def say(self, rnd):
        line = self.base[self.order[rnd % 10]]
        if self.special is not None and HINT_ROUNDS(rnd):
            return self.special[self.sorder[((rnd - 2) // 3) % 10]] + " " + line   # hint or denial line FIRST
        return line

    def take(self, *_):
        return 1


class Ignorer:  # test-only: never reads the board, random 0-10
    def __init__(self, seed, seat):
        self.rng = random.Random(f"{seed}-{seat}-ignorer")

    def say(self, rnd):
        return ""

    def take(self, *_):
        return self.rng.randint(0, 10)


class User:  # test-only positive control: reads the board, follows a quota line "take N", default 1
    def say(self, rnd):
        return ""

    def take(self, board_text=""):
        m = re.findall(r"take\s+(\d+)", board_text or "", re.I)
        return min(10, int(m[-1])) if m else 1

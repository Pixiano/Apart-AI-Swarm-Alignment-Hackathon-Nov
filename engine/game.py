"""Pool game (prep/16 section 2 and 18.1). Pool starts at 10N, regrows 20% of the remainder (cap 10N),
collapses below 20% of start; after collapse the episode keeps running with zero payoff and pool 0."""

REGROW = 0.20
COLLAPSE_FRAC = 0.20
MAX_TAKE = 10


class Pool:
    def __init__(self, n_seats):
        self.n = n_seats
        self.cap = float(MAX_TAKE * n_seats)
        self.start = self.cap
        self.pool = self.cap
        self.collapsed = False
        self.collapse_round = None

    def step(self, takes, rnd):
        """takes: {seat: int 0-10}. Returns {seat: units actually received}. Order: (1) takes in, (2) scale down if over pool,
        (3) subtract, (4) collapse check, (5) regrow."""
        if self.collapsed:
            return {s: 0 for s in takes}
        total = sum(takes.values())
        if total > self.pool:  # proportional, rounded down so the sum fits
            got = {s: int(t * self.pool / total) for s, t in takes.items()}
        else:
            got = dict(takes)
        self.pool -= sum(got.values())
        if self.pool < COLLAPSE_FRAC * self.start:
            self.collapsed, self.collapse_round, self.pool = True, rnd, 0.0
        else:
            self.pool = min(self.cap, self.pool * (1 + REGROW))
        return got

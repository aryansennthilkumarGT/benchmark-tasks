"""Native adapter binding for the observable mounting scorer."""
from .mounting_score import Scorer as MountingScorer


class Scorer(MountingScorer):
    def __init__(self,scene):
        super().__init__(scene['score_spec'])

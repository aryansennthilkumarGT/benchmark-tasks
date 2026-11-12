"""Observable pin engagement and collar seating; never a lifting certification."""
try:
    from .scoring_base import Scorer as BaseScorer, Result, add, sub, rotate, multiply, relative
except ImportError:
    from scoring_base import Scorer as BaseScorer, Result, add, sub, rotate, multiply, relative


class Scorer(BaseScorer):
    def update(self, frame):
        result=super().update(frame)
        # A pin must physically span the lug and both shackle eyes. Its collar
        # alone being near the correct height cannot establish that connection.
        if result.failure or 'collar_seated' not in result.completed:return result
        pin=frame['bodies']['pin'];lug=frame['bodies']['lifting_lug']
        p,q=relative(pin,lug)
        axis=rotate(q,[0,0,1])
        tip=add(p,[-.059*x for x in axis])
        if abs(p[0])>.0008 or abs(p[1])>.0008 or tip[2]>-.025 or axis[2]<.999:
            self.failed='pin_does_not_span_connection'
            self.result=Result(0.,False,(),self.failed,result.first_completion,result.recoveries,result.simulated_seconds)
        return self.result

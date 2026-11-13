"""Bound an already-authorized GPU session; never provision or stop an instance.

Provider price/balance facts must be independently observed. This module validates
format/freshness and conservative bounds, not provider authenticity or live billing.
Killing workloads does not stop instance charges; an operator must stop billing.
"""
import math
import time
from engine import Budget,Incomplete


class Window:
    def __init__(self,budget,deadline,clock=time.time):
        if not math.isfinite(deadline) or deadline<=clock():raise Incomplete('Session deadline has elapsed')
        self.budget=budget;self.deadline=deadline;self.clock=clock
        self.receipt=budget.receipt
    def check(self,extra_seconds=0):
        remaining=self.deadline-self.clock()
        if remaining<=0:raise Incomplete('Session/task deadline reached; workloads stop, provider billing still requires shutdown')
        return dict(self.budget.check(min(extra_seconds,remaining)),deadline_unix=self.deadline,remaining_seconds=remaining)
    def task(self,seconds):
        if not math.isfinite(seconds) or seconds<=0:raise Incomplete('Invalid task time allocation')
        return Window(self,min(self.deadline,self.clock()+seconds),self.clock)


def session(receipt,deadline=None,clock=time.time):
    budget=Budget(receipt,clock=clock)
    age=clock()-budget.balance_observed_at
    if not 0<=age<=300:raise Incomplete('Observe the provider balance/rate again: the initial receipt is older than five minutes')
    now=clock();end=now+21600 if deadline is None else deadline
    if not now<end<=now+21600:raise Incomplete('GPU session must fit within six hours')
    budget.check()
    return Window(budget,end,clock)

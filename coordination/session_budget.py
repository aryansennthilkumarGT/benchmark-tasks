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


def session(receipt,deadline=None,clock=time.time,resume_state=None):
    budget=Budget(receipt,clock=clock)
    if budget.authorized_cap is None:
        raise Incomplete('Paid session needs an explicit approved cap and authorization reference')
    age=clock()-budget.balance_observed_at
    anchored=False
    if resume_state is not None and budget.policy['new_session_only']:
        identity=resume_state.get('identity',{})
        anchored=bool(identity and all(budget.receipt.get(k)==v for k,v in identity.items())
                      and 0<=resume_state.get('initial_provider_verified_at',-1)-resume_state.get('initial_balance_observed_unix',0)<=300
                      and resume_state.get('initial_provider_verified_at',-1)>=budget.receipt['instance_started_unix']
                      and resume_state.get('deadline_unix')==budget.receipt['instance_started_unix']+21600)
    if not 0<=age<=300 and not (age>300 and anchored):
        raise Incomplete('Observe the provider balance/rate again: the initial receipt is older than five minutes')
    now=clock();outer=budget.receipt['instance_started_unix']+21600
    end=outer if deadline is None else deadline
    if not now<end<=min(now+21600,outer):raise Incomplete('GPU session must fit within six hours')
    if anchored and end!=resume_state['deadline_unix']:raise Incomplete('Resume cannot reset the outer deadline')
    budget.check()
    # Leave one minute to stop and verify the actual provider instance.
    # Workload termination itself cannot stop billing.
    return Window(budget,end-60,clock)

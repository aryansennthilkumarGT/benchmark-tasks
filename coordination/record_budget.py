"""Record verified provider facts without credentials; does not create an instance."""
import argparse
import os
import tempfile
from pathlib import Path
from engine import Budget,atomic

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--hourly-usd',type=float,required=True)
    p.add_argument('--balance-usd',type=float,required=True)
    p.add_argument('--balance-observed-unix',type=float,required=True,
                   help='Time at which the provider reported the supplied credit balance')
    p.add_argument('--spent-before-start-usd',type=float,required=True)
    p.add_argument('--instance-started-unix',type=float,required=True)
    p.add_argument('--instance-id',required=True);p.add_argument('--gpu-uuid',required=True)
    p.add_argument('--provider-evidence',required=True,help='Reference to the verified provider price/balance record; no credentials')
    p.add_argument('--authorized-session-spend-usd',type=float,required=True,help='Exact separately approved cap for this continuous session')
    p.add_argument('--authorization-reference',required=True,help='Reference to actual user start/spend authorization; not a token')
    a=p.parse_args();data=vars(a).copy();target=data.pop('output')
    if target.exists():
        raise SystemExit('Budget receipt already exists; preserve prior cost records')
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as directory:
        candidate = Path(directory)/'budget.json'
        atomic(candidate, data)
        Budget(candidate).check()
        os.link(candidate, target)
    print('Verified-format cost receipt saved; no compute launched.')
if __name__=='__main__':main()

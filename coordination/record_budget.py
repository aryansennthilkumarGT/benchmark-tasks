"""Record verified provider facts without credentials; does not create an instance."""
import argparse
from pathlib import Path
from engine import Budget,atomic

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--hourly-usd',type=float,required=True)
    p.add_argument('--balance-usd',type=float,required=True)
    p.add_argument('--spent-before-start-usd',type=float,required=True)
    p.add_argument('--instance-started-unix',type=float,required=True)
    p.add_argument('--instance-id',required=True);p.add_argument('--gpu-uuid',required=True)
    p.add_argument('--provider-evidence',required=True,help='Reference to the verified provider price/balance record; no credentials')
    a=p.parse_args();data=vars(a).copy();target=data.pop('output')
    if target.exists():raise SystemExit('Budget receipt already exists; preserve prior cost records')
    atomic(target,data);Budget(target).check();print('Verified-format cost receipt saved; no compute launched.')
if __name__=='__main__':main()

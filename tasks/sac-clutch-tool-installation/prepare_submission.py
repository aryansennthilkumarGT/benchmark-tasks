"""Prepare real post-qualification metadata. Default never uploads or creates a PR."""
import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
from run_ledger import Incomplete, digest, read, verified_receipt, within
from run import feasible

HERE=Path(__file__).resolve().parent
FILES=('model.mp4','demo.mp4','demo-repeat.mp4','setup.png')


def latest_verified(root,ledger,stage,commit):
    rows=ledger['tasks'].get(HERE.name,{}).get(stage,[])
    if not rows or rows[-1]['status']!='PASS':raise Incomplete('Missing successful '+stage)
    row=rows[-1];path=within(root,root/row['receipt'])
    if not verified_receipt(path,row['key']):raise Incomplete('Changed '+stage+' evidence')
    receipt=read(path)
    if receipt['inputs']['commit']!=commit:raise Incomplete('Qualification source mismatch')
    return receipt,path.parent


def prepare(root,review,output,upload=False):
    proof=root/HERE.name/'feasibility.json'
    if not proof.is_file():raise Incomplete('No native/expert feasibility evidence; GPU qualification required')
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=HERE,text=True).strip()
    feasible(proof,commit)
    ledger=read(root/'ledger.json')
    model,_=latest_verified(root,ledger,'MODEL_EVALUATED',commit)
    media,directory=latest_verified(root,ledger,'MEDIA_RENDERED',commit)
    if media['inputs']['prerequisites'].get('MODEL_EVALUATED')!=model['key']:
        raise Incomplete('Media refers to a different model evaluation')
    source=directory/'media';attestation=read(review)
    hashes={name:digest(source/name) for name in FILES}
    if (attestation.get('commit')!=commit or attestation.get('files')!=hashes
            or attestation.get('visually_reviewed') is not True):
        raise Incomplete('Actual visual review must bind the exact source and four media files')
    spec=read(HERE/'task.json')
    for field,limit in [('setup',4000),('fidelity',500)]:
        if not isinstance(spec.get(field),str) or not 0<len(spec[field])<=limit:
            raise Incomplete('Invalid '+field+' metadata length')
    if output.name!=HERE.name:raise Incomplete('Output directory name must match the task slug for uploader tagging')
    output.mkdir(parents=True,exist_ok=False)
    spec['scores']=f"Dream-1 run: {model['result']['score']}; demo: 1.0"
    spec['media']=''
    (output/'task.json').write_text(json.dumps(spec,indent=2)+'\n')
    for name in FILES:shutil.copy2(source/name,output/name)
    command=[sys.executable,str(HERE.parents[1]/'tools/upload_media.py'),str(output),
             '--video',str(output/'model.mp4'),'--demo',str(output/'demo.mp4'),
             '--screenshot',str(output/'setup.png')]
    if upload:subprocess.run(command,check=True)
    else:print('PREPARED VERIFIED MEDIA; upload command (not run): '+shlex.join(command))
    return spec


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--qualification',type=Path,required=True)
    p.add_argument('--review-file',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--upload',action='store_true')
    a=p.parse_args()
    try:prepare(a.qualification.resolve(),a.review_file.resolve(),a.output.resolve(),a.upload)
    except (Incomplete,OSError,ValueError,KeyError) as exc:
        print(str(exc),file=sys.stderr);return 2
    return 0


if __name__=='__main__':raise SystemExit(main())

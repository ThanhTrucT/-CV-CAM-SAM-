"""Create run metadata only, without starting ML or overwriting a run."""
import argparse,json,re,hashlib,subprocess
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
def create_run(run_id,method,owner,split,seed,root=ROOT):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}',run_id):raise ValueError('Invalid run ID')
    config_path=root/f'configs/{method}.json'
    config=json.loads(config_path.read_text(encoding='utf-8'))
    folder=root/'results'/run_id
    folder.mkdir(parents=True,exist_ok=False)
    try:commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,stderr=subprocess.DEVNULL,text=True).strip()
    except (OSError,subprocess.CalledProcessError):commit=None
    split_path=root/f'data/lists/{split}.txt'
    split_hash=hashlib.sha256(split_path.read_bytes()).hexdigest() if split_path.exists() else None
    manifest={'run_id':run_id,'method':method,'owner':owner,'split':split,'seed':seed,'created_utc':datetime.now(timezone.utc).isoformat(),'commit':commit,'split_sha256':split_hash,'status':'prepared_not_run','cam_checkpoint_sha256':None,'sam_checkpoint_sha256':None,'image_count':None,'failure_count':None,'artifact_locations':[]}
    for name,obj in [('config.json',config),('manifest.json',manifest)]:
        (folder/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (folder/'metrics.json').write_text('{}\n',encoding='utf-8')
    (folder/'cost.csv').write_text('image_id,prompt_points,prompt_sets,sam_calls,seconds,peak_vram_mb\n',encoding='utf-8')
    (folder/'command.txt').write_text('# Fill the actual ML command before running. No ML executed by this scaffold.\n',encoding='utf-8')
    (folder/'log.txt').write_text('',encoding='utf-8')
    return folder
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('run_id');p.add_argument('--method',choices=['B0','B1','B2','P','S','PS'],required=True);p.add_argument('--owner',required=True);p.add_argument('--split',choices=['train_fit','dev','val'],required=True);p.add_argument('--seed',type=int,default=0)
    a=p.parse_args();print(create_run(a.run_id,a.method,a.owner,a.split,a.seed))

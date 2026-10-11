"""Validate scaffold contracts; this does not validate trained models."""
import csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def validate(root=ROOT):
    mapping=json.loads((root/'data/metadata/class_map.json').read_text(encoding='utf-8'))
    classes=mapping['classes']
    assert len(classes)==20
    assert {c['cam_channel'] for c in classes}==set(range(20))
    assert {c['semantic_id'] for c in classes}==set(range(1,21))
    assert next(c for c in classes if c['name']=='cow')=={'name':'cow','cam_channel':9,'semantic_id':10}
    for path in (root/'configs').glob('*.json'):json.loads(path.read_text(encoding='utf-8'))
    rows=list(csv.DictReader((root/'docs/tasks.csv').open(encoding='utf-8',newline='')))
    assert len(rows)==32 and len({r['task_id'] for r in rows})==32
    assert sum(r['owner']=='Nguoi 1' for r in rows)==16
    assert all(r['owner']!=r['reviewer'] for r in rows)
    sets={}
    for name in ['train_fit','dev','val']:
        path=root/f'data/lists/{name}.txt'
        if path.exists():
            ids=[s.strip() for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
            assert len(ids)==len(set(ids)),f'duplicate IDs: {name}'
            sets[name]=set(ids)
    names=list(sets)
    for i,a in enumerate(names):
        for b in names[i+1:]:assert not sets[a]&sets[b],f'overlap {a}/{b}'
    return len(rows),len(sets)
if __name__=='__main__':
    count,splits=validate()
    print(f'PASS: {count} tasks, class map, JSON configs; {splits} supplied split lists checked. ML pipeline not implemented.')

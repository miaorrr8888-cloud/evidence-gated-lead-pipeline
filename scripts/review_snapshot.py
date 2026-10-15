"""Match a quote against a user-captured local page; never equate text presence with truth."""
import argparse,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
from urllib.parse import urlsplit

def review(record,root,now=None):
    root=Path(root).resolve()
    for field in ('snapshot','source_url','quote','captured_at'):
        if not isinstance(record.get(field),str) or not record[field].strip():raise ValueError(field+' required')
    u=urlsplit(record['source_url'])
    if u.scheme!='https' or not u.hostname or u.username or u.password:raise ValueError('invalid source_url')
    raw=root/record['snapshot']; path=raw.resolve()
    if raw.is_symlink() or not path.is_relative_to(root) or not path.is_file():raise ValueError('snapshot must be within input directory')
    if path.stat().st_size>5_000_000:raise ValueError('snapshot too large')
    body=path.read_text(encoding='utf-8-sig'); captured=datetime.fromisoformat(record['captured_at'].replace('Z','+00:00'))
    if captured.tzinfo is None:raise ValueError('captured_at requires timezone')
    age=((now or datetime.now(timezone.utc))-captured).total_seconds()/3600
    found=' '.join(record['quote'].split()) in ' '.join(body.split())
    current=0<=age<=24
    return {'quote_found':found,'fresh_within_24h':current,'snapshot_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'status':'READY_FOR_HUMAN_REVIEW' if found and current else 'HOLD','source_url':record['source_url'],
            'scope':'LOCAL_SNAPSHOT_ONLY','live_page_verified':False,'buyer_verified':False,'contacted':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('record');a=p.parse_args();path=Path(a.record).resolve()
    try:r=review(json.loads(path.read_text(encoding='utf-8-sig')),path.parent)
    except (OSError,ValueError,TypeError) as e:p.exit(2,'Input error: '+str(e)+'\n')
    print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()

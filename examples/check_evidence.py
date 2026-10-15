"""Synthetic URL examples; the script does not open these pages."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'references'))
from evidence_gate import apply_gate
samples=[{'channel':'Upwork','evidence_url':'https://www.upwork.com/hire/demo/','acquisition_path':'RESPOND_TO_JOB_POST'},
         {'channel':'Upwork','evidence_url':'https://upwork.com/freelance-jobs/apply/synthetic-demo_~123','acquisition_path':'RESPOND_TO_JOB_POST'}]
for sample in samples:
    reviewed,downgraded=apply_gate(sample); print(json.dumps({'synthetic':True,'reviewed':reviewed,'downgraded':downgraded},ensure_ascii=False))

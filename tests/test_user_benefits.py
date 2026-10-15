from pathlib import Path
import importlib.util, unittest, tempfile, subprocess, sys, json, zipfile, io, struct, os
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

class EvidenceEdges(unittest.TestCase):
    def setUp(self): self.m=load('evidence',ROOT/'references/evidence_gate.py')
    def test_malformed_and_credential_urls_rejected(self):
        for url in ['https://','https://[bad','https://user:pass@www.upwork.com/freelance-jobs/apply/demo_~123','https://www.upwork.com:444/freelance-jobs/apply/demo_~123']:
            self.assertFalse(self.m.classify_evidence(url,'Upwork')[1])
    def test_bare_official_host_and_full_path(self):
        self.assertTrue(self.m.classify_evidence('https://upwork.com/freelance-jobs/apply/demo_~123','Upwork')[1])
        self.assertFalse(self.m.classify_evidence('https://upwork.com/freelance-jobs/apply/demo_~123fake','Upwork')[1])
    def test_structure_check_cannot_mark_content_verified(self):
        result,_=self.m.apply_gate({'channel':'Upwork','evidence_url':'https://upwork.com/freelance-jobs/apply/demo_~123'})
        self.assertFalse(result['content_verified']); self.assertEqual(result['validation_scope'],'URL_STRUCTURE_ONLY')

if __name__=="__main__": unittest.main()

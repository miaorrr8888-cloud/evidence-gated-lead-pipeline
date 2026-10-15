from pathlib import Path
import importlib.util, unittest, tempfile, subprocess, sys, json, zipfile, io, os
R=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

class Evidence(unittest.TestCase):
    def setUp(self): self.m=load('evidence',R/'references/evidence_gate.py')
    def test_spoofed_upwork_host_rejected(self):
        self.assertFalse(self.m.classify_evidence('https://www.upwork.com.attacker.example/freelance-jobs/apply/job_~123','Upwork')[1])
    def test_category_page_is_downgraded(self):
        lead,changed=self.m.apply_gate({'channel':'Upwork','evidence_url':'https://www.upwork.com/hire/editors/','acquisition_path':'RESPOND_TO_JOB_POST'})
        self.assertTrue(changed); self.assertEqual(lead['evidence_url_status'],'FLAGGED')
    def test_unknown_third_party_stays_unknown(self):
        lead,changed=self.m.apply_gate({'channel':'TikTok Shop','evidence_url':'https://example.org/post','acquisition_path':'RESPOND_TO_JOB_POST'})
        self.assertFalse(changed); self.assertEqual(lead['evidence_url_status'],'THIRD_PARTY')

class TestExternalStateRequiresNoteAndHumanFlag(unittest.TestCase):
    def test_external_state_requires_note_and_human_flag(self):
        m=load('ceiling',R/'references/automation_ceiling.py')
        self.assertFalse(m.check_advance('CONTACT_READY','CONTACTED',human=False)[0])
        self.assertFalse(m.check_advance('CONTACT_READY','CONTACTED',human=True)[0])
        self.assertTrue(m.check_advance('CONTACT_READY','CONTACTED',note='manually sent; receipt available',human=True)[0])

if __name__=="__main__": unittest.main(verbosity=2)

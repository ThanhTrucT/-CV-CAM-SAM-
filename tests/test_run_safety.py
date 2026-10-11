import unittest,tempfile,json
from pathlib import Path
from scripts.new_run import create_run
class RunSafety(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
        (self.root/'configs').mkdir();(self.root/'configs/B2.json').write_text('{}')
    def tearDown(self):self.tmp.cleanup()
    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError):create_run('../outside','B2','N1','dev',0,self.root)
        self.assertFalse((self.root/'results').exists())
    def test_preserves_existing_run_and_marks_not_run(self):
        out=create_run('E001','B2','N1','dev',0,self.root)
        self.assertEqual(json.loads((out/'manifest.json').read_text())['status'],'prepared_not_run')
        (out/'log.txt').write_text('keep')
        with self.assertRaises(FileExistsError):create_run('E001','B2','N1','dev',0,self.root)
        self.assertEqual((out/'log.txt').read_text(),'keep')

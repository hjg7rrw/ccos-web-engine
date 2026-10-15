import pathlib,subprocess,tempfile,unittest
SCRIPT=pathlib.Path(__file__).resolve().parents[1]/'scripts'/'new_experience.py'
class TestScaffold(unittest.TestCase):
    def test_scaffold_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as root:
            dest=pathlib.Path(root)/'original-project'
            args=['python3',str(SCRIPT),'--name','Orbit Atelier','--accent','#aa66cc','--dest',str(dest)]
            r=subprocess.run(args,capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stderr)
            self.assertIn('Orbit Atelier',(dest/'index.html').read_text())
            self.assertIn('#aa66cc',(dest/'src/styles.css').read_text())
            self.assertTrue((dest/'src/engine.js').exists())
            self.assertNotEqual(subprocess.run(args,capture_output=True).returncode,0)
if __name__=='__main__':unittest.main()

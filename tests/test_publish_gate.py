"""Historical negative controls for private-only GitHub publishing guard.
NOT a current restriction: user later explicitly authorized public upload.
"""
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
import subprocess,sys
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
FILE=ROOT/'scripts'/'publish_to_new_repo.py'
spec=spec_from_file_location('ccos_publish',FILE)
module=module_from_spec(spec)
spec.loader.exec_module(module)
def test_no_gh_refuses_private_verification():
    with patch.object(module.shutil,'which',return_value=None):assert module.private_gate() is False
def test_public_repo_refuses():
    with patch.object(module.shutil,'which',return_value='/usr/bin/gh'),patch.object(module,'run',return_value='PUBLIC'):assert module.private_gate() is False
def test_authenticated_private_allows():
    with patch.object(module.shutil,'which',return_value='/usr/bin/gh'),patch.object(module,'run',return_value='PRIVATE'):assert module.private_gate() is True
def test_gh_error_refuses():
    with patch.object(module.shutil,'which',return_value='/usr/bin/gh'),patch.object(module,'run',side_effect=RuntimeError('denied')):assert module.private_gate() is False
def test_default_dry_run():
    result=subprocess.run([sys.executable,str(FILE)],text=True,capture_output=True)
    assert result.returncode==0
    assert 'NO REMOTE ACTION' in result.stdout
if __name__=='__main__':
    checks=[test_no_gh_refuses_private_verification,test_public_repo_refuses,test_authenticated_private_allows,test_gh_error_refuses,test_default_dry_run]
    for fn in checks:fn();print('PASS',fn.__name__)

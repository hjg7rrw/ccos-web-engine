# CCOS WebGL2 Windows capability test; UNVERIFIED on Windows.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
  throw 'Python launcher (py) is not installed'
}
py -m pip show playwright | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'Install Python Playwright first' }
py ops/webgl2_probe.py --modes headless-default,headless-swiftshader,headed-default,headed-swiftshader --output qa/windows_matrix.json --require-one
if ($LASTEXITCODE -ne 0) { throw 'No WebGL2 draw success; inspect qa/windows_matrix.json' }

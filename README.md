# CCOS Web Engine — Independent Cinematic WebGL2 Studio Lab

**Original owner:** Andrew Rosa / CCOS Studio  
**Status:** Open technical research and development, not production-approved  
**Current GitHub visibility:** PUBLIC. **License:** UNLICENSED (all rights reserved).

This is the dedicated CCOS web-engine repository, separate from Jarvis. It contains the original responsive, cinematic WebGL2 website and a repeatable software-rendering laboratory using Chromium, ANGLE SwiftShader, Mesa llvmpipe and Xvfb. Successful and unsuccessful test evidence is preserved.

## Run the website

With Python 3 installed, from the repository root:

```bash
python3 -m http.server 8080
```

Open `http://localhost:8080` on that machine. Windows: `run_local.bat`; Linux: `sh run_local.sh`.

## Test it

```bash
node --test tests/math.test.mjs
python3 tests/test_scaffold.py
python3 tests/test_publish_gate.py
# Linux + Chromium + Xvfb + Playwright required for actual WebGL2 tests:
bash ops/run_matrix_linux.sh
bash run_webgl2_qa.sh
```

GitHub-hosted tests:
- [Deterministic source tests](https://github.com/hjg7rrw/ccos-web-engine/actions/workflows/unit-tests.yml) — actually passed October 15, 2026.
- [WebGL2 software graphics/screenshots](https://github.com/hjg7rrw/ccos-web-engine/actions/workflows/webgl2-capture.yml) — real 4,800-point browser rendering passed in GitHub-hosted CI; original screenshots available as workflow artifacts, and new screenshots are staged in a dedicated evidence review branch where supported.

## Project structure

| Directory | Purpose |
|---|---|
| `src/` | Original WebGL2 shaders, deterministic geometry, camera/scroll and controls |
| `index.html` | Semantic original 3-scene homepage |
| `tests/` | Geometry, site generator, browser fallback, interaction and WebGL2 QA |
| `ops/` | Independent WebGL2 probe and Xvfb/Mesa/SwiftShader launchers |
| `lab/v0.1.3/` | Original isolated diagnostic code and evidence ledger from the Jarvis research branch |
| `qa-webgl2/` | Machine-readable PASS/FAIL records and hosted software-browser captures |
| `docs/` | Rights, releases, pain points, design/QA gates and source provenance |
| `skills/` | Reusable CCOS graphical engineering operator instructions |
| `scripts/` | Website scaffold, public research audits and dry-run-first historical archive importer |

## Release migration boundaries

The original local v0.1.4 release archive includes **73 files plus a separate Git-history bundle**, with historical screenshot PNGs. The currently published source/test/diagnostic subset is functional and independently read back. Some historical documents and original binary screenshots are **not yet imported byte-for-byte**. See `docs/RELEASE_MIGRATION_STATUS_2026-10-15.md`.

The new `scripts/import_historical_release.py` was dry-run validated against the ZIP (74 importable entries including the bundle). It requires a network-enabled, authenticated Git environment to create its separate archival review branch and transfer all files without overwriting `main`. The present container cannot resolve GitHub over Git CLI. Do not claim that this complete legacy archive has already been pushed.

## QA and security policy

- Separate WebGL2 **capability**, actual draw/readback, application behavior, and native physical GPU measurements.
- Record failures as well as successes. Headless SwiftShader may initialize intermittently in different configurations; headed Chromium on Xvfb with explicit software backend was the repeatable local path.
- Native HTTP and ES-module loading, real physical mobile GPUs, Windows parity, accessibility, and public site deployment are separate OPEN gates.
- Browser graphics flags including `--enable-unsafe-swiftshader` must only be used for trusted, locally authored content in an isolated test environment.
- Igloo Inc. is a referenced original developer case study, not an imported IP or asset pack; independent code is authored locally. Do not copy competitor artwork or unlicensed public repositories.
- Jarvis production branches and the user vault remain separate and unchanged.

**No CCOS project lineage uses hash/checksum tracking.** Human-readable version labels, run dates, source IDs, Git commits for transport, and explicit learning deltas provide provenance.

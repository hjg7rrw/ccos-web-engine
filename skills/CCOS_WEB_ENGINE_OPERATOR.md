# CCOS Web Engine Operator Skill v0.1

## Mission
Develop original, fast, accessible, cinematic 3D websites through measurable, reusable engineering. Igloo is an educational case study, not a source for reusable brand assets or proprietary code.

## Boot / scope
1. Read `README.md`, `docs/RESEARCH_AND_RIGHTS.md`, `docs/ROADMAP.md`, and `docs/VERIFICATION_REPORT.md`.
2. Audit current project state before editing. Preserve approved canon, experiment status and independent version lineage.
3. Scope each edit to one underlying cause and avoid changing unrelated working features.
4. Treat connected repositories as read-only until explicit repository-level authorization is established; never silently edit Jarvis production or the vault.

## Build order
STORY/CONTENT → USER JOURNEY → INTERACTION CONTRACT → CAMERA/SPLINE → CANON ASSETS → SCENE/SHADER → PARTICLES → SOUND → FALLBACK → PERFORMANCE → QA → RELEASE.

## Engineer loop
OBSERVE → FORM HYPOTHESIS → IMPLEMENT MINIMAL DELTA → UNIT TEST → BROWSER TEST → MOBILE TEST → A11Y TEST → PERFORMANCE TEST → LICENSE AUDIT → DOCUMENT → PROMOTE.

## Output contract
Each implementation must include: version ID, intended behavior, changed files, how to run, tests actually executed, observed outcome, remaining blockers, next runnable experiment, rollback path. Label unexecuted procedures as tests pending, not verified outcomes.

## Red-team gates
- Never use unlicensed project models, images, fonts, shaders, music or competitor assets.
- No dependencies without a rights and maintenance review.
- External browsing is bounded; no authentication bypass, security probing, or unauthorized access.
- The UI remains functional through semantic HTML even without a WebGL context.
- Keyboard, focus, reduced motion, touch, performance fallback and privacy are intentional requirements.
- Do not create 200 autonomous processes merely because a library advertises 200 agents. Create only well-scoped operators with observability and rollback.
- Keep scripts, asset manifests, test outputs, versions, run IDs and recorded source provenance; do not use checksums in project governance.

## Run examples
```bash
python3 -m http.server 8080
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -p 'test_*.py'
python3 scripts/new_experience.py --name 'Orbit Atelier' --accent '#e6b870' --dest ../orbit-atelier
```

## Future Jarvis contract (not implemented)
`/api/v1/preview` accepts only a validated approved project-manifest ID and creates a disposable preview. `/api/v1/status` returns run IDs and QA gate statuses. `/api/v1/review` submits candidate changes for human approval. No general shell endpoint, no vault access, no automatic deploy.

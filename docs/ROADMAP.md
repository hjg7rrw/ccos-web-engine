# Controlled engineering roadmap | v0.1

## Completed in local v0.1 candidate

Original 3D GPU particle renderer; deterministic shape generation; three interactive state changes; camera-on-scroll; responsive HTML presentation; no runtime packages or remote dependencies; reduced-motion handling; adaptive pixel ratio; diagnostics; basic render recovery; public-source audit scripts; math unit tests.

## Next gates (not yet verified / implemented)

**G01** Browser: visual screenshot on desktop and mobile with WebGL working; verify console clean.
**G02** Interactions: click shape cards, morph button, navigation, diagnostics; compare canvas captures after each state and scroll.
**G03** Performance: sustained 60 FPS on specified desktop hardware, at least 30 FPS on specified mobile hardware; measure GPU memory proxies and first interaction under real throttling. These are targets, not claims.
**G04** A11y: axe-core / keyboard navigation / reduced motion with screen reader; no WebGL-only information, no unlabelled actionable elements.
**G05** Content: replace concept copy with approved studio projects only; no silent canon changes.
**G06** Rights: approve artwork/fonts/audio license basis before integrating external media.

## Candidate subsequent modules
1. Camera waypoint editor and inspector with serialized scene definitions.
2. Original mesh artifact library with BVH-based picking and responsive project panels.
3. GPU physics module using spring-damper particle motion and full morph state machine.
4. Original GLSL shader library: Fresnel, distortion, frost-like layers, depth-controlled postprocessing.
5. Asset pipeline: GLB compression, LODs, texture variants, manifest-based loading and export.
6. Audio engine with explicit user consent to play; no autoplay surprises.
7. Studio CMS/API with approved content schema and authentication.
8. Jarvis operator integration after security audit; constrained build targets and dry-run, no direct production repo write.
9. Continuous site audit, Lighthouse runs and documented browser-device matrix.
10. Release gates, non-regression test suite and learning ledger after real website launch.

## Autonomous agent boundary

Jarvis can eventually propose manifests, previews and pull requests. It should never be granted blanket filesystem, credentials or production-deployment authority. Use scoped working directories, read-only research credentials, branch-based changes, dependency pinning, automated tests and manual approval for publication. A high agent count is not itself an indicator of reliability.

## Reusable website generator — v0.1 addition

`scripts/new_experience.py` now generates an independent named and color-themed website from the template. Validation rejects non-hex colors and overwrites. This is an internal tooling capability, not a substitute for a complete brand brief or production-ready content schema.

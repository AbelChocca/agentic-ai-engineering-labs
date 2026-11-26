# Stickman Studio — Execution Plan

**Status:** Documentation complete; implementation not started.  
**Owner:** Human Lead Developer.  
**Implementer:** Codex CLI.  
**Rule:** Implement one milestone at a time, verify acceptance criteria and report results. Do not automatically expand into the next milestone.

## M0 — Python environment and repository-local setup

**Owner:** Codex CLI. **Status:** TODO.

- Inspect current project subdirectory and existing `AGENTS.md`; preserve any code or configuration already present.
- Confirm parent Git repository is already initialized and **DO NOT run `git init`** or alter files outside the project subdirectory.
- Initialize local Python 3.12 project managed with `uv`, including a `.venv` in the project subdirectory.
- Create `pyproject.toml`, resolve/install dependencies, generate `uv.lock`, ensure local CLI package is importable.
- Install only project-scoped dependencies. Verify availability of `ffmpeg` and `ffprobe`; if unavailable, request approval for machine-wide installation rather than silently modifying global system.
- Create `.env.example` for Gemini / LangSmith (no credentials committed). Update project-local ignore patterns safely; avoid edits to parent `.gitignore` without approval.
- Configure Ruff and pytest, a basic smoke test, a minimal README with exact local commands.

**Acceptance:** `uv sync`, `uv run pytest`, `uv run ruff check .` pass; Python interpreter is 3.12; `ffmpeg` and `ffprobe` are accessible or documented as a blocking prerequisite; no Git repo was initialized or reset; existing files are intact.

## M1 — Offline deterministic first render

**Owner:** Codex CLI. **Status:** TODO.

- Implement Pydantic models and validation from `CONTRACTS.md`.
- Hand-author a 5-second JSON fixture representing two stickmans, a server icon, a caption and a `point` gesture.
- Implement basic stickman geometry, poses, fixed-time frame generation, Pillow composition and FFmpeg encoding with bounded memory.
- Implement MP4 validation with FFprobe and meaningful errors; write a minimal manifest.
- CLI `render` command generates a video without model credentials.

**Acceptance:** fixture renders **120 frames** to 5-second H.264 1280×720 24-fps MP4; file exists and is nonempty; FFprobe validates format/duration; tests include schema rejection and one end-to-end render.

## M2 — 30-second visual language

**Owner:** Codex CLI. **Status:** TODO.

- Implement `idle`, `walk`, `wave`, `point`, `enter`, `exit` with deterministic pose/timeline interpolation.
- Implement educational captions with safe wrapping and a modest set of objects (computer, server, request, response, arrows and labels).
- Support multiple scenes; ensure total frames exactly equal target requested duration and no time gaps.
- Produce a hand-authored API REST storyboard of 30 seconds as a fixture.

**Acceptance:** 720-frame 30-second educational video from **JSON only**, containing two animated characters, multiple scenes and legible captions; smoke render and format checks pass.

## M3 — Agentic content generation

**Owner:** Codex CLI. **Status:** TODO.

- Create Deep Agent supervisor with scoped scriptwriter and storyboard subagents; explicit tools for writing artifacts and invoking existing renderer/validator.
- Use environment-provided Gemini credentials; fail helpfully if absent. Enable LangSmith only when configured.
- Produce `plan.md`, `script.md`, `storyboard.json` for a request and validate against Pydantic. Reject or bounded-retry invalid outputs; never execute generated code.
- Keep prompts and tool descriptions concise; track relevant decisions in docs.

**Acceptance:** Given an educational topic, agent produces a valid storyboard and written artifacts; tests mock the LLM; trace reveals delegation and tool use in an opt-in real-model smoke test.

## M4 — End-to-end demo, hardening and handoff

**Owner:** Codex CLI. **Status:** TODO.

- CLI `generate` handles prompt → plan → script → storyboard → render → validation.
- Emit manifest and meaningful logs, safe unique output paths, clear failure behavior and rerun semantics.
- Validate full 30-second API REST prompt in a real Gemini run (subject to API availability).
- Document commands, env configuration and demo evidence; maintain reproducible fixture path for offline demo.

**Acceptance:** one CLI request produces `outputs/<slug>/final.mp4`, `plan.md`, `script.md`, `storyboard.json`, `manifest.json`; FFprobe passes; offline render continues to work without API credentials; tests/lint pass.

## Codex task policy

1. Before work, read `AGENTS.md`, `ARCHITECTURE.md`, `CONTRACTS.md` and only the applicable milestone in this plan.
2. Do not overwrite existing work or redefine interfaces silently.
3. Complete the milestone's implementation **and** tests, then run checks and fix failures.
4. Update the milestone's status and concise evidence of commands/results when it is truly complete.
5. Report changed files, acceptance tests, limitations and architectural proposals requiring approval.
6. Stop before the next milestone, unless explicitly authorized.

## Milestone log

| Milestone | State | Verified evidence |
| --- | --- | --- |
| M0 | TODO | — |
| M1 | TODO | — |
| M2 | TODO | — |
| M3 | TODO | — |
| M4 | TODO | — |

# Stickman Studio — Architecture Decision Records

Accepted below as **MVP planning defaults** based on Lead Developer discussion. Any later change requires Lead Developer approval and an ADR amendment; Codex cannot silently replace decisions.

## ADR-001: Local deterministic 2D renderer

**Status:** Accepted for MVP.  
**Decision:** Pillow for frame composition, FFmpeg for H.264 MP4 encoding and FFprobe for validation. Model outputs scene JSON, not executable render code.  
**Why:** Reliable output, predictable costs, repeatability and fast debugging.  
**Alternatives:** SVG rasterization per frame; browser/Canvas/Three.js.  
**Consequence:** A small supported motion/object vocabulary; visual sophistication is deferred.

## ADR-002: CLI-first

**Status:** Accepted.  
**Decision:** Local Python CLI, no web frontend/backend.  
**Why:** Focus on working end-to-end video generation; minimal orchestration overhead.  
**Alternative:** Web UI.  
**Consequence:** User interaction initially via terminal.

## ADR-003: Deep Agents with scoped subagents

**Status:** Accepted.  
**Decision:** One supervisor responsible for planning and validation; specialized scriptwriter and storyboard subagents. Start renderer without LLMs, introduce orchestration at M3.  
**Why:** Demonstrate planning, artifacts, task delegation and tool use without introducing unnecessary microservices.  
**Alternative:** One undifferentiated agent.  
**Consequence:** Higher complexity and token usage than a single agent; mitigate with short tool contracts and bounded retries.

## ADR-004: Silent video MVP

**Status:** Accepted.  
**Decision:** Captions and speech bubbles only. No TTS/audio initially.  
**Why:** Avoid voice production and synchronization as critical-path risks.  
**Alternative:** Immediate TTS.  
**Consequence:** Educational clarity depends on legible captions and pacing.

## ADR-005: Python and modular monolith

**Status:** Accepted.  
**Decision:** Python 3.12, uv, Pydantic v2, pytest, Ruff; module boundaries described in ARCHITECTURE.  
**Why:** Toolchain matches Deep Agents course and favors fast iteration.

## ADR-006: Existing parent Git repository

**Status:** Accepted and mandatory.  
**Decision:** Stickman Studio is a subdirectory inside an existing initialized Git repository. **Do not run `git init`, clone, reset or reconfigure Git.** Work only in this project's subdirectory; do not alter parent repo configuration, history or unrelated files.  
**Why:** Avoid damaging an existing ongoing repository.  
**Consequence:** Codex creates Python environment and dependencies locally, not Git infrastructure.

## ADR-007: Human/agent division of responsibilities

**Status:** Accepted.  
**Decision:** Lead Developer approves direction and validates outcomes; architect owns proposals; Codex implements setup, dependencies, code, tests and local docs updates.  
**Why:** Avoid repeated manual implementation and unapproved architectural drift.

## ADR-008: Production-safe output validation

**Status:** Accepted.  
**Decision:** Validate LLM JSON before rendering; use safe output paths; no generated executable code; verify MP4 with FFprobe.  
**Why:** Reliable outputs and a safe trust boundary between LLM and local runtime.

## Open design questions (not blockers for M0–M1)

- Fonts/caption layout on macOS and cross-platform environments.
- Detailed motion interpolation and easing vocabulary.
- How much technical research is necessary for simple educational topics.
- Whether per-scene SVG previews should be an optional export after the raster MVP works.

The Lead Developer can decide these when relevant. Codex may propose options with trade-offs but must not silently add major dependencies.

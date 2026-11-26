# Stickman Studio — Product Brief

**Status:** MVP scope approved for implementation planning.  
**Owner:** Human Lead Developer.  
**Language:** Spanish user prompts supported; internal schema and code identifiers in English.

## Purpose

Convert a natural-language educational request into a self-contained, reproducible **2D stickman explainer video**. Example: “Crea una animación educativa de 30 segundos donde dos stickmans expliquen cómo funciona una API REST.”

## MVP user journey

1. User executes the CLI with a topic, a requested duration (default 30 seconds), and an output directory.
2. A Deep Agent plans, optionally researches the topic, and delegates script and storyboard work.
3. The application writes `plan.md`, `script.md`, `storyboard.json` in a project-specific output directory.
4. The storyboard is validated against strict schemas and a renderer capability catalog.
5. A deterministic engine renders frames and FFmpeg produces `final.mp4`.
6. FFprobe checks dimensions, frame rate, video codec, duration, and existence. The CLI reports generated artifacts or an actionable failure.

## MVP capabilities

- 2D articulated stick figures (at least two characters), idle, walk, wave, point, and enter/exit transitions.
- Legible educational captions / speech bubbles, basic visual objects (server, computer, HTTP request/response, labels), scene backgrounds.
- Time-based scene and action specifications, simple animation easing, fixed scene transitions (cut or fade if feasible).
- MP4 H.264, 1280×720, 24 fps, nominal 30 seconds for the headline demo.
- Local filesystem output; repeatable rendering of the same storyboard without an LLM.
- LangSmith tracing for LLM/agent portions when environment variables are configured.

## Explicit non-goals

- Text-to-speech, generated voice, synchronized lip movement or music in MVP.
- Web application, authentication, cloud hosting, database, multi-tenancy, queueing or billing.
- Cinematic 3D, photorealistic generation, text-to-video foundation models or per-frame LLM/image API calls.
- Arbitrary Python/JavaScript/FFmpeg commands authored by the model.
- Direct publishing to social media.

## Quality bar

- Demonstrate a locally produced, playable ~30-second tutorial from one CLI request.
- Every output video has source storyboard and metadata available for review.
- Schemas reject unsupported animation types and invalid time ranges **before** expensive rendering.
- Clear error messages when Gemini, model quota, FFmpeg, fonts, or filesystem are unavailable.
- No claim of successful generation unless the MP4 passes automated validation.

## User roles

- **Lead Developer:** prioritizes, reviews, accepts architecture and validates final videos.
- **Architect:** proposes architectural decisions and acceptance criteria.
- **Codex CLI:** implements code, environment, tests and updates milestone status within the authorized subdirectory.

## Primary demo

An API REST explainer with two stick figures: client asks for data, request travels to server, server processes request, response returns, and both summarize the client/server interaction.

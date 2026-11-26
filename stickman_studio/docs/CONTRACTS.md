# Stickman Studio — Contracts v0.1

**Status:** Proposed baseline for implementation; refine field names only through an explicit ADR before consumers rely on them. The aim is a stable declarative renderer API.

## Design principles

- JSON is data, not executable code. Unknown keys and unsupported enum values must be rejected by Pydantic (`extra="forbid"`).
- Define separate types for `Storyboard`, `Scene`, `Character`, `Action`, `Caption`, and `VisualObject`.
- Internal timing uses integer frames at 24 fps; external scene duration may be represented as `duration_frames` to avoid drift.
- 30-second default = **720 frames**, 1280×720; a 5-second fixture = 120 frames.
- Paths/asset references are trusted identifiers resolved by application code, not arbitrary filesystem paths.

## Minimal JSON example

```json
{
  "schema_version": "0.1",
  "title": "How a REST API works",
  "fps": 24,
  "width": 1280,
  "height": 720,
  "scenes": [
    {
      "id": "scene_01",
      "duration_frames": 120,
      "background": "#F8FAFC",
      "characters": [
        {"id": "client", "x": 300, "y": 540, "color": "#1E293B", "scale": 1.0},
        {"id": "server", "x": 940, "y": 540, "color": "#1E293B", "scale": 1.0}
      ],
      "objects": [
        {"id": "api", "type": "server", "x": 940, "y": 390, "label": "API"}
      ],
      "actions": [
        {"character_id": "client", "type": "point", "start_frame": 24, "duration_frames": 70, "target_x": 940, "target_y": 390}
      ],
      "captions": [
        {"text": "A client sends a request to an API", "start_frame": 0, "duration_frames": 120}
      ]
    }
  ]
}
```

The sample above is intentionally **5 seconds**: render it in M1. The 30-second demo should contain 720 total frames across all scenes.

## Required schema rules

### Storyboard

- `schema_version`: exactly `"0.1"` for MVP.
- `title`: non-empty text, bounded length.
- `fps`: exactly `24` for MVP.
- `width`/`height`: `1280` / `720` for MVP.
- `scenes`: between 1 and a bounded maximum, with unique `id` values.
- Total duration: sum of `duration_frames`; enforce target duration against requested CLI duration, frame-accurate.

### Scene

- `id`: safe slug, e.g. `scene_01`; unique in storyboard.
- `duration_frames`: positive integer.
- `background`: valid hex color (no model-authored file paths).
- `characters`, `actions`, `captions`, `objects`: arrays (possibly empty, with limits).

### Character

- `id`: safe identifier unique within scene.
- `x`, `y`: finite coordinates in canvas units (define position as feet anchor; y increases downward).
- `color`: valid hex string; `scale`: bounded positive float.

### Action

- `character_id`: must reference an existing character in the same scene.
- `type`: allowlisted enum: `idle`, `walk`, `wave`, `point`, `enter`, `exit`.
- `start_frame`: nonnegative integer.
- `duration_frames`: positive integer.
- `[start_frame, start_frame + duration_frames)` must lie inside the scene.
- `target_x` / `target_y`: optional or required depending on action (`walk`/`point` require targets).
- Overlapping actions on one character: reject conflicting overlaps unless explicitly supported by renderer; define deterministic priority before enabling combinations.

### Caption

- `text`: bounded non-empty plain text. No markup/script execution.
- `start_frame` and `duration_frames`: scene-local valid frame range.
- Renderer must wrap text legibly and keep within safe title margins.

### VisualObject

- `id`: scene-unique safe identifier.
- `type`: allowlisted enum (start with `server`, `computer`, `request`, `response`, `label`, `arrow`).
- `x`, `y`: finite coordinates. `label`: optional bounded plain text.

## Rendering contract

Input: a fully validated `Storyboard`, a safe project workspace, and optional renderer configuration.

Output: `final.mp4` encoded with H.264, 1280×720, 24 fps, plus `manifest.json`. Rendering is deterministic for the same input and engine version (apart from encoder metadata).

Validation: `ffprobe` must confirm an H.264 video stream, width/height/fps, and total duration within one frame of the expected duration. Must not report success if the final video is absent or empty.

## Artifact contract

```text
outputs/<safe-project-slug>/
  plan.md
  script.md
  storyboard.json
  manifest.json
  final.mp4
  scenes/                 # optional debug frames / thumbnails
```

`manifest.json` records title, request/target duration, computed duration, fps, resolution, output path, pipeline status, validation result and diagnostics without credentials.

## CLI contract (target)

`uv run stickman-studio generate --prompt "..." --duration 30 --output-dir outputs/api-rest-explained`

`uv run stickman-studio render --storyboard tests/fixtures/storyboard_5s.json --output-dir outputs/demo-5s`

Exact executable wiring is established by Codex in M0; commands must be documented in README. Both commands must return nonzero exit codes on failure and explain the reason.

## Error categories

`InvalidStoryboard`, `UnsupportedAnimation`, `MissingDependency`, `ModelGenerationFailure`, `RenderingFailure`, `VideoValidationFailure`. Prefer specific errors and actionable messages over silent fallback.

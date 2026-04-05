# ADR-0003: Use ab-av1 as the AV1 Encoding Backend

## Status
Accepted

## Date
2026-04-04

## Context
The av1-tui tool needs to convert video files to AV1 format. A key user
requirement is ensuring near-imperceptible quality loss during conversion,
which means we need VMAF-based quality targeting rather than fixed
bitrate/CRF guessing.

We need to decide how to invoke AV1 encoding: wrap ffmpeg directly, use a
Python binding, or delegate to a higher-level tool that handles quality
optimization automatically.

## Options Considered

### Option A: ab-av1
- **Pros:**
  - `auto-encode` command performs interpolated binary search with VMAF
    sampling to find the optimal CRF for a target quality — no manual tuning
  - Handles the full workflow: sample, search, encode
  - Supports SVT-AV1 (primary), plus H.265 and H.264 as alternatives
  - Actively maintained, pre-built binaries for Linux and Windows
  - Clean CLI interface — straightforward to invoke as a subprocess
- **Cons:**
  - Adds a system dependency (ab-av1 must be installed separately)
  - Requires ffmpeg built with libsvtav1, libvmaf, and libopus
  - Progress output format is not a stable API — parsing may break between versions
  - Written in Rust, so not installable via pip
- **Effort:** Low — we shell out to `ab-av1 auto-encode` and parse output

### Option B: Direct ffmpeg/SVT-AV1 invocation
- **Pros:**
  - Fewer dependencies (just ffmpeg)
  - Full control over encoding parameters
  - Well-documented progress output (`-progress pipe:1`)
- **Cons:**
  - No built-in VMAF-targeted CRF search — we'd have to implement the
    binary search ourselves (sample encodes, VMAF scoring, iteration)
  - Significant development effort to replicate what ab-av1 does
- **Effort:** High — VMAF search logic is non-trivial to implement correctly

### Option C: Python binding (e.g., ffmpeg-python, PyAV)
- **Pros:**
  - Pure Python, pip-installable
  - In-process control, no subprocess parsing
- **Cons:**
  - No VMAF-targeted CRF search — same problem as Option B
  - PyAV doesn't support SVT-AV1 encoding out of the box
  - ffmpeg-python is largely unmaintained
  - Tight coupling between encoding and application code
- **Effort:** High — same VMAF search problem plus binding limitations

## Decision
Use **ab-av1** as the encoding backend. The `auto-encode` command solves the
hardest problem — VMAF-targeted quality optimization — out of the box. Building
this ourselves on top of raw ffmpeg would be the bulk of the project's
complexity, and ab-av1 has already solved it well. The TUI shells out to
`ab-av1 auto-encode -i <input> --min-vmaf <target>` as a subprocess.

This aligns with the architecture principle that "encoding runs as subprocess"
and "TUI and encoding logic are fully separated."

## Consequences

### Positive
- VMAF-targeted encoding works immediately with no custom implementation
- Users get near-imperceptible quality loss by default
- Clean separation: TUI manages UX, ab-av1 manages encoding intelligence
- If ab-av1 adds new encoders or features, we get them for free

### Negative
- Users must install ab-av1 and a compatible ffmpeg build separately
- We depend on ab-av1's CLI output format for progress reporting
- Cannot pip-install the entire tool — system dependency management needed

### Risks
- ab-av1's progress output format could change between versions, breaking our
  parser. Mitigation: pin to a known version range, add integration tests
  against sample output.
- If ab-av1 is abandoned, we'd need to reimplement the VMAF search.
  Mitigation: the tool is actively maintained; worst case, the Rust binary
  can be vendored.

## Related
- Related ADRs: ADR-0002 (Textual TUI framework — will display encoding progress)
- Relevant commits: (will be filled by the commit recording this decision)
- Discussion: https://github.com/alexheretic/ab-av1

## Provenance
- **Decided by:** human+claude-code
- **Session context:** User chose ab-av1 for its VMAF auto-crf feature ensuring near-imperceptible quality loss. Claude confirmed architectural fit and documented alternatives.

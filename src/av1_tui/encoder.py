"""Wrapper around the ab-av1 CLI for VMAF-targeted AV1 encoding."""

from __future__ import annotations

import asyncio
import shutil
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class EncodeJob:
    """Represents a single encoding task."""

    input_path: Path
    output_path: Path
    min_vmaf: float = 95.0
    preset: int = 6
    encoder: str = "libsvtav1"


@dataclass
class EncodeProgress:
    """Progress update from an encoding job."""

    percent: float = 0.0
    fps: float = 0.0
    elapsed: str = ""
    raw_line: str = ""


@dataclass
class EncodeResult:
    """Final result of an encoding job."""

    job: EncodeJob
    success: bool
    return_code: int = 0
    error: str = ""


def find_ab_av1() -> Path | None:
    """Locate the ab-av1 binary on the system PATH."""
    path = shutil.which("ab-av1")
    return Path(path) if path else None


def build_command(job: EncodeJob) -> list[str]:
    """Build the ab-av1 auto-encode command for a job."""
    return [
        "ab-av1",
        "auto-encode",
        "-i", str(job.input_path),
        "-o", str(job.output_path),
        "--encoder", job.encoder,
        "--preset", str(job.preset),
        "--min-vmaf", str(job.min_vmaf),
    ]


def parse_progress(line: str) -> EncodeProgress | None:
    """Parse a line of ab-av1 stderr output into a progress update.

    Returns None if the line doesn't contain progress information.
    ab-av1 outputs progress lines like:
        'Encoding 50.3% ░░░░░░░░░░ 12.3 fps, eta 1m 30s'
    """
    stripped = line.strip()
    if not stripped.startswith("Encoding"):
        return None

    progress = EncodeProgress(raw_line=stripped)

    # Extract percentage
    parts = stripped.split()
    for part in parts:
        if part.endswith("%"):
            try:
                progress.percent = float(part.rstrip("%"))
            except ValueError:
                pass
            break

    # Extract fps
    for i, part in enumerate(parts):
        if part == "fps," or part == "fps":
            try:
                progress.fps = float(parts[i - 1])
            except (ValueError, IndexError):
                pass
            break

    return progress


async def run_encode(
    job: EncodeJob,
    on_progress: callable | None = None,
) -> EncodeResult:
    """Run an ab-av1 auto-encode job asynchronously.

    Args:
        job: The encoding job to run.
        on_progress: Optional callback invoked with EncodeProgress updates.

    Returns:
        EncodeResult with success status and any error output.
    """
    cmd = build_command(job)

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    error_lines: list[str] = []

    async def read_stderr():
        assert process.stderr is not None
        while True:
            line = await process.stderr.readline()
            if not line:
                break
            decoded = line.decode(errors="replace")
            progress = parse_progress(decoded)
            if progress and on_progress:
                on_progress(progress)
            else:
                error_lines.append(decoded)

    await read_stderr()
    return_code = await process.wait()

    return EncodeResult(
        job=job,
        success=return_code == 0,
        return_code=return_code,
        error="".join(error_lines).strip(),
    )

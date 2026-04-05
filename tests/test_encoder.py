"""Tests for the ab-av1 encoder wrapper."""

from pathlib import Path

from av1_tui.encoder import (
    EncodeJob,
    build_command,
    find_ab_av1,
    parse_progress,
)


class TestBuildCommand:
    def test_default_options(self) -> None:
        job = EncodeJob(
            input_path=Path("/tmp/input.mkv"),
            output_path=Path("/tmp/output.mkv"),
        )
        cmd = build_command(job)
        assert cmd == [
            "ab-av1",
            "auto-encode",
            "-i",
            "/tmp/input.mkv",
            "-o",
            "/tmp/output.mkv",
            "--encoder",
            "libsvtav1",
            "--preset",
            "6",
            "--min-vmaf",
            "95.0",
        ]

    def test_custom_options(self) -> None:
        job = EncodeJob(
            input_path=Path("/tmp/input.mp4"),
            output_path=Path("/tmp/output.mp4"),
            min_vmaf=90.0,
            preset=4,
            encoder="libx265",
        )
        cmd = build_command(job)
        assert "--min-vmaf" in cmd
        assert cmd[cmd.index("--min-vmaf") + 1] == "90.0"
        assert cmd[cmd.index("--preset") + 1] == "4"
        assert cmd[cmd.index("--encoder") + 1] == "libx265"


class TestParseProgress:
    def test_encoding_line(self) -> None:
        line = "Encoding 50.3% ░░░░░░░░░░ 12.3 fps, eta 1m 30s"
        progress = parse_progress(line)
        assert progress is not None
        assert progress.percent == 50.3
        assert progress.fps == 12.3

    def test_zero_percent(self) -> None:
        line = "Encoding 0.0% ░░░░░░░░░░ 0.0 fps, eta --"
        progress = parse_progress(line)
        assert progress is not None
        assert progress.percent == 0.0

    def test_complete(self) -> None:
        line = "Encoding 100.0% ░░░░░░░░░░ 24.1 fps, eta 0s"
        progress = parse_progress(line)
        assert progress is not None
        assert progress.percent == 100.0

    def test_non_progress_line(self) -> None:
        assert parse_progress("Some other output") is None
        assert parse_progress("") is None

    def test_preserves_raw_line(self) -> None:
        line = "Encoding 75.0% ░░░░░░░░░░ 15.0 fps, eta 30s"
        progress = parse_progress(line)
        assert progress is not None
        assert progress.raw_line == line.strip()


class TestFindAbAv1:
    def test_returns_path_or_none(self) -> None:
        result = find_ab_av1()
        assert result is None or isinstance(result, Path)

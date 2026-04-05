"""Tests for the file browser module."""

from pathlib import Path


from av1_tui.file_browser import VIDEO_EXTENSIONS, is_video_file, VideoDirectoryTree


class TestVideoExtensions:
    def test_common_formats_included(self) -> None:
        expected = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".ts"}
        assert expected.issubset(VIDEO_EXTENSIONS)

    def test_no_non_video_formats(self) -> None:
        non_video = {".txt", ".py", ".jpg", ".png", ".mp3", ".pdf"}
        assert non_video.isdisjoint(VIDEO_EXTENSIONS)


class TestIsVideoFile:
    def test_video_file(self, tmp_path: Path) -> None:
        video = tmp_path / "test.mp4"
        video.touch()
        assert is_video_file(video) is True

    def test_non_video_file(self, tmp_path: Path) -> None:
        text = tmp_path / "notes.txt"
        text.touch()
        assert is_video_file(text) is False

    def test_directory_is_not_video(self, tmp_path: Path) -> None:
        subdir = tmp_path / "videos"
        subdir.mkdir()
        assert is_video_file(subdir) is False

    def test_case_insensitive(self, tmp_path: Path) -> None:
        video = tmp_path / "test.MKV"
        video.touch()
        assert is_video_file(video) is True

    def test_nonexistent_path(self, tmp_path: Path) -> None:
        missing = tmp_path / "missing.mp4"
        assert is_video_file(missing) is False


class TestVideoDirectoryTreeFilter:
    def test_filters_non_video_files(self, tmp_path: Path) -> None:
        video = tmp_path / "clip.mp4"
        text = tmp_path / "readme.txt"
        subdir = tmp_path / "subdir"
        video.touch()
        text.touch()
        subdir.mkdir()

        tree = VideoDirectoryTree(tmp_path)
        filtered = list(tree.filter_paths([video, text, subdir]))

        assert video in filtered
        assert subdir in filtered
        assert text not in filtered

    def test_keeps_all_directories(self, tmp_path: Path) -> None:
        dirs = []
        for name in ["a", "b", "c"]:
            d = tmp_path / name
            d.mkdir()
            dirs.append(d)

        tree = VideoDirectoryTree(tmp_path)
        filtered = list(tree.filter_paths(dirs))
        assert filtered == dirs

    def test_empty_input(self, tmp_path: Path) -> None:
        tree = VideoDirectoryTree(tmp_path)
        assert list(tree.filter_paths([])) == []

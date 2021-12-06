import subprocess
import sys
from pathlib import Path
from textwrap import dedent
from typing import List

pytest_plugins = ["pytester"]


def run_and_check(command: List[str], cwd: Path) -> None:
    subprocess.run([sys.executable] + command, check=True)


def test_not_running(tmp_path):
    example = tmp_path / "example.py"
    example.write_text(
        dedent(
            """\
            import pytest_is_running
            assert not pytest_is_running.is_running()
            """
        )
    )

    run_and_check([str(example)], cwd=tmp_path)


def test_running(tmp_path):
    example = tmp_path / "example.py"
    example.write_text(
        dedent(
            """\
            import pytest_is_running
            assert pytest_is_running.is_running()

            def test_one():
                assert pytest_is_running.is_running()
            """
        )
    )

    run_and_check(["-m", "pytest", str(example)], cwd=tmp_path)


def test_running_plugin_ignored(tmp_path):
    example = tmp_path / "example.py"
    example.write_text(
        dedent(
            """\
            import pytest_is_running

            def test_one():
                assert not pytest_is_running.is_running()
            """
        )
    )

    run_and_check(["-m", "pytest", "-p", "no:is_running", str(example)], cwd=tmp_path)


def test_running_wrapper(tmp_path):
    example = tmp_path / "example.py"
    example.write_text(
        dedent(
            """\
            import pytest_is_running
            assert pytest_is_running.is_running()

            def test_one():
                assert pytest_is_running.is_running()
            """
        )
    )
    wrapper = tmp_path / "wrapper.py"
    wrapper.write_text(
        dedent(
            """\
            import pytest
            import pytest_is_running

            if __name__ == "__main__":
                assert not pytest_is_running.is_running()
                pytest.main(["example.py"])
                assert not pytest_is_running.is_running()
            """
        )
    )

    run_and_check([str(wrapper)], cwd=tmp_path)

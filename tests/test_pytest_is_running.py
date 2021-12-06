import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent
from typing import List

import pytest


@pytest.fixture()
def our_tmp_path(tmp_path):
    (tmp_path / "sitecustomize.py").write_text(
        dedent(
            """\
            import coverage
            coverage.process_startup()
            """
        )
    )
    yield tmp_path


SETUP_CFG_PATH = Path(__file__).resolve().parent.parent / "setup.cfg"


def run_and_check(command: List[str], cwd: Path) -> None:
    env = dict(
        os.environ, PYTHONPATH=str(cwd), COVERAGE_PROCESS_START=str(SETUP_CFG_PATH)
    )
    subprocess.run(
        [sys.executable] + command,
        check=True,
        env=env,
    )


def test_not_running(our_tmp_path):
    example = our_tmp_path / "example.py"
    example.write_text(
        dedent(
            """\
            import pytest_is_running
            assert not pytest_is_running.is_running()
            """
        )
    )

    run_and_check([str(example)], cwd=our_tmp_path)


def test_running(our_tmp_path):
    example = our_tmp_path / "example.py"
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

    run_and_check(["-m", "pytest", str(example)], cwd=our_tmp_path)


def test_running_plugin_ignored(our_tmp_path):
    example = our_tmp_path / "example.py"
    example.write_text(
        dedent(
            """\
            import pytest_is_running

            def test_one():
                assert not pytest_is_running.is_running()
            """
        )
    )

    run_and_check(
        ["-m", "pytest", "-p", "no:is_running", str(example)], cwd=our_tmp_path
    )


def test_running_wrapper(our_tmp_path):
    example = our_tmp_path / "example.py"
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
    wrapper = our_tmp_path / "wrapper.py"
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

    run_and_check([str(wrapper)], cwd=our_tmp_path)

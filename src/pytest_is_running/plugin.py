from __future__ import annotations

import pytest

import pytest_is_running


# pytest missing type hints for @hookimpl
@pytest.hookimpl(tryfirst=True)  # type: ignore [misc]
def pytest_load_initial_conftests() -> None:
    pytest_is_running._is_running = True


def pytest_unconfigure() -> None:
    pytest_is_running._is_running = False

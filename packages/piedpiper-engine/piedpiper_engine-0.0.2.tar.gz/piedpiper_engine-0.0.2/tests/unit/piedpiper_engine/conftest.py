import pytest

from piedpiper_engine import Engine


@pytest.fixture(scope="function")
def engine():
    engine_ = Engine()
    engine_.clear_queues()

    yield engine_

    engine_.quit()

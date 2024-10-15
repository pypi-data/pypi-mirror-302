from core.client import Client
from piedpiper_engine.engine import Engine


def test_two_clients_dont_have_same_id():
    client_1 = Client()
    client_2 = Client()

    assert client_1._id != client_2._id


def test_client_has_none_as_the_engine_initially():
    client = Client()
    assert client._engine is None


def test_client_process_adds_to_engine():
    client = Client()
    engine = Engine()

    engine.add_client(client)
    engine.add_message(client._id, "Test message")

    cq = engine._find_client_queue_(client._id)

    assert cq.get_next_message() == "Test message"
    assert cq.get_next_message() is None

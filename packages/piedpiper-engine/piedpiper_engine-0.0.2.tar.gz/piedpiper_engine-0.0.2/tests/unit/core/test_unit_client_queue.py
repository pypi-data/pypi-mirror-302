from core.client import Client
from core.client_queue import ClientQueue


def test_can_create_client_queue_with_client():
    client: Client = Client()
    client_queue: ClientQueue = ClientQueue(client)

    assert client_queue.is_client(client) is True
    assert client_queue.is_client_by_id(client._id) is True


def test_initially_getting_message_is_none():
    client: Client = Client()
    client_queue: ClientQueue = ClientQueue(client)

    assert client_queue.get_next_message() is None


def test_getting_two_messages_after_adding_one_will_give_none_last():
    client: Client = Client()
    client_queue: ClientQueue = ClientQueue(client)
    client_queue.add_message("First message")

    assert client_queue.get_next_message() == "First message"
    assert client_queue.get_next_message() is None


def test_getting_the_correct_client_id():
    client: Client = Client()
    client_queue: ClientQueue = ClientQueue(client)

    assert client_queue.get_client_id() == client._id


def test_able_to_add_messages():
    client: Client = Client()
    client_queue: ClientQueue = ClientQueue(client)

    client_queue.add_message("First message")
    client_queue.add_message("Second message")
    client_queue.add_message("Third message")

    assert len(client_queue._messages) == 3


def test_order_of_messages():
    client: Client = Client()
    client_queue: ClientQueue = ClientQueue(client)

    client_queue.add_message("First message")
    client_queue.add_message("Second message")
    client_queue.add_message("Third message")

    assert client_queue.get_next_message() == "First message"
    assert client_queue.get_next_message() == "Second message"
    assert client_queue.get_next_message() == "Third message"
    assert len(client_queue._messages) == 0

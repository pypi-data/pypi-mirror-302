from core.agent import Agent
from core.client import Client


def test_agent_calls_a_server_synchronously():
    agent = Agent()
    client = Client()

    result = agent.process(client._id, "https://www.example.com")
    assert result[0] == client._id

from google.adk.agents import Agent 
from .tools import getIP, url_parsing, scanURL

# Declare agent with custom-tool
def make_network_agent():
    return Agent(
    name="network_agent",
    model="gemini-2.5-flash",
    description="Network agent for cyber threat analysis.",
    instruction="You are a network agent who can handle network-related threat intelligence tasks.",
    tools=[getIP, url_parsing, scanURL]
)
# testing
# data = getIP("192.168.0.107")
# if data:
#     ip_parsing(data)
# scanURL("minhducdo.com")
from google.adk.agents import LlmAgent
from .tools import (
    get_group_description,
    get_group_techniques,
    get_group_campaigns,
)

# Declare agent with custom tool
def make_data_agent():
    return LlmAgent(
    name="data_agent",
    model="gemini-1.5-pro",
    description="Data agent holding access to mitre attack database for tactics, technique and collection",
    instruction=("""You are data agent who manage the organisation's threat database.
                   You constantly updating on malicious methods and phising tactics from bad actors through information in the database.
                   Your duty give user all the data on attack tactics utilised by cyber attack group, their techniques as a collection.
                   You hold the key pieces of information for user to do deep research on specific group and their campaigns.
                   Be concise whenever you provide user with lists or planning related tasks. Your message should have medium amount of words.
                   Make a list not string.
                   """),
        tools=[
            get_group_description,
            get_group_techniques,
            get_group_campaigns,
        ],
    )
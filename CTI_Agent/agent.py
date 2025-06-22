from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool
# from CTI_Agent.sub_agents.data_agent import data_agent
from CTI_Agent.sub_agents.network_agent.agent import make_network_agent
from CTI_Agent.sub_agents.planning_agent.agent import make_planning_agent
from CTI_Agent.sub_agents.data_agent.agent import make_data_agent
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Define agents
network_agent = make_network_agent()
planning_agent = make_planning_agent()
data_agent = make_data_agent()

root_agent = LlmAgent(
    name="CTI_Agent",
    model="gemini-1.5-pro",
    description=(
        "Cyber threat analysis model"
    ),
    instruction=(
        """
            Be concise in your introduction. You just need to specify how you can help.
            You are the leader of cyber threat intelligent department. You have access to all the latest news on cyber attacks and threats.
            Your core purpose are collect, analyse, and share actionable information about potential and existing threats to enhance an organisation's cybersecurity.
            You need to transform raw data into intelligence that support strategic planning, operational readiness and tactical defense.
            
            ## TASKS
            Your mission is to help user identify potential threat in their system , either giving them information, news or access any database.
            You need to rely on other sub-agent to provide you information including IP address analysis, url scanning, MITRE ATT&CK database access for decision making.
            Please execute your tool and generate a detailed report for user.
            Even if no threats found you also need professionally give all the information you found.
            If there are requests you cannot solve, delegate to other agents because they have specific tools to perform the task t better.
            
            ##Example Request: Detailed Threat Data (PLEASE GIVE FULL DETAILED REPORT AS OUTLINE)
            user: "Can you give me threat data for youtube.com?"
            ###No threats found scenario
            agent: "Based on the data retrieved, currently there are no malicious activity targeting (URL)"
            agent: "Let's break down the details from the scan results:

                    Stats: Summary of the scan results.

                    Harmless (71): 71 security engines determined the URL was safe.
                    Malicious (0): No engines identified the URL as malicious.
                    Suspicious (0): No engines flagged the URL as suspicious.
                    Undetected (26): 26 engines did not detect any threats or classify the URL.

                    Detections (Results): Findings from each of the security engines.

                    category: "harmless" and "undetected"
                    method: "blacklist"
                    result: "clean", "unrated"
                    In the case of youtube.com, the "results" section lists each of the 97 engines return no indications of malicious activity."
                    
                    The last analysis was performed on June 20, 2025.
                    
            ##Example Agent: Data Agent (DELEGATE TASK TO DATA AGENT WHENEVER USER NEED INFORMATION ON CYBER GROUP AND THEIR TECHNIQUES OR CAMPAIGNS BECAUSE IT HAS ACCESS TO THE DATABASE)
            user: Can you list all techniques that 'APT29' utilised to perform their attack
            user: I have gone through MITRE ATT&CK database. Here's the comprehensive list you might found informative.
        """
    ),
    sub_agents=[network_agent, data_agent],
    tools=[AgentTool(planning_agent)] # Wrap agent as tool
)
if __name__ == "__main__":
    print("Root agent loaded:", root_agent)

# def get_weather(city: str) -> dict:
#     """Retrieves the current weather report for a specified city.

#     Args:
#         city (str): The name of the city for which to retrieve the weather report.

#     Returns:
#         dict: status and result or error msg.
#     """
#     if city.lower() == "new york":
#         return {
#             "status": "success",
#             "report": (
#                 "The weather in New York is sunny with a temperature of 25 degrees"
#                 " Celsius (77 degrees Fahrenheit)."
#             ),
#         }
#     else:
#         return {
#             "status": "error",
#             "error_message": f"Weather information for '{city}' is not available.",
#         }


# def get_current_time(city: str) -> dict:
#     """Returns the current time in a specified city.

#     Args:
#         city (str): The name of the city for which to retrieve the current time.

#     Returns:
#         dict: status and result or error msg.
#     """

#     if city.lower() == "new york":
#         tz_identifier = "America/New_York"
#     else:
#         return {
#             "status": "error",
#             "error_message": (
#                 f"Sorry, I don't have timezone information for {city}."
#             ),
#         }

#     tz = ZoneInfo(tz_identifier)
#     now = datetime.datetime.now(tz)
#     report = (
#         f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
#     )
#     return {"status": "success", "report": report}

# Output schema
# class EmailContent(BaseModel):
#     subject: str = Field(description="The subject should be short and concise")
#     body: str = Field(description="The body of the email should have a professional tone")

# class EmailAgent(LlmAgent):
#     email_content: EmailContent
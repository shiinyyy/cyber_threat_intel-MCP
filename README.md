# Cyber Threat Intelligence (CTI Agent)
A basic multi-agent CTI model designed to support decision-making of a SOC. Each agent includes tools for scanning and generating reports on cyber threats. The architect is extensible, capable of identifying threat groups, their techniques and associated campaigns.

## GOOGLE-HACKATHON-2025
tools: google-adk, VirusTotal, MITRE ATT&CK

## Details
Activate venv
```bash
source venv/bin/activate
```

Install requirement.txt
```bash
python -m pip install -r requirement.txt
```

After .env setting
```bash
google adk
```

## Challenges:
Utilising model gemini-1.5-pro (support function calling).

The model come with the limitation of being concise for every requests, not tool calling but desired responses.  

Built-in tool cannot run alongside with custom-tool -> The agent need to be wrapped as tool.

Accessing database consumes a good amount of time, separate functions efficiently enhance performing process.

For model context, description and instruction need to be robust.
from agent.hotspot_extract_agent import hotspot_extract_agent
from agent.absurd_life_agent import absurd_life_agent

agent_store = {
    "hotspot_extract": {
        "agent": hotspot_extract_agent,
        "is_params": False
    },
    "absurd_life": {
        "agent": absurd_life_agent,
        "is_params": True,
        "param_variable": "user_input"
    }
}
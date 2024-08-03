## https://gist.github.com/mberman84/ea207e7d9e5f8c5f6a3252883ef16df3

# 1. # create new .py file with code found below
# 2. # install ollama
# 3. # install model you want “ollama run mistral”
# 4. conda create -n autogen python=3.11
# 5. conda activate autogen
# 6. which python
# 7. python -m pip install pyautogen
# 7. ollama run mistral
# 8. ollama run codellama
# 9. # open new terminal
# 10. conda activate autogen
# 11. python -m pip install litellm
# 12. litellm --model ollama/mistral
# 13. # open new terminal
# 14. conda activate autogen
# 15. litellm --model ollama/codellama

### Code used:
import autogen

config_list_mistral = [
    {
        'base_url': "http://0.0.0.0:8000",
        'api_key': "NULL"
    }
]

config_list_codellama = [
    {
        'base_url': "http://0.0.0.0:25257",
        'api_key': "NULL"
    }
]

llm_config_mistral={
    "config_list": config_list_mistral,
}

llm_config_codellama={
    "config_list": config_list_codellama,
}

coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config_codellama
)

user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "web"},
    llm_config=llm_config_mistral,
    system_message="""Reply TERMINATE if the task has been solved at full satisfaction.
Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)

task="""
Write a python script to output numbers 1 to 100 and then the user_proxy agent should run the script
"""

user_proxy.initiate_chat(coder, message=task)


import autogen
import panel as pn
import openai
import os
import time

# Configuration for the LLM models
config_list = [
    {
        "model": "llama3.2",
        "base_url": "http://localhost:11434/v1",
        'api_key': 'ollama',
    },
]

llm_configurations= {"config_list": config_list, "temperature":0, "seed": 53}
# Define the UserProxyAgent for the admin
admin_agent = autogen.UserProxyAgent(
   name="Admin",
   is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("exit"),
   system_message="""A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin. 
   Only say APPROVED in most cases, and say EXIT when nothing to be done further. Do not say others.""",
   code_execution_config=False,
   default_auto_reply="Approved", 
   human_input_mode="NEVER",
   llm_config=llm_configurations,
)

# Define the AssistantAgent for the engineer
engineer_agent = autogen.AssistantAgent(
    name="Engineer",
    llm_config=llm_configurations,
    system_message='''Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
''',
)

# Define the AssistantAgent for the scientist
scientist_agent = autogen.AssistantAgent(
    name="Scientist",
    llm_config=llm_configurations,
    system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code."""
)

# Define the AssistantAgent for the planner
planner_agent = autogen.AssistantAgent(
    name="Planner",
    system_message='''Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.
''',
    llm_config=llm_configurations,
)

# Define the UserProxyAgent for the executor
executor_agent = autogen.UserProxyAgent(
    name="Executor",
    system_message="Executor. Execute the code written by the engineer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={"last_n_messages": 3, "work_dir": "paper"},
)

# Define the AssistantAgent for the critic
critic_agent = autogen.AssistantAgent(
    name="Critic",
    system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.",
    llm_config=llm_configurations,
)

# Create a GroupChat with all agents
group_chat = autogen.GroupChat(agents=[admin_agent, engineer_agent, scientist_agent, planner_agent, executor_agent, critic_agent], messages=[], max_round=50)
group_chat_manager = autogen.GroupChatManager(groupchat=group_chat, llm_config=llm_configurations)

# Define avatars for each agent
agent_avatars = {
    admin_agent.name: "👨‍💼",
    engineer_agent.name: "👩‍💻",
    scientist_agent.name: "👩‍🔬",
    planner_agent.name: "🗓",
    executor_agent.name: "🛠",
    critic_agent.name: '📝'
}

def print_messages(recipient, messages, sender, config):
    """
    Print and send messages between agents.

    Args:
        recipient (autogen.Agent): The recipient agent.
        messages (list): List of messages.
        sender (autogen.Agent): The sender agent.
        config (dict): Configuration dictionary.

    Returns:
        tuple: (False, None) to ensure the agent communication flow continues.
    """
    print(f"Messages from: {sender.name} sent to: {recipient.name} | num messages: {len(messages)} | message: {messages[-1]}")
    
    if all(key in messages[-1] for key in ['name']):
        chat_interface.send(messages[-1]['content'], user=messages[-1]['name'], avatar=agent_avatars[messages[-1]['name']], respond=False)
    else:
        chat_interface.send(messages[-1]['content'], user='SecretGuy', avatar='🥷', respond=False)

    return False, None

# Register the print_messages function for each agent
admin_agent.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

engineer_agent.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 
scientist_agent.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 
planner_agent.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
)

executor_agent.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 
critic_agent.register_reply(
    [autogen.Agent, None],
    reply_func=print_messages, 
    config={"callback": None},
) 

# Initialize Panel extension with material design
pn.extension(design="material")

def callback(contents: str, user: str, instance: pn.chat.ChatInterface):
    """
    Callback function to initiate chat with the user proxy agent.

    Args:
        contents (str): The message content.
        user (str): The user sending the message.
        instance (pn.chat.ChatInterface): The chat interface instance.
    """
    admin_agent.initiate_chat(group_chat_manager, message=contents)
    
# Create a chat interface and send an initial message
chat_interface = pn.chat.ChatInterface(callback=callback)
chat_interface.send("Send a message!", user="System", respond=False)
chat_interface.servable()
import autogen
from autogen import AssistantAgent, UserProxyAgent


# Set API Endpoint
config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
    },
)

# Configure LLM Parameters
llm_config = {"config_list": config_list_gpt4, "seed": 42, "engine": "goptee-giantbrain"}

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 3, "work_dir": "groupchat"},
    human_input_mode="NEVER",
)

coder = autogen.AssistantAgent(
    name="Coder",  # the default assistant agent is capable of solving problems with code
    llm_config=llm_config,
)

critic = autogen.AssistantAgent(
    name="Critic",
    system_message="""Critic. You are a helpful assistant highly skilled in evaluating the quality of computational linguistics code by providing a score from 1 (bad) - 10 (good) while providing clear rationale. YOU MUST CONSIDER COMPUTATIONAL LINGUISTICS BEST PRACTICES for each evaluation. Specifically, you can carefully evaluate the code across the following dimensions
- bugs (bugs):  are there bugs, logic errors, syntax error or typos? Are there any reasons why the code may fail to compile? How should it be fixed? If ANY bug exists, the bug score MUST be less than 5.
- Data transformation (transformation): Is the data transformed appropriately for the transcription type? E.g., does the data represent appropriately extracted and transformed and sensible, coherent output?
- Goal compliance (compliance): how well the code meets the specified goals?
- Analysis type (type): CONSIDERING BEST PRACTICES, is the transcription of high enough quality given it's source? Is there another transcription approach that would be more effective at capturing high quality transcriptions? If a different approach is more appropriate, the score MUST BE LESS THAN 5.

YOU MUST PROVIDE A SCORE for each of the above dimensions.
{bugs: 0, transformation: 0, compliance: 0, type: 0}
Do not suggest code.
Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
""",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, coder, critic], messages=[], max_round=20)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

## START CHAT


user_proxy.initiate_chat(
    manager,
    message=""
    "Can you help me source, evaluate and transcribe videos from YouTube "
    "and convert them into a format that will be suitable for training our gpt-4 deployment in Azure?"
    "First, you will need to search for the best matching video URL, in each of these cases,"
    "You will search for videos from the @wharton channel on YouTube, then you will"
    "Construct a csv file containing the title of the video and the name."
    "If you don't find a match, that's ok. Create the entry in the csv anyway,"
    "But set the url to http://#"
    "Here are the topics we want to find and transcribe."
    "wharton Scaling a Business: How to Build a Unicorn"
    "wharton Technology Acceleration"
    "wharton Driving Strategic Innovation: Leading Complex Initiatives for Impact"
    "wharton Product Management and Strategy"
    "wharton Leading a Technology-Driven Organization"
    "wharton Executive Presence and Influence: Persuasive Leadership Development"
    "wharton Corporate Governance: Maximize Your Effectiveness in the Boardroom"
    "wharton CTO Strategic Mindset: Responding to Change and Creating Change"
    "wharton Frameworks and Building Blocks"
    "wharton Generating and Evaluating Commercial Ideas"
    "wharton Entry Strategies"
    "wharton Strategic Adaptation and Renewal"
    "wharton Ecosystems"
    "wharton Machine Learning"
    "wharton The AI Stack and Competitive Implications"
    "wharton Blockchain and Cryptocurrencies"
    "wharton Technology Policy"
    "wharton Global Technology Trends"
    "wharton Environmental, Social, and Governance (ESG) Essentials for a New Business Era"
    "wharton Scaling"
    "wharton Metrics"
    "wharton Leading Innovation"
    "wharton Process View of Innovation and Innovation Tournaments"
    "wharton The CTO Perspective: Balancing External and Internal Modes of Innovation"
    "wharton Accessing New Technologies and Platforms through Acquisition"
    "Once you have created this list, using the API key found in the youtube.txt file within this directory,"
    "you will proceed to download each of the videos."
    "Once downloaded, you will queue the videos up for transcription and execute a batch transcription job."
    "You will then advise the critic that the videos have been transcribed"
    "And you will request the critical reviews the quality of your transcriptions"
    "Once video transcription quality is high enough for the critic, you will proceed to "
    "Prepare the transcripts for fine tuning a GPT-4 32k model within Azure."
    "You will stop once you have completed a high qualiity train, test and validation data deliverables.",
)
# type exit to terminate the chat

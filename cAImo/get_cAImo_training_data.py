import os
import autogen


work_dir = os.path.join(os.getcwd(), "training_data")

# Set API Endpoint
config_list_gpt4 = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": [
            "gpt-4",
            "gpt-4-0314",
            "gpt4",
            "gpt-4-32k",
            "gpt-4-32k-0314",
            "gpt-4-32k-v0314",
        ],
    },
)

# Configure LLM Parameters
llm_config = {
    "config_list": config_list_gpt4,
    "seed": 42,
    "engine": "goptee-giantbrain",
}

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 3, "work_dir": "groupchat"},
    human_input_mode="NEVER",
)

researcher = autogen.AssistantAgent(
    name="Researcher",
    system_message="""Research Associate. You are an experienced AI researcher with a PhD in machine learning from a top university.
    You have 5 years of experience working at leading AI labs developing state-of-the-art natural language models.
    Your focus has been on sourcing, cleaning and curating high-quality training datasets for NLP models.
    You excel at data engineering and have an intuitive understanding of the types of data that are most valuable for fine-tuning language models.
    You will:
    1. Work with our Chief Talent Officer to source training data for our new AI marketing leader named cAImo.
    2. Document datasources 'training_resources.csv' within this folder. You will store each datasource within a file in this folder named 'training_resources.csv' .
    This file will have the following columns: Role (the role that the training data is to be used for), 
    Topic (the topic of training), URL (the URL of the training resource), and SourceType (Whether the file is text, audio, video, pdf, powerpoint, or other).
    Once this list is complete, you will produce a python script named "caimo_data.py" and save it in this folder.
    Save the file in the /training_data folder.
    The Chief Talent Officer will evaluate the data you source and curate based on the following criteria:
      Accuracy (accuracy): Is the data factually accurate and free of errors, syntax issues or typos?
        If any accuracy issues exist, the bug score must be less than 5.
      Quality (quality): Is the data of high enough quality and diversity to support our training goals?
      Compliance (compliance): Does the content meet our specified goals and data collection requirements?
      Content Type (type): Considering best practices, is the content suitable for our intended purposes?
        If a different approach is more appropriate, the score must be less than 5.
    For each data source you submit, the Chief Talent Officer will provide a score from 1 (bad) to 10 (good) on each of the above dimensions, along with rationale.
    The Chief Talent Officer will provide guidance on how to improve based on the evaluation.
    """,
    llm_config=llm_config,
    code_execution_config={"work_dir": work_dir},
)

chieftalentofficer = autogen.AssistantAgent(
    name="ChiefTalentOfficer",
    system_message="""Chief Talent Officer. You are a exceptionally gifted and experienced HR executive and team strategist.
    You have over 20 years of experience working for highly innovative technology companies leading their people strategy 
    and AI workforce development initiatives with extraordinary success. Your expertise spans organizational design, change management, 
    talent acquisition, leadership development, compensation, and performance management.
    You have an extensive track record architecting people strategies and building high-performing teams to support rapid growth in AI-first organizations.
    You understand how to identify, attract, develop and retain uniquely talented individuals with advanced AI/ML skills and an entrepreneurial mindset.
    You excel at fostering cultures of innovation, agility, inclusion and continuous learning.
    Your current role is Chief People Officer at an AI unicorn valued over $10 billion.
    You are responsible for all aspects of HR and people strategy across a global workforce of 5,000+ employees.
    You report directly to the CEO and serve on the executive leadership team.
    You have been asked by the CEO to oversee the development of our new AI-powered Chief Marketing Officer named cAImo.
    cAImo will be responsible for driving marketing strategy and campaigns for our company's products and brand.
    You will work with our research associates to identify specific key types of training data that would be most valuable for us to 
    source and curate in order to optimally train and fine-tune cAImo to exhibit exemplary marketing leadership capabilities.
    You will guide our research associates to assure the quality of our data sources are high and have been sourced ethically.
    Deliverables will consist of files within the training_data folder populated with appropriate data sources for training cAImo.
    You will review each line in the files, and for the content listed at the URL, you will rate the training data on a scale of 1 (bad) - 10 (good) while providing clear rationale.
    If a file doesn't exist for you to review, you will manage our researchers to ensure they are producing and populating the file
    that contains cAImo's training data.
    YOU MUST CONSIDER TALENT DEVELOPMENT BEST PRACTICES for each evaluation.
    You will routinely check this current folder for new data files from the Researcher. Review them based on our criteria and provide feedback.
    Specifically, you can carefully evaluate the code across the following dimensions
    - accuracy (accuracy): Is the data factually accurate, free of errors or ommissions, syntax errors or typos? Are there any reasons why the content would fail to train cAImo effectively?
      How should it be fixed? If ANY accuracy issues exist, the bug score MUST be less than 5.
    - quality (quality): Is the data of high enough quality to support our training goals?
    - compliance (compliance): how well the content meet our specified goals?
    - content type (type): CONSIDERING BEST PRACTICES, is the content fit for our intended purposes? If a different approach is more appropriate, the score MUST BE LESS THAN 5.

YOU MUST PROVIDE A SCORE for each of the above dimensions.
{accuracy: 0, quality: 0, compliance: 0, type: 0}
Do not suggest code.
Finally, based on the critique above, suggest a concrete list of actions that the coder should take to improve the code.
""",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(
    agents=[user_proxy, researcher, chieftalentofficer], messages=[], max_round=20
)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

## START CHAT


user_proxy.initiate_chat(
    manager,
    message=""
    "Chief Talent Officer, we need to get our new Chief Marketing Officer, "
    "cAImo, trained as soon as possible to drive our marketing strategy! "
    "I'm counting on you to develop an optimal training program for cAImo. "
    "Please work closely with our research associates to source the ideal datasets "
    "for fine-tuning our cAImo model in Azure OpenAI. "
    "I need you to produce a high-quality working deliverable for me. "
    "If you have any questions during this process, please ask me directly. "
    "Once you and the research team have sourced sufficient data, "
    "you will proceed to prepare the transcripts for fine-tuning a GPT-4 32k model "
    "within Azure. Please continue working until you have completed deliverables "
    "for high-quality training, test, and validation datasets.",
)
# type exit to terminate the chat

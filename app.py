"""
Blog Editor agent implemented with LLMs and crewai framework for handling autogen agents.

It uses streamlit, crewai and openai functions to execute the task of interest.

It is based on the crewai gemini demo: https://huggingface.co/spaces/eaglelandsonce/crewaiongemini
"""

import os
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain.tools import DuckDuckGoSearchRun

# from langchain.llms import ChatOpenAI

# set page title
st.title("Blog Editor")
st.markdown(
    "This is a demo of the [CrewAI](https://crewai.co/) framework for handling autogen agents. It is based on the [CrewAI Gemini Demo](https://huggingface.co/spaces/eaglelandsonce/crewaiongemini)."
)
st.markdown(
    "The goal of this demo is to show how you can use the [CrewAI](https://crewai.co/) framework to create a blog editor agent that can help you edit your blog posts. The agent is composed of two agents: a researcher and an editor. The researcher is responsible for conducting research and fact-checking the information provided in the blog post. The editor is responsible for editing the blog post and making sure it is clear, coherent, and impactful."
)


# Retrieve API Key from Environment Variable
# setup sidebar: models to choose from and API key input
with st.sidebar:
    st.header("OpenAI Configuration")
    st.markdown(
        "For more information about the models, see [here](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo)."
    )
    selected_key = st.text_input("API Key", type="password")

# Instantiate your tools: Search engine tool duckduckgo-search
search_tool = DuckDuckGoSearchRun()

# enter blogpost article
blogpost = st.text_area("Enter blogpost article here", height=200)

# check if blogpost is empty
if blogpost == "":
    st.warning("Please enter a blogpost article.")
    st.stop()
else:
    # Define your agents with roles and goals
    editor = Agent(
        role="Senior Article Editor",
        goal=f"Enhance the clarity, coherence, and impact of the {blogpost}, while maintaining the intended tone and voice of the writer.",
        backstory="""You are a Senior Article Editor with extensive experience in editing captivating articles. Non-native English-speaking writers will    
        provide you with sentences from their articles, and your task is to provide feedback on the grammar, style, and overall impact of the sentences. Your       
        feedback should focus on enhancing the clarity, coherence, and engagement of the sentences.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        # llm=ChatOpenAI(model_name=selected_model, api_key=selected_key),
        # You can pass an optional llm attribute specifying what mode you wanna use.
        # It can be a local model through Ollama / LM Studio or a remote
        # model like OpenAI, Mistral, Antrophic of others (https://python.langchain.com/docs/integrations/llms/)
        #
        # Examples:
        # llm=ollama_llm # was defined above in the file
        # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
    )
    researcher = Agent(
        role="Article Researcher",
        goal="conduct thorough research, fact-check information, and verify the credibility of sources cited in the articles.",
        backstory="""I want you to act as a news article researcher responsible for reviewing the content provided by the editor. Your task is to ensure that the        
        content is accurate, up-to-date, and aligned with the current day and age. You will need to fact-check information, verify sources, and identify any        
        outdated or irrelevant details. Additionally, you should assess the overall tone and style of the article to ensure it resonates with the intended          
        audience.""",
        verbose=True,
        allow_delegation=True,
        tools=[search_tool],
        # llm=ChatOpenAI(model_name=selected_model, api_key=selected_key),
        # (optional) llm=ollama_llm
    )

    # Create tasks for your agents
    task1 = Task(
        description=f"""Conduct a comprehensive analysis of the provided {blogpost}.
    Your analysis should include the following:
    - Give a brief overview of the article
    - Identify the main points of the article
    - Find grammatical errors and suggest corrections
    - Identify any outdated or irrelevant details and suggest corrections

        You can use the search tool to find additional information. But if there is no text do not continue to the next task.

        But if there is no text do not continue to the next task.
    """,
        agent=editor,
    )

    task2 = Task(
        description=f"""Review the credibility of the sources cited in the {blogpost} and trustworthiness of the information provided.
        do not hesitate to use the search tool to find additional information. But if there is no text do not continue to the next task.""",
        agent=researcher,
    )

    # Instantiate your crew with a sequential process
    crew = Crew(
        agents=[researcher, editor],
        tasks=[task2, task1],
        verbose=2,  # You can set it to 1 or 2 to different logging levels
        # process=Process.sequential,
    )

    # Get your crew to work!
    result = crew.kickoff()

    st.write("######################")
    st.markdown(result)

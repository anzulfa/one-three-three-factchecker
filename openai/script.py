'''
pip install langchain
pip install openai
pip install google-search-results

'''

from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import load_tools

openai_api = 'OPENAI_API_GOES_HERE'
serpapi_api = 'SERPAPI_API_GOES_HERE'

llm = OpenAI(temperature=0,openai_api_key=openai_api)
tools = load_tools(["serpapi", "llm-math"], llm=llm,serpapi_api_key=serpapi_api)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

query = "Is this factually true? Does Microsoft invest to ChatGPT."
agent.run(query)
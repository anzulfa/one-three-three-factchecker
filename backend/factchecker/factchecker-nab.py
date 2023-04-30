from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import load_tools
import contextlib
import io
import re

captured_output = io.StringIO()

serpapi_api = 'a588596ca9b650d44158b6d68975eda8e1b19a25e0c06ddeddcf1d6ee766fc66'

llm = OpenAI(temperature=0, model_name = 'gpt-3.5-turbo', openai_api_key='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')
tools = load_tools(["serpapi", "llm-math"], llm=llm,serpapi_api_key=serpapi_api)
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
# agent = initialize_agent(tools, llm, verbose=True)

query = '''
You are a professional article fact checker. 
Can you fact check this article: "{url}"
Perform the fact check by listing down the "factual" statements that the article author claim to be true into bullet points, and present this points.
Then for each point, find out whether they are true by cross checking with other websites.
Finally, present the end result by giving a verdict for each point whether they are true or not, and also present the website used for the cross check.
'''
with contextlib.redirect_stdout(captured_output):
    agent.run(query.format(url = "https://edition.cnn.com/2021/06/09/tech/robot-zaps-weeds-spc-intl/index.html" ))

captured_string = captured_output.getvalue()
print("captured string --> ")
print(captured_string)
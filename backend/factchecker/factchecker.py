import os
from flask import Flask
from flask import jsonify
from flask import request
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI
from langchain.agents import load_tools
from flask_cors import CORS
import contextlib
import io
import re

app = Flask(__name__)
CORS(app)

# API Key
openai_api_key = os.environ['OPENAI_API_KEY']
serpapi_api_key = os.environ['SERPAPI_API_KEY']

# Pre-compiled variable
ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
prompt_factcheck = '''
    You are a professional article fact checker. 
    Can you fact check this article: "{url}"
    Perform the fact check by listing down the "factual" statements that the article author claim to be true into bullet points, and present this points.
    Then for each point, find out whether they are true by cross checking with other websites.
    Finally, present the end result by giving a verdict for each point whether they are true or not, and also present the website used for the cross check.
    '''
prompt_score = ''' You are an article scorer. An article fact checker gave his review on this article:
    "{article_final}" from url {url} 
    in a score of 1-100, how would you score this article based on its correctness?
    '''

@app.route("/check-fact", methods=['POST'])
def ask():
    # Extract request
    reqJson = request.get_json()
    print("Check fact for page url: " + reqJson['pageUrl'])

    # Call OpenAI for inference
    llm = OpenAI(temperature=0, model_name = 'gpt-3.5-turbo', openai_api_key=openai_api_key)
    tools = load_tools(["serpapi", "llm-math"], llm=llm,serpapi_api_key=serpapi_api_key)
    agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    # agent = initialize_agent(tools, llm, verbose=True)

    # Run agent, capture agent internal stdout to variable
    captured_output = io.StringIO()
    article_final = None
    with contextlib.redirect_stdout(captured_output):
        article_final = agent.run(prompt_factcheck.format(url = reqJson['pageUrl']))
        score_final = llm(prompt_score.format(article_final = article_final, url = reqJson['pageUrl']))
    agent_run_result = captured_output.getvalue()
    agent_run_result = ansi_escape.sub('', agent_run_result)

    print("article final: ", str(article_final))
    print('score final: ', str(score_final))

    # Process agent result and generate response
    resultDict = {
        "shortSummary": article_final,
        "summary": article_final,
        "score": "",
        "processChain": extract_process_chain(agent_run_result)
    }

    responseBody = {
        "success": "true",
        "message": "",
        "hotel": "traveloka",
        "pageUrl": reqJson['pageUrl'],
        "result": resultDict
    }

    # Return response to client
    response = jsonify(responseBody)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Extract stdout for AI thought process
def extract_process_chain(text_input):
    print('Raw text input: ' + text_input)
    result = ansi_escape.sub('', text_input)
    result = result.replace("\n","")
    result = result.replace("> Finished chain.","")
    result = result.split("Final Answer:")[0]
    result_array = result.split("Action: ")

    final_result_list = []
    for r in range(len(result_array)):
        res = result_array[r]
        if "Observation" not in res:
            continue

        observation = re.search('Observation:(.*)Thought', res).group(1)
        thought = re.search('Thought:(.*)', res).group(1)
        final_result_list.append({ 'id': r, 'observation': observation, 'thought': thought })
        
    return final_result_list

if __name__ == '__main__':
    print("Running app on port 8080...")
    from waitress import serve
    serve(app, host="127.0.0.1", port=8080)

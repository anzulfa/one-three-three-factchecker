import os
from flask import Flask
from flask import jsonify
from flask import request
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain import LLMChain

api_key = os.environ['OPENAI_API_KEY']
template = """Summarize this page {pageUrl} in bullets"""

davinci = OpenAI(model_name='text-davinci-003', openai_api_key=api_key)

app = Flask(__name__)


@app.route("/check-fact", methods=['POST'])
def ask():
    reqJson = request.get_json()
    print(reqJson)
    print("Page url: " + reqJson['pageUrl'])

    prompt = PromptTemplate(
        template=template,
        input_variables=['pageUrl']
    )
    llm_chain = LLMChain(
        prompt=prompt,
        llm=davinci
    )

    result = llm_chain.run(reqJson['pageUrl'])

    # Parse result and summarize
    rawResultList = result.replace('\n\n', '').split('• ')
    resultList = []
    for rawResultItem in rawResultList:
        if (rawResultItem):
            resultList.append(rawResultItem.strip())
    
    for r in resultList:
        print('- ' + r)

    sampleDict = {
        "success": "true",
        "hotel": "trivago",
        "pageUrl": reqJson['pageUrl'],
        "factList": resultList
    }
    return jsonify(sampleDict)


if __name__ == '__main__':
    print("Running app on port 8080...")
    from waitress import serve
    serve(app, host="127.0.0.1", port=8080)

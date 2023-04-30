import re

text_string = """\n\n[1m> Entering new AgentExecutor chain...[0m\n[32;1m[1;3mI need to use the Search tool to find other websites that can verify the factual statements in the article.\nAction: Search\nAction Input: \"robot zaps weeds cnn article fact check\"[0m\nObservation: [36;1m[1;3mSmall Robot says robot Tom can scan 20 hectares (49 acres) a day, collecting data which is then used by Dick, a “crop-care” robot, to zap weeds.[0m\nThought:[32;1m[1;3mI need to cross check the statement \"robot Tom can scan 20 hectares (49 acres) a day\" with other websites.\nAction: Search\nAction Input: \"robot Tom scan 20 hectares a day\"[0m\nObservation: [36;1m[1;3mTom is a scanning robot that lives on the farm covering 20 Hectares/day. Soon he will be fully autonomous, living in his own kennel equipped with battery ...[0m\nThought:[32;1m[1;3mI need to cross check the statement \"Dick, a 'crop-care' robot, can zap weeds\" with other websites.\nAction: Search\nAction Input: \"crop-care robot Dick zaps weeds\"[0m\nObservation: [36;1m[1;3mSmall Robot says robot Tom can scan 20 hectares (49 acres) a day, collecting data which is then used by Dick, a “crop-care” robot, to zap ...[0m\nThought:[32;1m[1;3mBased on the cross checks, the factual statements in the article seem to be true.\nFinal Answer: The factual statements in the article are true.[0m\n\n[1m> Finished chain.[0m\n"""

ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
result = ansi_escape.sub('', text_string)
result = result.replace("\n","")
result = result.replace("> Finished chain.","")
result_array = result.split("Action: ")

final_result_list = []
for res in result_array:
    if "Observation" not in res:
        continue

    observation = re.search('Observation:(.*)Thought', res).group(1)
    print(observation)
    thought = re.search('Thought:(.*)', res).group(1)
    print(observation)
    final_result_list.append({ 'observation': observation, 'thought': thought })

# print(result)
# print(final_result_list)

for fr in final_result_list:
    print(fr)
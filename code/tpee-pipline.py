from utils import load_config, split_content, extract_steps, ActionTree, process_array, extract_steps_to_val
import json
from openai import OpenAI
import ast

# Load configuration
cfg = load_config()
current_state = cfg["current_state_index"]-1
state_to_ini = {
    0: "Ini_1",
    1: "Ini_2",
    2: "Ini_3",
    3: "Ini_4"
}
ini_key = state_to_ini.get(current_state, "Ini_1")

# read the initial state
with open(cfg["dataset"]["initial_state_url"], 'r', encoding='utf-8') as file:
    data = json.load(file)
    Ini = data[current_state]

# read the in-context examples
with open(cfg["dataset"]["in_context_examples_url"], 'r', encoding='utf-8') as file:
    exampleData = json.load(file)

# read the decomposition prompt and insert initial state
with open(cfg["prompt"]["decomposition_prompt_url"], 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        if "(In-Context Examples)" in line:
            del lines[i+1]
            del lines[i-2:i] # remove the comment section of the original prompt
            lines.insert(i-3, str(Ini)+"\n") # insert initial state
            insert_pos = i # start to insert In-Context Examples
            for record in exampleData:
                lines.insert(insert_pos, "Task:" + record['task'] + '\n')
                insert_pos += 1
                lines.insert(insert_pos, record[ini_key] + '\n')
                insert_pos += 1
            break

# save temporary file, and read the content as String
with open(cfg["save_url"]+"dectemp.txt", 'w+', encoding='utf-8') as file:
    file.writelines(lines)
    file.seek(0)
    content = file.read()

# split systemPrompt and userPrompt
systemdecPrompt, userdecPrompt = split_content(content,"(Initial Observation)")

# read the select prompt and insert initial state
with open(cfg["prompt"]["select_prompt_url"], 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        if "(Select)" in line:
            del lines[-1]
            del lines[i-2:i] # remove the comment section of the original prompt
            lines.insert(i-3, str(Ini)+"\n") # insert initial state

# save temporary file, and read the content as String
with open(cfg["save_url"]+"selecttemp.txt", 'w+', encoding='utf-8') as file:
    file.writelines(lines)
    file.seek(0)
    content = file.read()

# split systemPrompt and userPrompt
systemselectPrompt, userselectPrompt = split_content(content,"(Initial Observation)")

# read the select prompt and insert initial state
with open(cfg["prompt"]["rewrite_prompt_url"], 'r', encoding='utf-8') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        if "(Rewrite)" in line:
            del lines[-1]
            del lines[i-2:i] # remove the comment section of the original prompt
            lines.insert(i-3, str(Ini)+"\n") # insert initial state

# save temporary file, and read the content as String
with open(cfg["save_url"]+"rewritetemp.txt", 'w+', encoding='utf-8') as file:
    file.writelines(lines)
    file.seek(0)
    content = file.read()

# split systemPrompt and userPrompt
systemrewritePrompt, userrewritePrompt = split_content(content,"(Initial Observation)")

# read in tasks
with open(cfg["dataset"]["golden_plan_url"], 'r', encoding='utf-8') as file:
    taskList = json.load(file)

# planning tasks
with open(cfg["save_url"]+"result.txt", 'w', encoding='utf-8') as file:
    for task in taskList:
        # plan sampling
        print("Processing task id:"+task['id'])
        client = OpenAI(
        base_url = cfg["model"]["base_url"],
        api_key=cfg["model"]["api_key"])
        completion = client.chat.completions.create(
            model=cfg["model"]["name"],
            messages=[
                {"role": "system", "content": systemdecPrompt},
                {"role": "user", "content": userdecPrompt + task['task']}
            ],
            temperature = cfg["model"]["temperature"],
            top_p = cfg["model"]["top_p"],
            n = 1 if cfg["model"]["count"] < 1 else cfg["model"]["count"]
        )
        print("Plan sampling completed for task id:"+task['id']+ "\n\n")

        plans = []
        for i, choice in enumerate(completion.choices):
            result = choice.message.content
            plan = extract_steps(result)
            plans.append(plan)

        # # candidate sequence visualization
        # action_tree = ActionTree()
        # action_tree.construct_from_plans(plans)
        # action_tree.visualize(save_path=cfg["save_url"]+"candidate-sequence/"+task['id'])

        # choose the best plan
        completion = client.chat.completions.create(
            model=cfg["model"]["name"],
            messages=[
                {"role": "system", "content": systemselectPrompt},
                {"role": "user", "content": userselectPrompt+'\n'+"Task:"+task['task']+ '\n' + str(plans)},
            ],
            temperature = cfg["model"]["temperature"],
            top_p = cfg["model"]["top_p"]
        )
        result = completion.choices[0].message.content
        arr = ast.literal_eval(result)
        result = process_array(arr)
        file.write("id:"+task['id']+"\n"+"initial plan:"+"\n"+result + "\n\n")
        print("Best plan selected for task id:"+task['id']+ "\n\n")

        # rewrite the plan
        i=0
        while True:
            plan=extract_steps_to_val(result)
            completion = client.chat.completions.create(
                model=cfg["model"]["name"],
                messages=[
                    {"role": "system", "content": systemrewritePrompt},
                    {"role": "user", "content": userrewritePrompt+'\n'+"Task:"+task['task']+'\n'+plan},
                ],
                temperature=cfg["model"]["temperature"],
                top_p=cfg["model"]["top_p"],
            )
            result = completion.choices[0].message.content
            i+=1
            if(i>=12):
                break
        file.write("id:"+task['id']+"\n"+"final plan:"+"\n"+ result + "\n\n")
        print("Plan rewrite completed for task id:"+task['id'] + "\n\n")

        # event extract
        


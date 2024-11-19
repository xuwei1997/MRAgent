from mragent import MRAgent
import json
from key import AI_key


def accuracy(paperjson, paperllm):
    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0

    # Iterate over keys in paperjson
    for key in paperjson:
        true_value = paperjson[key]
        predicted_value = paperllm.get(key, 'no')  # Default to 'no' if key not in paperllm

        if true_value == 'yes':
            if predicted_value == 'yes':
                true_positive += 1
            else:
                false_negative += 1
        else:
            if predicted_value == 'yes':
                false_positive += 1
            else:
                true_negative += 1

    # Calculate metrics
    accuracy = (true_positive + true_negative) / len(paperjson)
    precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) > 0 else 0
    recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }


def model_test(model, paper_json_list, paper_title_list, key=AI_key, url='https://api.gpt.ge/v1/'):
    with open('MRAgentTest2STROBEMR/STROBE-MR-llm-result.txt', 'a') as f:
        f.write('model: ' + model + '\n')
    agent = MRAgent(LLM_model=model, AI_key=key, base_url=url, outcome='None')
    for paper_title, paper_json in zip(paper_title_list, paper_json_list):
        paper_llm = agent.STROBE_MR(paper_title)
        acc = accuracy(paper_json, paper_llm)
        print(paper_title)
        print(paper_llm)
        print(acc)
        # 追加写入同一个文件
        with open('MRAgentTest2STROBEMR/STROBE-MR-llm-result.txt', 'a') as f:
            f.write(json.dumps(paper_llm) + '\n')
            f.write(json.dumps(acc) + '\n')


def main():
    # 读取MRAgentTest2STROBEMR/STROBE-MR-hum.txt，每一行都是json格式，共5行代表5篇文章
    with open('MRAgentTest2STROBEMR/STROBE-MR-hum.txt', 'r') as f:
        hum_list = f.readlines()

    paper1title = 'Causal relationship between type 2 diabetes and glioblastoma: bidirectional Mendelian randomization analysis'
    paper1json = json.loads(hum_list[0])

    paper2title = 'Association between gut microbiota and preeclampsia-eclampsia: a two-sample Mendelian randomization study'
    paper2json = json.loads(hum_list[1])

    paper3title = 'The association between human papillomavirus and bladder cancer: Evidence from meta‐analysis and two‐sample mendelian randomization'
    paper3json = json.loads(hum_list[2])

    paper4title = 'Relationship between alcohol consumption and dementia with Mendelian randomization approaches among older adults in the United States'
    paper4json = json.loads(hum_list[3])

    paper_title_list = [paper1title, paper2title, paper3title, paper4title]
    paper_json_list = [paper1json, paper2json, paper3json, paper4json]

    # 调用各个模型进行测试
    # model_test('gpt-4o', paper_json_list, paper_title_list)
    # model_test('gpt-3.5-turbo', paper_json_list, paper_title_list) # not working
    # model_test('gpt-4-turbo', paper_json_list, paper_title_list)
    # model_test('claude-3-haiku-20240307', paper_json_list, paper_title_list) # not working
    # model_test('qwen-max-0403', paper_json_list, paper_title_list, key='') # not working
    model_test('meta/llama3-70b-instruct', paper_json_list, paper_title_list, key='',
               url="https://integrate.api.nvidia.com/v1")  # not working
    model_test('mistralai/mixtral-8x22b-instruct-v0.1', paper_json_list, paper_title_list, key='',
               url="https://integrate.api.nvidia.com/v1")  # 3 not working


if __name__ == '__main__':
    main()

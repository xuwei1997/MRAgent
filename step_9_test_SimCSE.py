import os
import pandas as pd
from simcse import SimCSE


def main(llm_name):
    print(llm_name)
    path = 'MRAgentTest9-SimCSE'

    with open(os.path.join(path, 'result.txt'), 'a') as f:
        f.write('\n')
        f.write(llm_name + ': \n')

    step9_path = os.path.join(path, 'mr_run_s9.csv')
    df = pd.read_csv(step9_path)
    # print(df)

    avg_list = []

    # 逐行获取df中的Outcome	Exposure	Outcome_id	Exposure_id
    for index, row in df.iterrows():

        Outcome = row['Outcome']
        Exposure = row['Exposure']
        Outcome_id = row['Outcome_id']
        Exposure_id = row['Exposure_id']
        print(Outcome, Exposure, Outcome_id, Exposure_id)

        # 文件夹
        oe_path = os.path.join(path, Exposure + '_' + Outcome + '_' + Exposure_id + '_' + Outcome_id)
        print(oe_path)
        # 取llm_name文件的txt
        txt_path = os.path.join(oe_path, llm_name + '_LLM_result.txt')

        # 判断文件是否存在
        if not os.path.exists(txt_path):
            print('No such file or directory:', txt_path)
            continue

        with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
            txt = f.read()
            print(txt)

        # 取人类手工标注的MR结果
        human_path = os.path.join(path, Exposure + '_' + Outcome + '.txt')
        with open(human_path, 'r', encoding='utf-8', errors='replace') as f:
            human = f.read()
            print(human)

        # txt and human 计算
        # SimCSE
        # model = SimCSE("princeton-nlp/unsup-simcse-roberta-large")
        model = SimCSE("princeton-nlp/unsup-simcse-bert-large-uncased")
        out = model.similarity(txt, human)
        print(out)

        avg_list.append(out)

        # 保存结果txt文件
        with open(os.path.join(path, 'result.txt'), 'a') as f:
            # f.write(llm_name + ': \n')
            # 写入Outcome, Exposure
            f.write('Outcome: ' + Outcome + '\n')
            f.write('Exposure: ' + Exposure + '\n')
            f.write(str(out) + '\n')

    # 求平均值
    avg = sum(avg_list) / len(avg_list)
    print(avg)
    with open(os.path.join(path, 'result.txt'), 'a') as f:
        f.write('avg: ' + str(avg) + '\n')




if __name__ == '__main__':
    main('gpt-3.5-turbo')
    main('gpt-4-turbo-preview')
    main('claude-3-opus-20240229')
    main('qwen-max-0403')
    main('llama3_8b')
    main('llama3_70b')
    main('mixtral_8x22b')

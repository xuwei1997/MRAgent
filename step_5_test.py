# from agent_workflow import MRAgent
from mragent import MRAgent
import pandas as pd
import os
import ast
import re


def parse_list(input_string):
    # Remove square brackets and split by comma
    stripped_string = re.sub(r"[\[\]]", "", input_string)
    elements = stripped_string.split(',')

    # Remove any leading/trailing whitespaces and quotes
    cleaned_elements = [el.strip().strip("'\"") for el in elements]

    return cleaned_elements


class MRAgentTest5(MRAgent):
    def __init__(self, AI_key=None, LLM_model=None):
        self.LLM_model = LLM_model
        self.AI_key = AI_key
        self.define_path()

    def define_path(self):
        self.path = os.path.join('./MRAgentTest5')
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def step5(self):
        print(self.LLM_model)
        # 5.1 读取step4的结果
        step5_path = os.path.join(self.path, 'gwas_test.csv')
        df = pd.read_csv(step5_path)
        # print(df)

        # 5.2 取出opengwas为True的行
        df_oe = df[df['opengwas'] == True]

        # 5.3 获取df_oe所有相关gwas_id
        df_oe['gwas_id_' + self.LLM_model] = df_oe.apply(lambda x: self.step5_get_gwas_id(x['OE']), axis=1)
        print(df_oe)

        # 5.4 将df_oe的gwas_id列按OE合并到df中
        df = pd.merge(df, df_oe[['OE', 'gwas_id_' + self.LLM_model]], on='OE', how='left')
        print(df)

        # 取gwas_id_hum列
        gwas_id_c = df['gwas_id_hum']
        gwas_id_llm_c = df['gwas_id_' + self.LLM_model]

        # 5.5 计算查准率、查全率、F1分数

        precision_all = []
        recall_all = []
        f1_score_all = []

        # 逐行获取gwas_id_hum和gwas_id_llm,并转换为list
        for i, j in zip(gwas_id_c, gwas_id_llm_c):
            print(i, j)
            i = str(i)
            j = str(j)
            # gwas_id_list = ast.literal_eval(i)
            # gwas_id_llm_list = ast.literal_eval(j)

            gwas_id_list = parse_list(i)
            gwas_id_llm_list = parse_list(j)

            print(gwas_id_list)
            print(gwas_id_llm_list)

            # 计算交集
            intersection = list(set(gwas_id_list) & set(gwas_id_llm_list))
            # 计算查准率和查全率
            precision = len(intersection) / len(gwas_id_llm_list)
            recall = len(intersection) / len(gwas_id_list)
            print("交集: ", intersection)
            print("查准率: ", precision)
            print("查全率: ", recall)
            precision_all.append(precision)
            recall_all.append(recall)

            # 计算F1分数
            # 判断 若precision和recall都为0，则F1分数为0
            if precision == 0 and recall == 0:
                f1_score = 0
            else:
                f1_score = 2 * (precision * recall) / (precision + recall)
            print("F1分数: ", f1_score)
            f1_score_all.append(f1_score)

        # 计算查准率、查全率、F1分数的平均值
        precision_avg = sum(precision_all) / len(precision_all)
        recall_avg = sum(recall_all) / len(recall_all)
        f1_score_avg = sum(f1_score_all) / len(f1_score_all)
        print("查准率平均值: ", precision_avg)
        print("查全率平均值: ", recall_avg)
        print("F1分数平均值: ", f1_score_avg)

        # 保存结果到txt文件
        # 保存结果txt文件
        with open('MRAgentTest5/' + 'result.txt', 'a') as f:
            f.write(self.LLM_model + ':\n')
            f.write('precision_avg: ' + str(precision_avg) + '\n')
            f.write('recall_avg: ' + str(recall_avg) + '\n')
            f.write('f1_score_avg: ' + str(f1_score_avg) + '\n')
            f.write('\n')

        # 5.5 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'gwas_test.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    agent = MRAgentTest5(LLM_model='gpt-3.5-turbo', AI_key='')
    agent.step5()

    agent = MRAgentTest5(LLM_model='gpt-4-turbo-preview', AI_key='')
    agent.step5()

    agent = MRAgentTest5(LLM_model='claude-3-opus-20240229',
                         AI_key='')
    agent.step5()

    agent = MRAgentTest5(LLM_model='qwen-max-0403',
                         AI_key='')
    agent.step5()
    #
    agent = MRAgentTest5(LLM_model='gpt-4o', AI_key='')
    agent.step5()

    agent = MRAgentTest5(LLM_model='mixtral:8x22b', )
    agent.step5()

    agent = MRAgentTest5(LLM_model='llama3:8b', )
    agent.step5()

    agent = MRAgentTest5(LLM_model='llama3:70b', )
    agent.step5()

    agent = MRAgentTest5(LLM_model='qwen2:72b', )
    agent.step5()

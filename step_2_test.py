# 第二步测试 查看outcome和exposure是否做了MR
# from agent_workflow import MRAgent
from mragent import MRAgent
import pandas as pd
import os


class MRAgentTest2(MRAgent):
    def __init__(self, AI_key=None, LLM_model=None):
        self.LLM_model = LLM_model
        self.AI_key = AI_key
        self.define_path()

    def define_path(self):
        self.path = os.path.join('MRAgentTest2')
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def step2(self):
        # 2.1 读取step1的结果
        step1_path = os.path.join(self.path, 'MR40.csv')
        df = pd.read_csv(step1_path)
        # print(df)

        # 2.2 查看outcome和exposure是否做了MR
        # 提取outcome和exposure，去重
        df_oe = df[['Outcome', 'Exposure']].drop_duplicates()
        # print(df_oe)
        # 查看df_oe是否做了MR
        col = 'MRorNot_' + self.LLM_model
        # TODO outcome_exposure_MRorNot已经修改
        df_oe[col] = df_oe.apply(lambda x: self.outcome_exposure_MRorNot(x['Outcome'], x['Exposure']), axis=1)
        # print(df_oe)
        # 以df为基础，将df_oe的MRorNot合并到df中， 'Outcome'和 'Exposure'  是主键
        df = pd.merge(df, df_oe, on=['Outcome', 'Exposure'], how='left')

        # 计算准确率，地面真值列为 'MRorNot'，预测列为 'MRorNot_' + self.LLM_model
        GT = df['MRorNot']
        pred = df['MRorNot_' + self.LLM_model]
        # 计算准确率
        accuracy = sum(GT == pred) / len(GT)
        print(self.LLM_model, 'ACC:', accuracy)

        # 将准确率单独写入txt文件
        out_path = os.path.join(self.path, 'MR.txt')
        with open(out_path, 'a') as f:
            f.write(self.LLM_model + ' ACC: ' + str(accuracy) + '\n')

        # # 2.3 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'MR40.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    agent = MRAgentTest2(LLM_model='mixtral:8x22b')
    agent.step2()

    agent = MRAgentTest2(LLM_model='llama3:8b')
    agent.step2()

    agent = MRAgentTest2(LLM_model='llama3:70b')
    agent.step2()

    agent = MRAgentTest2(LLM_model='gpt-3.5-turbo', AI_key='')
    agent.step2()

    agent = MRAgentTest2(LLM_model='gpt-4-turbo-preview', AI_key='')
    agent.step2()

    agent = MRAgentTest2(LLM_model='claude-3-opus-20240229',
                         AI_key='')
    agent.step2()

    agent = MRAgentTest2(LLM_model='qwen-max-0403',
                         AI_key='')
    agent.step2()

    agent = MRAgentTest2(LLM_model='gpt-4o', AI_key='')
    agent.step2()

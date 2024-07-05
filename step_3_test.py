# 第三步测试
from agent_workflow import MRAgent
import os
import pandas as pd
from agent_tool import get_synonyms

class MRAgentTest3(MRAgent):
    def __init__(self, AI_key=None, LLM_model=None):
        self.LLM_model = LLM_model
        self.AI_key = AI_key
        self.define_path()

    def define_path(self):
        self.path = os.path.join('./MRAgentTest3')
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    # 同义词增强
    def step3(self):
        step_path = os.path.join(self.path, 'Outcome_SNP.csv')
        df2 = pd.read_csv(step_path)
        # 3.4 从df1中提取OE，调用GPT，寻找同义词，并合并到df2中。要求nID继续递增，但是sID还是原来OE的sID

        for index, row in df2.iterrows():
            # 3.4.1 提取OE和sID
            OE = row['OE']
            sID = row['sID']

            # 3.4.2 调用UMLS
            print(OE)
            python_list = get_synonyms(OE, "d6382a8b-5ca8-493a-98ca-2b02fffcaeb5")

            # 3.4.3 合并到df2中
            df3 = pd.DataFrame(python_list, columns=['OE'])
            # 增加一列sID
            df3['sID'] = sID
            print(df3)
            # 合并到df2中
            df2 = pd.concat([df2, df3], ignore_index=True)
            # print(df2)

        # 3.5 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, self.LLM_model + '_Outcome_SNP.csv')
        df2.to_csv(out_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    agent = MRAgentTest3(LLM_model='gpt-3.5-turbo', AI_key='')
    agent.step3()

    agent = MRAgentTest3(LLM_model='gpt-4-1106-preview', AI_key='')
    agent.step3()

    agent = MRAgentTest3(LLM_model='mixtral')
    agent.step3()

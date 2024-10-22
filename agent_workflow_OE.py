from agent_workflow import MRAgent
import pandas as pd
import os


class MRAgentOE(MRAgent):
    def __init__(self, mode='OE', *args, **kwargs):
        super().__init__(mode, *args, **kwargs)

    def step1(self):
        print(self.path)
        # 新建一个df然后保存到Exposure_and_Outcome.csv
        # 创建一个带有数据的DataFrame
        data = {'index': [1], 'Outcome': [self.outcome], 'Exposure': [self.exposure], 'title': ['title null'],
                'oeID': [1]}
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(self.path, 'Exposure_and_Outcome.csv'), index=False)  # 保存到csv文件

        # 打印DataFrame
        print(df)


if __name__ == '__main__':
    mr_key = ''
    # agent = MRAgentOE(outcome='anxiety', exposure='Lung cancer',
    #                   AI_key='',
    #                   model='MR_MOE', synonyms=False, bidirectional=True, introduction=False)
    # agent.run(step=[9])

    # agent = MRAgentOE(outcome='anxiety', exposure='erectile dysfunction',
    #                   AI_key='',
    #                   model='MR', synonyms=False, bidirectional=True, introduction=False)
    # agent.run()

    agent = MRAgentOE(exposure='spondylolysis', outcome='low back pain',
                      AI_key='', LLM_model='gpt-4o',
                      model='MR', synonyms=False, bidirectional=False, introduction=False, gwas_token=mr_key)
    agent.run(step=[1, 2, 3, 4, 5, 6, 7, 8, 9])

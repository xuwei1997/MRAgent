from mragent.agent_workflow import MRAgent
import pandas as pd
import os

class MRAgentOE(MRAgent):
    def __init__(self, mode='OE', *args, **kwargs):
        super().__init__(mode, **kwargs)

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

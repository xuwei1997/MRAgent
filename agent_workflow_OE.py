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
    mr_key = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImFwaS1qd3QiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkub3Blbmd3YXMuaW8iLCJhdWQiOiJhcGkub3Blbmd3YXMuaW8iLCJzdWIiOiI2NzA1MjU3NDRAcXEuY29tIiwiaWF0IjoxNzI0ODE3ODIwLCJleHAiOjE3MjYwMjc0MjB9.LW149mOujc5_Fwk4KxVncGcRudg3yJBarIlPOYEAool_UcDWf8HJESxl6tfrs7kPTU9r2jnxoCTb-w9vEe4LTAvUBFIUNZ5p38sW2S_d4VU1O2fpRmVuo7inlmJeTkFsoIMGI_Mg6559SFczs8nbYCkBQh515K6-NHU4vRMZS8fMVSQRfTwgVJKxStnzZweOC4XBvBwCb8RfUj3ypkRt_cHsn_dNyjkqEkuJ4Af98RmZrR6g6M9F8CcPwuoCumfsT9CJKevBa0aF0-yqerW8HY2_AQYj2J6-TuqvIR2itNlWMFv6FBP99fRSqSfHiY8-tmh0Calq1EZSvwJgmZ8CRQ'  # 提示词中已经加入ID
    # agent = MRAgentOE(outcome='anxiety', exposure='Lung cancer',
    #                   AI_key='',
    #                   model='MR_MOE', synonyms=False, bidirectional=True, introduction=False)
    # agent.run(step=[9])

    # agent = MRAgentOE(outcome='anxiety', exposure='erectile dysfunction',
    #                   AI_key='',
    #                   model='MR', synonyms=False, bidirectional=True, introduction=False)
    # agent.run()

    agent = MRAgentOE(exposure='spondylolysis', outcome='low back pain',
                      AI_key='sk-UPEaoPDBCHU9sy6N04A56cB8683249628fB6CdE2C45fDa67', LLM_model='gpt-4o',
                      model='MR', synonyms=False, bidirectional=False, introduction=False, gwas_token=mr_key)
    agent.run(step=[1, 2, 3, 4, 5, 6, 7, 8, 9])

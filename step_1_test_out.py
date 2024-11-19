# from agent_workflow import MRAgent
# from agent_tool import pubmed_crawler
# from LLM import llm_chat

import os

from mragent import MRAgent
from mragent.agent_tool import pubmed_crawler
from mragent.LLM import llm_chat

# from template_text import pubmed_text_obo
from mragent.template_text import pubmed_text_obo
import json
import pandas as pd

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


class MRAgentTest1(MRAgent):
    def __init__(self, outcome=None, AI_key=None, LLM_model=None, num=100):
        self.LLM_model = LLM_model
        self.AI_key = AI_key
        self.outcome = outcome
        self.num = num
        self.define_path()

    def define_path(self):
        self.path = os.path.join('MRAgentTest1')
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def step1(self):
        # 判断json文件是否存在
        out_path = os.path.join(self.path, self.outcome + str(self.num) + '.json')
        print(os.path.exists(out_path))
        if os.path.exists(out_path):
            # 读取json文件
            with open(out_path, 'r', encoding='utf-8') as f:
                pubmed_out = f.read()
                # 转换为json
                pubmed_out = json.loads(pubmed_out)
                print(pubmed_out)

        else:
            # 1.1 从pubmed获取相关文章
            pubmed_out = pubmed_crawler(self.outcome, self.num, 'most recent', json_str=False)
            print(pubmed_out)
            # 保存为json文件
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(json.dumps(pubmed_out))

            # 1.1 将文章写入pdf文件中，基于from reportlab.lib.styles import getSampleStyleSheet
            # 1.1.1 创建pdf文件
            doc = SimpleDocTemplate(os.path.join(self.path, self.outcome + str(self.num) + '.pdf'), pagesize=letter)
            # 1.1.2 创建样式
            styles = getSampleStyleSheet()
            # 1.1.3 创建一个空列表，用于存放结果
            story = []
            # 1.1.4 标题
            title = story.append(Paragraph('Most Recent Paper Related to ' + self.outcome, styles['Title']))
            story.append(title)
            story.append(Spacer(1, 12))
            story.append(Spacer(1, 12))
            # 1.1.5 内容
            for paper in pubmed_out:
                index = paper['index']
                title = paper['title']
                abstract = paper['abstract']
                story.append(Paragraph('Index: ' + str(index), styles['Normal']))
                story.append(Paragraph('Title: ' + title, styles['Normal']))
                story.append(Paragraph('Abstract: ' + abstract, styles['Normal']))
                story.append(Spacer(1, 12))
            # 构建 PDF
            doc.build(story)

        # 1.2 输出文章信息
        # 创建一个空列表，用于存放结果
        out = []
        # 提示词
        template = pubmed_text_obo
        for paper in pubmed_out:
            print(paper)
            # 分别取出index, title, abstract
            index = paper['index']
            title = paper['title']
            abstract = paper['abstract']
            # 1.3 LLM判断
            try:
                t = template.format(Outcome=self.outcome, title=title, abstract=abstract)
                gpt_out = llm_chat(t, self.LLM_model, self.AI_key)
                print('gpt_out:')
                print(gpt_out)
                # 利用正则表达式提取结果中的json list
                gpt_out = gpt_out.split('[')[1].split(']')[0]
                gpt_out = '[' + gpt_out + ']'
                print('gpt_out_list:')
                print(gpt_out)

                # 1.4 保存结果
                # 转换为json
                items = json.loads(gpt_out)
                print('items:')
                print(items)
                for item in items:
                    # 测试时不判断不为空
                    if item['Outcome'] is not None:
                        # 将index加入item
                        item['index'] = index
                        # 将 title 加入item
                        item['title'] = title
                        # 将 abstract 加入item
                        item['abstract'] = abstract
                        out.append(item)
                print('\n')
            except Exception as e:
                print('error:', e)
        print(out)

        # 1.4 转换为DataFrame
        # df = pd.DataFrame(items, columns=['index', 'Outcome', 'Exposure', 'title'])
        df = pd.DataFrame(out, columns=['index', 'title', 'Outcome', 'Exposure'])
        # 增加一列nID oeID
        # df['nID'] = range(0, len(df))
        df['oeID'] = range(0, len(df))
        print(df)

        # 1.5 保存
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, self.outcome + '_' + self.LLM_model + '_Exposure_and_Outcome.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')


def run_test(outcome, num):
    # 开源模型
    agent = MRAgentTest1(outcome=outcome, LLM_model='mixtral:8x22b', num=num)
    agent.step1()

    agent = MRAgentTest1(outcome=outcome, LLM_model='llama3:8b', num=num)
    agent.step1()

    agent = MRAgentTest1(outcome=outcome, LLM_model='llama3:70b', num=num)
    agent.step1()
    #
    # # 闭源模型
    # gpt-4-turbo-2024-04-09
    agent = MRAgentTest1(outcome=outcome, LLM_model='gpt-4-turbo-preview',
                         AI_key='', num=num)
    agent.step1()

    # gpt-3.5-turbo-0125
    agent = MRAgentTest1(outcome=outcome, LLM_model='gpt-3.5-turbo',
                         AI_key='', num=num)
    agent.step1()

    agent = MRAgentTest1(outcome=outcome, LLM_model='gemini-1.5-pro-latest',
                         AI_key='', num=num)
    agent.step1()

    agent = MRAgentTest1(outcome=outcome, LLM_model='claude-3-opus-20240229',
                         AI_key='', num=num)
    agent.step1()
    #
    agent = MRAgentTest1(outcome=outcome, LLM_model='qwen-max-0403',
                            AI_key='', num=num)
    agent.step1()


if __name__ == '__main__':
    run_test('Alzheimer', 30)
    run_test('Lung cancer', 30)
    run_test('Chronic kidney disease', 30)

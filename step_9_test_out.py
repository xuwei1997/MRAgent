# from agent_workflow import MRAgent
from mragent import MRAgent
import os
import pandas as pd
# from agent_tool import MRtool, MRtool_MOE
from mragent.agent_tool import MRtool, MRtool_MOE
# from template_text import MRorNot_text, synonyms_text, gwas_id_text, pubmed_text, LLM_MR_template, LLM_MR_MOE_template, \
#     LLM_conclusion_template, LLM_Introduction_template, pubmed_text_obo

from mragent.template_text import MRorNot_text, synonyms_text, gwas_id_text, pubmed_text, LLM_MR_template, LLM_MR_MOE_template, \
    LLM_conclusion_template, LLM_Introduction_template, pubmed_text_obo

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfMerger
# from LLM import llm_chat
from mragent.LLM import llm_chat

from key import mr_key


class MRAgentTest9(MRAgent):
    def __init__(self, AI_key=None, LLM_model=None, model='MR', gwas_token=None):
        self.LLM_model = LLM_model
        self.AI_key = AI_key
        self.define_path()
        self.model = model
        self.gwas_token = gwas_token

    def define_path(self):
        self.path = os.path.join('MRAgentTest9')
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def LLM_MR_result(self, Exposure, Outcome, Exposure_id, Outcome_id, snp_path):

        if self.model == 'MR':
            # 打开文件
            with open(os.path.join(snp_path, 'table.MRresult.csv'), 'r') as file:
                MRresult = file.read()
            with open(os.path.join(snp_path, 'table.heterogeneity.csv'), 'r') as file:
                heterogeneity = file.read()
            with open(os.path.join(snp_path, 'table.pleiotropy.csv'), 'r') as file:
                pleiotropy = file.read()

            template = LLM_MR_template
            t = template.format(Outcome=Outcome, Exposure=Exposure, MRresult=MRresult, heterogeneity=heterogeneity,
                                pleiotropy=pleiotropy, Exposure_id=Exposure_id, Outcome_id=Outcome_id)
            gpt_out = llm_chat(t, self.LLM_model, self.AI_key)
            # 保存输出结果
            with open(os.path.join(snp_path, self.LLM_model + '_LLM_result.txt'), 'w') as file:
                file.write(gpt_out)
        elif self.model == 'MR_MOE':
            # 打开文件
            with open(os.path.join(snp_path, 'MR.MRresult.csv'), 'r') as file:
                MRresult = file.read()
            with open(os.path.join(snp_path, 'MR.heterogeneity.csv'), 'r') as file:
                heterogeneity = file.read()
            with open(os.path.join(snp_path, 'MR.table.pleiotropy.csv'), 'r') as file:
                pleiotropy = file.read()

            template = LLM_MR_MOE_template
            t = template.format(Outcome=Outcome, Exposure=Exposure, MRresult=MRresult, heterogeneity=heterogeneity,
                                pleiotropy=pleiotropy, Exposure_id=Exposure_id, Outcome_id=Outcome_id)
            gpt_out = llm_chat(t, self.LLM_model, self.AI_key)
            # 保存输出结果
            with open(os.path.join(snp_path, self.LLM_model + '_LLM_result.txt'), 'w') as file:
                file.write(gpt_out)

        # # 生成PDF####################################
        # 创建
        doc = SimpleDocTemplate(os.path.join(snp_path, self.LLM_model + "_Report.pdf"), pagesize=letter)
        # 设置样式
        styles = getSampleStyleSheet()
        # 创建一个空的 Story 列表来保存文档内容
        story = []
        # 添加标题
        title = Paragraph("A Mendelian randomisation study about " + Exposure + " and " + Outcome,
                          styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))

        styles["BodyText"].fontSize = 12  # 设置字体大小为 14
        styles["BodyText"].alignment = 4  # 设置文字居中 4
        styles["BodyText"].fontName = 'Times-Roman'  # 设置字体

        # 分析结果
        subtitle = Paragraph("Analysis of MR results", styles["Heading2"])
        story.append(subtitle)
        gpt_out_list = gpt_out.split('\n')
        for gpt_out_i in gpt_out_list:
            text = Paragraph(gpt_out_i, styles["BodyText"])
            # story.append(Spacer(1, 12))
            story.append(text)
        # 构建 PDF
        doc.build(story)

        # 合并PDF和图片
        # 创建一个 PdfFileMerger 对象
        merger = PdfMerger()
        # 列出你想要合并的 PDF 文件
        pdfs = [os.path.join(snp_path, self.LLM_model + "_Report.pdf"), os.path.join(snp_path, 'pic.scatter_plot.pdf'),
                os.path.join(snp_path, 'pic.forest.pdf'), os.path.join(snp_path, 'pic.funnel_plot.pdf'),
                os.path.join(snp_path, 'pic.leaveoneout.pdf')]
        # 循环遍历 PDF 文件并将它们添加到合并器
        for pdf in pdfs:
            merger.append(pdf)
        # 写入合并的 PDF 文件
        merger.write(os.path.join(snp_path, self.LLM_model + "_Report.pdf"))
        # 关闭合并器
        merger.close()

        return gpt_out

    def step9_run_mr_test(self, Exposure, Outcome, path, Exposure_id, Outcome_id):
        try:
            # 进行MR分析
            if self.model == 'MR':
                # 判断是否已经生成了MR结果
                if not os.path.exists(os.path.join(path, 'table.MRresult.csv')):
                    path = path.replace('\\', '//')
                    MRtool(Exposure_id, Outcome_id, path, self.gwas_token)
                # 调用GPT解释MR的结果
                self.LLM_MR_result(Exposure=Exposure, Outcome=Outcome, snp_path=path, Exposure_id=Exposure_id,
                                   Outcome_id=Outcome_id)

            elif self.model == 'MR_MOE':
                # 判断是否已经生成了MR结果
                if not os.path.exists(os.path.join(path, 'MR.MRresult.csv')):
                    path = path.replace('\\', '//')
                    MRtool_MOE(Exposure_id, Outcome_id, path, self.gwas_token)
                # 调用GPT解释MR的结果
                self.LLM_MR_result(Exposure=Exposure, Outcome=Outcome, snp_path=path, Exposure_id=Exposure_id,
                                   Outcome_id=Outcome_id)

            # TODO: 创建对应不同LLM模型的文件夹
            # 进行LLM生成
            # 生成的结果保存到文件夹中

        except Exception as e:
            print(e)

    def step9(self):
        # mr_run_s9_test.csv 中包含了Outcome和Exposure以及对应的snp的gwas_id
        step9_path = os.path.join(self.path, 'mr_run_s9.csv')
        df = pd.read_csv(step9_path)
        # 逐行获取df中的Outcome	Exposure	Outcome_id	Exposure_id
        for index, row in df.iterrows():
            Outcome = row['Outcome']
            Exposure = row['Exposure']
            Outcome_id = row['Outcome_id']
            Exposure_id = row['Exposure_id']
            print(Outcome, Exposure, Outcome_id, Exposure_id)

            # 创建文件夹
            oe_path = os.path.join(self.path, Exposure + '_' + Outcome + '_' + Exposure_id + '_' + Outcome_id)
            if not os.path.exists(oe_path):
                os.makedirs(oe_path)

            # 运行MR
            # 此处若是已经生成了MR结果，则不再生成
            self.step9_run_mr_test(Exposure=Exposure, Outcome=Outcome, path=oe_path, Exposure_id=Exposure_id,
                                   Outcome_id=Outcome_id)


if __name__ == '__main__':
    agent = MRAgentTest9(LLM_model='gpt-3.5-turbo', AI_key='',
                         model='MR_MOE', gwas_token=mr_key)
    agent.step9()

    agent = MRAgentTest9(LLM_model='gpt-4-turbo-preview', AI_key='',
                         model='MR_MOE', gwas_token=mr_key)
    agent.step9()

    agent = MRAgentTest9(LLM_model='qwen-max-0403', AI_key='',
                         model='MR_MOE', gwas_token=mr_key)
    agent.step9()

    agent = MRAgentTest9(LLM_model='claude-3-opus-20240229',
                         AI_key='',
                         model='MR_MOE', gwas_token=mr_key)
    agent.step9()

    agent = MRAgentTest9(LLM_model='mixtral:8x22b',
                         model='MR_MOE', gwas_token=mr_key)
    agent.step9()

    agent = MRAgentTest9(LLM_model='llama3:8b',
                         model='MR_MOE', gwas_token=mr_key)
    agent.step9()

    agent = MRAgentTest9(LLM_model='llama3:70b',
                         model='MR_MOE', gwas_token=mr_key)
    agent.step9()

    agent = MRAgentTest9(LLM_model='qwen2:72b',
                         model='MR_MOE', gwas_token=mr_key)
    agent.step9()

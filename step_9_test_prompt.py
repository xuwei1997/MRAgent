# 复制step_9_test_out.py到step_9_test_template.py并修改

# MR
# 完全无知识
LLM_MR_template_zero_shot = """Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}), please read and understand the results in the table and generate a paragraph describing the results in detail in academic language. 

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}
"""

# 有少量知识
LLM_MR_template_few_knowledge = """Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}), please read and understand the results in the table and generate a paragraph describing the results in detail in academic language. Typically, significance can be judged by the Inverse variance weighted method of pval<0.05. or>1 there is a positive correlation and or<1 there is a negative correlation.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}
"""

# 有一个例子
LLM_MR_template_one_shot = LLM_MR_template_zero_shot + """
I will also give another completed report for your reference.

The referenced report:

Mendelian randomization (MR) analyses of fresh fruit intake (ukb-b-3881) and asthma (finn-b-J10_ASTHMA) was conducted using summary data from genome-wide association studies (GWAS). Five different MR methods including MR Egger regression, weighted median, inverse variance weighted, simple mode and weighted mode were applied. 53 single nucleotide polymorphisms (SNPs) were included in the final MR analysis.

The MR analyses provided evidence that higher fruit intake causally decreases asthma risk. Specifically, the inverse-variance weighted (IVW) algorithm showed a statistically significant association between fruit intake and lower asthma risk (OR = 0.509, 95% CI: 0.334 - 0.775; P = 0.001). Furthermore, this causal association was supported by the weighted median (OR = 0.499, 95% CI: 0.274 - 0.907; P = 0.02). All methods were directionally consistent.

A series of sensitivity analyses were conducted to evaluate potential sources of bias heterogeneity and pleiotropy in our MR analysis. First, we conducted heterogeneity testing using the IVW and MR-Egger methods, and the results revealed no heterogeneity among the instruments (Q pval >0.05). Next, MR-Egger regression intercepts were examined to detect the horizontal pleiotropy, defined as a genetic variant influencing both exposure and outcome through independent biological pathways and no evidence of pleiotropy was identified (P = 0.44).  

In summary, this Mendelian randomization analysis provides supportive evidence that higher fresh fruit intake has a causal protective effect on reducing asthma risk. Sensitivity analyses validated the robustness of these causal relationships against biases from pleiotropy, outliers or reverse causation.
"""

# 有少量知识且有例子
LLM_MR_template_one_shot_and_knowledge = LLM_MR_template_few_knowledge + """
I will also give another completed report for your reference.

The referenced report:

Mendelian randomization (MR) analyses of fresh fruit intake (ukb-b-3881) and asthma (finn-b-J10_ASTHMA) was conducted using summary data from genome-wide association studies (GWAS). Five different MR methods including MR Egger regression, weighted median, inverse variance weighted, simple mode and weighted mode were applied. 53 single nucleotide polymorphisms (SNPs) were included in the final MR analysis.

The MR analyses provided evidence that higher fruit intake causally decreases asthma risk. Specifically, the inverse-variance weighted (IVW) algorithm showed a statistically significant association between fruit intake and lower asthma risk (OR = 0.509, 95% CI: 0.334 - 0.775; P = 0.001). Furthermore, this causal association was supported by the weighted median (OR = 0.499, 95% CI: 0.274 - 0.907; P = 0.02). All methods were directionally consistent.

A series of sensitivity analyses were conducted to evaluate potential sources of bias heterogeneity and pleiotropy in our MR analysis. First, we conducted heterogeneity testing using the IVW and MR-Egger methods, and the results revealed no heterogeneity among the instruments (Q pval >0.05). Next, MR-Egger regression intercepts were examined to detect the horizontal pleiotropy, defined as a genetic variant influencing both exposure and outcome through independent biological pathways and no evidence of pleiotropy was identified (P = 0.44).  

In summary, this Mendelian randomization analysis provides supportive evidence that higher fresh fruit intake has a causal protective effect on reducing asthma risk. Sensitivity analyses validated the robustness of these causal relationships against biases from pleiotropy, outliers or reverse causation.
"""

#  零样本cot
LLM_MR_template_zero_shot_CoT = """
Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}), please read and understand the results in the table and generate a paragraph describing the results in detail in academic language. Let’s think step by step.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}
"""

# 有少量知识cot
LLM_MR_template_zero_shot_CoT_and_knowledge = """
Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}), please read and understand the results in the table and generate a paragraph describing the results in detail in academic language. Typically, significance can be judged by the Inverse variance weighted method of pval<0.05. or>1 there is a positive correlation and or<1 there is a negative correlation. Let’s think step by step.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}
"""

# MR_MOE
# 完全无知识
LLM_MR_MOE_template_zero_shot = """
Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}).
Mendelian randomization analysis was performed based on the Mixture of experts (MOE) function in TwoSampleMR.
Please read and understand the results in the table and generate a paragraph describing the results in detail in academic language.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}
"""

# 有少量知识
LLM_MR_MOE_template_few_knowledge = """Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}).
Mendelian randomization analysis was performed based on the Mixture of experts (MOE) function in TwoSampleMR. Once all MR methods have been applied to a summary set, you can then use the mixture of experts to predict the method most likely to be the most accurate. The MOE column, which is a predictor for each method for how well it performs in terms of high power and low type 1 error (scaled 0-1, where 1 is best performance). It orders the table to be in order of best performing method.
Please read and understand the results in the table and generate a paragraph describing the results in detail in academic language.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}
"""

# 有一个例子
LLM_MR_MOE_template_one_shot = LLM_MR_MOE_template_zero_shot + """
I will also give another completed report for your reference.

The referenced report:
The Mendelian randomization (MR) analysis, leveraging the Mixture of experts (MOE) function in TwoSampleMR, investigated the causal relationship between Type 2 diabetes (Exposure; GWAS ID: ebi-a-GCST006867) and Bone mineral density (Outcome; GWAS ID: ebi-a-GCST90014022). The results span various MR methods, displaying a range of estimates for the causal effect, alongside their precision and statistical significance.

The Penalised mode method yielded a statistically significant association (b = 0.0330, SE = 0.0083, CI: 0.0168 to 0.0493, p = 0.00012), suggesting a potential causal relationship between Type 2 diabetes and an increased risk of Bone mineral density. This outcome was corroborated by the Random Effects Inverse Variance Weighted (RE IVW) and Fixed Effects Egger (FE Egger) methods, although with varying effect sizes and confidence intervals, indicating some differences in the robustness and interpretation of the causal estimate across these methods.

The analysis performed checks for both heterogeneity and pleiotropy, critical aspects that can affect the validity of MR estimates. The heterogeneity analysis, assessed through the Cochran’s Q test, indicated no significant heterogeneity across the instrumental variables used in the IVW (Q = 1159.35, P = 1.46E-173) and Egger (Q = 1160.9793, P = 2.1555E-174) methods, suggesting that the instrumental variables contributed similarly to the estimation of the causal effect. The pleiotropy test, using the Egger intercept, showed no evidence of pleiotropy (intercept = 0.000795, SE = 0.00162, p = 0.625171), implying that the instrumental variables were not affecting the outcome through pathways other than the exposure, thus supporting the validity of the MR findings.

These comprehensive analyses, when considered together, provide evidence to suggest a potential causal association between Type 2 diabetes and Bone mineral density. The consistency of significant findings across multiple MR methods strengthens the confidence in the observed association, albeit recognizing the importance of further investigative studies to confirm these results and elucidate underlying mechanisms.
"""

# 有少量知识且有例子
LLM_MR_MOE_template_one_shot_and_knowledge = LLM_MR_MOE_template_few_knowledge + """
I will also give another completed report for your reference.

The referenced report:
The Mendelian randomization (MR) analysis, leveraging the Mixture of experts (MOE) function in TwoSampleMR, investigated the causal relationship between Type 2 diabetes (Exposure; GWAS ID: ebi-a-GCST006867) and Bone mineral density (Outcome; GWAS ID: ebi-a-GCST90014022). The results span various MR methods, displaying a range of estimates for the causal effect, alongside their precision and statistical significance.

The Penalised mode method yielded a statistically significant association (b = 0.0330, SE = 0.0083, CI: 0.0168 to 0.0493, p = 0.00012), suggesting a potential causal relationship between Type 2 diabetes and an increased risk of Bone mineral density. This outcome was corroborated by the Random Effects Inverse Variance Weighted (RE IVW) and Fixed Effects Egger (FE Egger) methods, although with varying effect sizes and confidence intervals, indicating some differences in the robustness and interpretation of the causal estimate across these methods.

The analysis performed checks for both heterogeneity and pleiotropy, critical aspects that can affect the validity of MR estimates. The heterogeneity analysis, assessed through the Cochran’s Q test, indicated no significant heterogeneity across the instrumental variables used in the IVW (Q = 1159.35, P = 1.46E-173) and Egger (Q = 1160.9793, P = 2.1555E-174) methods, suggesting that the instrumental variables contributed similarly to the estimation of the causal effect. The pleiotropy test, using the Egger intercept, showed no evidence of pleiotropy (intercept = 0.000795, SE = 0.00162, p = 0.625171), implying that the instrumental variables were not affecting the outcome through pathways other than the exposure, thus supporting the validity of the MR findings.

These comprehensive analyses, when considered together, provide evidence to suggest a potential causal association between Type 2 diabetes and Bone mineral density. The consistency of significant findings across multiple MR methods strengthens the confidence in the observed association, albeit recognizing the importance of further investigative studies to confirm these results and elucidate underlying mechanisms.
"""

#  零样本cot
LLM_MR_MOE_template_zero_shot_CoT = """
Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}).
Mendelian randomization analysis was performed based on the Mixture of experts (MOE) function in TwoSampleMR. 
Please read and understand the results in the table and generate a paragraph describing the results in detail in academic language. Let’s think step by step.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}
"""

# 有少量知识cot
LLM_MR_MOE_template_zero_shot_CoT_and_knowledge = """Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}).
Mendelian randomization analysis was performed based on the Mixture of experts (MOE) function in TwoSampleMR. Once all MR methods have been applied to a summary set, you can then use the mixture of experts to predict the method most likely to be the most accurate. The MOE column, which is a predictor for each method for how well it performs in terms of high power and low type 1 error (scaled 0-1, where 1 is best performance). It orders the table to be in order of best performing method.
Please read and understand the results in the table and generate a paragraph describing the results in detail in academic language. Let’s think step by step.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}
"""

# from agent_workflow import MRAgent
from mragent import MRAgent
# from template_text import LLM_MR_template, LLM_MR_MOE_template
import os
import pandas as pd
from mragent.agent_tool import MRtool, MRtool_MOE
from mragent.LLM import llm_chat
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfMerger


class MRAgentTest9Prompt(MRAgent):
    def __init__(self, prompt_template, prompt_name, AI_key=None, LLM_model=None,
                 base_url="https://api.gpt.ge/v1/", model='MR', gwas_token=None,
                 test_csv_path=None):
        self.LLM_model = LLM_model
        self.AI_key = AI_key
        self.define_path()
        self.model = model
        self.gwas_token = gwas_token
        self.prompt_template = prompt_template
        self.test_csv_path = test_csv_path
        self.prompt_name = prompt_name
        self.base_url = base_url

    def define_path(self):
        self.path = os.path.join('MRAgentTest9-Prompt')
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def LLM_MR_result_PDF(self, Exposure, Outcome, gpt_out, mrlap_text, snp_path):
        # 创建PDF####################################
        doc = SimpleDocTemplate(os.path.join(snp_path, self.prompt_name + "_Report.pdf"), pagesize=letter)
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
        pdfs = [os.path.join(snp_path, self.prompt_name + "_Report.pdf"),
                os.path.join(snp_path, 'pic.scatter_plot.pdf'),
                os.path.join(snp_path, 'pic.forest.pdf'), os.path.join(snp_path, 'pic.funnel_plot.pdf'),
                os.path.join(snp_path, 'pic.leaveoneout.pdf')]
        # 循环遍历 PDF 文件并将它们添加到合并器
        for pdf in pdfs:
            merger.append(pdf)
        # 写入合并的 PDF 文件
        merger.write(os.path.join(snp_path, self.prompt_name + "_Report.pdf"))
        # 关闭合并器
        merger.close()

    def LLM_MR_result(self, Exposure, Outcome, Exposure_id, Outcome_id, snp_path):
        print(Exposure, Outcome, Exposure_id, Outcome_id)

        if self.model == 'MR':
            # 打开文件
            with open(os.path.join(snp_path, 'table.MRresult.csv'), 'r', encoding='utf-8') as file:
                MRresult = file.read()
            with open(os.path.join(snp_path, 'table.heterogeneity.csv'), 'r', encoding='utf-8') as file:
                heterogeneity = file.read()
            with open(os.path.join(snp_path, 'table.pleiotropy.csv'), 'r', encoding='utf-8') as file:
                pleiotropy = file.read()

            template = self.prompt_template
            t = template.format(Outcome=Outcome, Exposure=Exposure, MRresult=MRresult, heterogeneity=heterogeneity,
                                pleiotropy=pleiotropy, Exposure_id=Exposure_id, Outcome_id=Outcome_id)
            gpt_out = llm_chat(t, self.LLM_model, self.AI_key, self.base_url, self.model_type)
            # print(gpt_out)
            # 保存输出结果
            with open(os.path.join(snp_path, 'LLM_result.txt'), 'w', encoding='utf-8') as file:
                file.write(gpt_out)
        elif self.model == 'MR_MOE':
            # 打开文件
            with open(os.path.join(snp_path, 'MR.MRresult.csv'), 'r', encoding='utf-8') as file:
                MRresult = file.read()
            with open(os.path.join(snp_path, 'MR.heterogeneity.csv'), 'r', encoding='utf-8') as file:
                heterogeneity = file.read()
            with open(os.path.join(snp_path, 'MR.table.pleiotropy.csv'), 'r', encoding='utf-8') as file:
                pleiotropy = file.read()

            template = self.prompt_template
            t = template.format(Outcome=Outcome, Exposure=Exposure, MRresult=MRresult, heterogeneity=heterogeneity,
                                pleiotropy=pleiotropy, Exposure_id=Exposure_id, Outcome_id=Outcome_id)
            gpt_out = llm_chat(t, self.LLM_model, self.AI_key, self.base_url, self.model_type)
            # 保存输出结果
            with open(os.path.join(snp_path, 'LLM_result.txt'), 'w', encoding='utf-8') as file:
                file.write(gpt_out)
        else:
            gpt_out = None

        mrlap_text = None

        self.LLM_MR_result_PDF(Exposure, Outcome, gpt_out, mrlap_text, snp_path)

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
        except Exception as e:
            print(e)

    def step9(self):
        # mr_run_s9_test.csv 中包含了Outcome和Exposure以及对应的snp的gwas_id
        step9_path = os.path.join(self.path, self.test_csv_path)
        df = pd.read_csv(step9_path)
        # 逐行获取df中的Outcome	Exposure	Outcome_id	Exposure_id
        for index, row in df.iterrows():
            Outcome = row['Outcome']
            Exposure = row['Exposure']
            Outcome_id = row['Outcome_id']
            Exposure_id = row['Exposure_id']
            print(Outcome, Exposure, Outcome_id, Exposure_id)

            # 创建文件夹
            oe_path = os.path.join(self.path,
                                   self.model + '_' + Exposure + '_' + Outcome + '_' + Exposure_id + '_' + Outcome_id)
            if not os.path.exists(oe_path):
                os.makedirs(oe_path)

            # 运行MR
            # 此处若是已经生成了MR结果，则不再生成
            self.step9_run_mr_test(Exposure=Exposure, Outcome=Outcome, path=oe_path, Exposure_id=Exposure_id,
                                   Outcome_id=Outcome_id)


if __name__ == '__main__':
    from key import AI_key, mr_key

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_template_zero_shot, prompt_name='LLM_MR_template_zero_shot',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_template_few_knowledge,
                               prompt_name='LLM_MR_template_few_knowledge',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_template_one_shot, prompt_name='LLM_MR_template_one_shot',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_template_one_shot_and_knowledge,
                               prompt_name='LLM_MR_template_one_shot_and_knowledge',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_template_zero_shot_CoT,
                               prompt_name='LLM_MR_template_zero_shot_CoT',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_template_zero_shot_CoT_and_knowledge,
                               prompt_name='LLM_MR_template_zero_shot_CoT_and_knowledge',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_MOE_template_zero_shot,
                               prompt_name='LLM_MR_MOE_template_zero_shot',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR_MOE',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_MOE_template_few_knowledge,
                               prompt_name='LLM_MR_MOE_template_few_knowledge',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR_MOE',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_MOE_template_one_shot,
                               prompt_name='LLM_MR_MOE_template_one_shot',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR_MOE',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_MOE_template_one_shot_and_knowledge,
                               prompt_name='LLM_MR_MOE_template_one_shot_and_knowledge',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR_MOE',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_MOE_template_zero_shot_CoT,
                               prompt_name='LLM_MR_MOE_template_zero_shot_CoT',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR_MOE',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

    agent = MRAgentTest9Prompt(prompt_template=LLM_MR_MOE_template_zero_shot_CoT_and_knowledge,
                               prompt_name='LLM_MR_MOE_template_zero_shot_CoT_and_knowledge',
                               LLM_model='gpt-4o', base_url="https://api.gpt.ge/v1/", AI_key=AI_key, model='MR_MOE',
                               gwas_token=mr_key, test_csv_path='mr_prompt_test.csv')
    agent.step9()

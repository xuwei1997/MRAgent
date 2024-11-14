# 复制step_9_test_out.py到step_9_test_template.py并修改

from agent_workflow import MRAgent
# from template_text import LLM_MR_template, LLM_MR_MOE_template

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
"""

# 有少量知识
LLM_MR_MOE_template_few_knowledge = """
"""

# 有一个例子
LLM_MR_MOE_template_one_shot = """
"""

# 有少量知识且有例子
LLM_MR_MOE_template_one_shot_and_knowledge = """
"""

#  零样本cot
LLM_MR_MOE_template_zero_shot_CoT = """
"""

# 有少量知识cot
LLM_MR_MOE_template_zero_shot_CoT_and_knowledge = """
"""

class MRAgentTest9Prompt(MRAgent):
    pass
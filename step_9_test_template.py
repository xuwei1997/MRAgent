# 复制step_9_test_out.py到step_9_test_template.py并修改

from agent_workflow import MRAgent
from template_text import LLM_MR_template, LLM_MR_MOE_template

# MR
# 完全无知识
LLM_MR_template_zero_shot = """
"""

# 有少量知识
LLM_MR_template_few_knowledge = """
"""
# 有一个例子
LLM_MR_template_one_shot = """
"""


# 有少量知识且有例子
LLM_MR_template_one_shot_and_knowledge = """
"""

#  零样本cot
LLM_MR_template_zero_shot_CoT = """
"""

# 有少量知识cot
LLM_MR_template_zero_shot_CoT_and_knowledge = """
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
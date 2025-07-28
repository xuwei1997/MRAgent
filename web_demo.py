import streamlit as st
import pandas as pd
import os
import sys
import time
import zipfile
import io
import shutil
import subprocess
from mragent import MRAgent, MRAgentOE
import threading
import streamlit.components.v1 as components




# 设置页面配置
st.set_page_config(page_title="MRAgent Demo", layout="wide")

# 标题和介绍
st.title("MRAgent: An LLM-based Automated Agent for Causal Knowledge Discovery")
st.markdown("""
This demo allows you to run MRAgent for causal knowledge discovery in disease via Mendelian Randomization.
""")
st.markdown("[Paper](https://doi.org/10.1093/bib/bbaf140) | [GitHub](https://github.com/xuwei1997/MRAgent) | [PyPI](https://pypi.org/project/mragent/) | [中文文档](https://p1bvxbwjxl0.feishu.cn/docx/L0ogdoDs5ofjIux6W6gct8E4nyd?from=from_copylink)")

# 模式选择
mode = st.selectbox("Select Mode", ["Knowledge Discovery", "Causal Validation"])

# 根据模式显示不同的输入字段
if mode == "Knowledge Discovery":
    st.markdown("### Knowledge Discovery Mode")
    st.markdown("In this mode, the agent will discover potential causal relationships for a given disease.")

    # 输入字段
    col1, col2 = st.columns(2)
    with col1:
        exposure = st.text_input("Exposure (Optional if Outcome is provided)")
    with col2:
        outcome = st.text_input("Outcome (Optional if Exposure is provided)")

    # 验证至少有一个字段被填写
    if not exposure and not outcome:
        st.warning("Please provide at least one of Exposure or Outcome.")

else:  # Causal Validation 模式
    st.markdown("### Causal Validation Mode")
    st.markdown("In this mode, the agent will validate a specific causal relationship between an exposure and outcome.")

    # 输入字段
    col1, col2 = st.columns(2)
    with col1:
        exposure = st.text_input("Exposure (Required)")
    with col2:
        outcome = st.text_input("Outcome (Required)")

    # 验证两个字段都被填写
    if not exposure or not outcome:
        st.warning("Both Exposure and Outcome are required for Causal Validation mode.")

# 共同的输入字段
col1, col2, col3 = st.columns(3)
with col1:
    ai_key = st.text_input("AI Key (Required)", type="password")
with col2:
    base_url = st.text_input("Base URL (Optional)")
# with col3:
#     llm_model = st.selectbox("LLM Model",
#                              ["gpt-4o", "gpt-4", "gpt-3.5-turbo", "claude-3-opus", "claude-3-sonnet", "gemini-pro"])

# 修改后的代码
with col3:
    # 预定义的模型列表
    predefined_models = ["gpt-4.1", "gpt-4o", "gpt-4.1-mini", "deepseek-r1", "gemini-2.5-pro"]
    # 添加一个“自定义”选项
    options = predefined_models + ["Custom..."]

    # 创建下拉选择框
    selected_option = st.selectbox(
        "LLM Model",
        options,
        help="Select a predefined model or choose 'Custom' to enter your own."
    )

    # 如果用户选择“自定义”，则显示一个文本输入框
    if selected_option == "Custom...":
        llm_model = st.text_input(
            "Enter Custom Model Name:",
            placeholder="e.g., gpt-4o-2024-05-13",
            key="custom_llm_model_input"
        )
    else:
        # 否则，使用选择的模型
        llm_model = selected_option

col1, col2 = st.columns(2)
with col1:
    gwas_token = st.text_input("GWAS Token", type="password")
with col2:
    mr_model = st.selectbox("MR Model", ["MR", "MR_MOE"])

# 高级选项（可折叠）
with st.expander("Advanced Options"):
    col1, col2, col3 = st.columns(3)
    with col1:
        bidirectional = st.checkbox("Bidirectional Analysis", value=False)
        synonyms = st.checkbox("Use Synonyms", value=True)
    with col2:
        introduction = st.checkbox("Generate Introduction", value=False)
        mrlap = st.checkbox("Use MRlap", value=False, disabled=True)
    with col3:
        mr_quality_evaluation = st.checkbox("MR Quality Evaluation", value=False, disabled=True)
        num_articles = st.slider("Number of Articles", min_value=10, max_value=500, value=100, step=10)

# 运行步骤选择
st.markdown("### Run Steps")
col1, col2, col3 = st.columns(3)
with col1:
    step1 = st.checkbox("Step 1: Identify Exposure and Outcome", value=True)
    step2 = st.checkbox("Step 2: Check Previous MR Analyses", value=True)
    step3 = st.checkbox("Step 3: Synonym Expansion", value=True)
with col2:
    step4 = st.checkbox("Step 4: Check OpenGWAS Availability", value=True)
    step5 = st.checkbox("Step 5: Get GWAS IDs", value=True)
    step6 = st.checkbox("Step 6: Generate Combinations", value=True)
with col3:
    step7 = st.checkbox("Step 7: Check MR for New Combinations", value=True)
    step8 = st.checkbox("Step 8: Select Final Pairs for MR", value=True)
    step9 = st.checkbox("Step 9: Run MR Analysis", value=True)

# 运行按钮
run_button = st.button("Run MRAgent")

# 创建一个显示当前步骤的容器
step_status_container = st.empty()

# 创建一个区域用于显示命令行输出，设置固定高度和滚动条
st.markdown("### Python Output Log")
# 使用st.container和CSS来创建固定高度的滚动区域
python_output_container = st.container()
with python_output_container:
    # 使用st.markdown创建一个div，设置固定高度和滚动
    st.markdown("""
    <style>
    .python-output-area {
        height: 300px;
        overflow-y: auto;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        white-space: pre;
    }
    </style>
    """, unsafe_allow_html=True)

    # 创建输出区域
    python_output_area = st.empty()

# 创建一个区域用于显示R输出，设置固定高度和滚动条
st.markdown("### R Output Log")
# 使用st.container和CSS来创建固定高度的滚动区域
r_output_container = st.container()
with r_output_container:
    # 使用st.markdown创建一个div，设置固定高度和滚动
    st.markdown("""
    <style>
    .r-output-area {
        height: 300px;
        overflow-y: auto;
        background-color: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        font-family: monospace;
        white-space: pre;
    }
    </style>
    """, unsafe_allow_html=True)

    # 创建输出区域
    r_output_area = st.empty()

# 存储agent路径的会话状态变量
if 'agent_path' not in st.session_state:
    st.session_state.agent_path = None

# 存储输出文本的会话状态变量
if 'output_text' not in st.session_state:
    st.session_state.output_text = ""

if 'r_output_text' not in st.session_state:
    st.session_state.r_output_text = ""


# 捕获标准输出的函数
class CaptureOutput:
    def __init__(self):
        self.output_text = st.session_state.output_text

    def write(self, text):
        self.output_text += text
        st.session_state.output_text = self.output_text
        # 使用HTML div显示输出，以支持滚动
        python_output_area.markdown(f'<div class="python-output-area">{self.output_text}</div>', unsafe_allow_html=True)
        return len(text)

    def flush(self):
        pass


# 修改os.system函数以捕获R输出
original_os_system = os.system


def patched_os_system(command):
    if 'R ' in command:
        # 使用subprocess代替os.system来捕获输出
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 创建线程来读取输出
        def read_output(stream, output_text):
            for line in stream:
                output_text.append(line)

        r_output = []
        stdout_thread = threading.Thread(target=read_output, args=(process.stdout, r_output))
        stderr_thread = threading.Thread(target=read_output, args=(process.stderr, r_output))

        stdout_thread.start()
        stderr_thread.start()

        # 等待进程完成
        return_code = process.wait()

        # 等待线程完成
        stdout_thread.join()
        stderr_thread.join()

        # 更新R输出显示
        r_output_text = "".join(r_output)
        st.session_state.r_output_text += r_output_text
        # 使用HTML div显示输出，以支持滚动
        r_output_area.markdown(f'<div class="r-output-area">{st.session_state.r_output_text}</div>',
                               unsafe_allow_html=True)

        return return_code
    else:
        # 对于非R命令，使用原始的os.system
        return original_os_system(command)


# 替换os.system
os.system = patched_os_system


# 创建下载按钮的函数
def create_download_button(path):
    if os.path.exists(path):
        # 创建一个内存中的ZIP文件
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            # 遍历目录并添加所有文件
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 计算相对路径，以便在ZIP中保持目录结构
                    rel_path = os.path.relpath(file_path, os.path.dirname(path))
                    zip_file.write(file_path, rel_path)

        # 重置缓冲区位置到开始
        zip_buffer.seek(0)

        # 创建下载按钮
        st.download_button(
            label="Download Results as ZIP",
            data=zip_buffer,
            file_name=f"MRAgent_results_{time.strftime('%Y%m%d_%H%M%S')}.zip",
            mime="application/zip",
            key=f"download_{time.time()}"
        )


# 初始化agent的函数
def initialize_agent():
    # 验证必填字段
    if not ai_key:
        st.error("AI Key is required.")
        return None

    if mode == "Knowledge Discovery" and not (exposure or outcome):
        st.error("Either Exposure or Outcome must be provided for Knowledge Discovery mode.")
        return None

    if mode == "Causal Validation" and (not exposure or not outcome):
        st.error("Both Exposure and Outcome are required for Causal Validation mode.")
        return None

    # 根据模式创建适当的MRAgent实例
    if mode == "Knowledge Discovery":
        agent_mode = 'O' if outcome else 'E'
        agent = MRAgent(
            mode=agent_mode,
            exposure=exposure,
            outcome=outcome,
            AI_key=ai_key,
            model=mr_model,
            num=num_articles,
            bidirectional=bidirectional,
            synonyms=synonyms,
            introduction=introduction,
            LLM_model=llm_model,
            base_url=base_url if base_url else None,
            gwas_token=gwas_token,
            opengwas_mode='online',
            mrlap=mrlap,
            mr_quality_evaluation=mr_quality_evaluation
        )
    else:  # Causal Validation
        agent = MRAgentOE(
            exposure=exposure,
            outcome=outcome,
            AI_key=ai_key,
            model=mr_model,
            bidirectional=bidirectional,
            synonyms=synonyms,
            introduction=introduction,
            LLM_model=llm_model,
            base_url=base_url if base_url else None,
            gwas_token=gwas_token,
            opengwas_mode='online',
            mrlap=mrlap,
            mr_quality_evaluation=mr_quality_evaluation
        )

    return agent


# 运行单个步骤并更新UI
def run_step(agent, step_num):
    # 更新步骤状态
    step_descriptions = {
        1: "Identifying Exposure and Outcome",
        2: "Checking Previous MR Analyses",
        3: "Expanding Synonyms",
        4: "Checking OpenGWAS Availability",
        5: "Getting GWAS IDs",
        6: "Generating Combinations",
        7: "Checking MR for New Combinations",
        8: "Selecting Final Pairs for MR",
        9: "Running MR Analysis (Please be patient, as this may take some time to complete.)"
    }

    # 使用进度条显示当前步骤
    step_status_container.info(f"Running Step {step_num}: {step_descriptions.get(step_num, '')}")

    # 创建输出捕获器
    capture = CaptureOutput()

    # 重定向标准输出
    old_stdout = sys.stdout
    sys.stdout = capture

    try:
        # 运行特定步骤
        agent.run(step=[step_num])

        # 保存路径到会话状态
        st.session_state.agent_path = agent.path

        return True
    except Exception as e:
        st.error(f"An error occurred during step {step_num}: {str(e)}")
        return False
    finally:
        # 恢复标准输出
        sys.stdout = old_stdout


# 当运行按钮被点击时执行
if run_button:
    # 清空输出文本
    st.session_state.output_text = ""
    st.session_state.r_output_text = ""
    python_output_area.markdown('<div class="python-output-area"></div>', unsafe_allow_html=True)
    r_output_area.markdown('<div class="r-output-area"></div>', unsafe_allow_html=True)

    # 初始化agent
    agent = initialize_agent()
    if agent:
        # 确定要运行的步骤
        steps_to_run = []
        if step1: steps_to_run.append(1)
        if step2: steps_to_run.append(2)
        if step3: steps_to_run.append(3)
        if step4: steps_to_run.append(4)
        if step5: steps_to_run.append(5)
        if step6: steps_to_run.append(6)
        if step7: steps_to_run.append(7)
        if step8: steps_to_run.append(8)
        if step9: steps_to_run.append(9)

        # 逐步运行
        for step in steps_to_run:
            success = run_step(agent, step)
            if not success:
                break
            time.sleep(1)  # 给UI更新一点时间

        # 所有步骤完成后，清除步骤状态
        step_status_container.empty()

# 显示结果（无论是否刚刚运行，只要有路径就显示）
if 'agent_path' in st.session_state and st.session_state.agent_path:
    if os.path.exists(st.session_state.agent_path):
        st.markdown("### Results")

        # 显示Exposure_and_Outcome.csv
        st.markdown("#### Exposure and Outcome")
        exposure_outcome_path = os.path.join(st.session_state.agent_path, 'Exposure_and_Outcome.csv')
        if os.path.exists(exposure_outcome_path):
            try:
                df = pd.read_csv(exposure_outcome_path)
                edited_df = st.data_editor(df, key='exposure_outcome_editor')
                if st.button("Save changes to Exposure and Outcome", key='save_exposure_outcome'):
                    edited_df.to_csv(exposure_outcome_path, index=False)
                    st.success("Exposure and Outcome CSV saved successfully.")
            except Exception as e:
                st.info(f"Could not load Exposure_and_Outcome.csv: {str(e)}")
        else:
            st.info("Exposure_and_Outcome.csv not found")

        # 显示Outcome_SNP.csv
        st.markdown("#### Outcome SNP")
        outcome_snp_path = os.path.join(st.session_state.agent_path, 'Outcome_SNP.csv')
        if os.path.exists(outcome_snp_path):
            try:
                df = pd.read_csv(outcome_snp_path)
                edited_df = st.data_editor(df, key='outcome_snp_editor')
                if st.button("Save changes to Outcome SNP", key='save_outcome_snp'):
                    edited_df.to_csv(outcome_snp_path, index=False)
                    st.success("Outcome SNP CSV saved successfully.")
            except Exception as e:
                st.info(f"Could not load Outcome_SNP.csv: {str(e)}")
        else:
            st.info("Outcome_SNP.csv not found")

        # 显示mr_run.csv
        st.markdown("#### MR Run")
        mr_run_path = os.path.join(st.session_state.agent_path, 'mr_run.csv')
        if os.path.exists(mr_run_path):
            try:
                df = pd.read_csv(mr_run_path)
                edited_df = st.data_editor(df, key='mr_run_editor')
                if st.button("Save changes to MR Run", key='save_mr_run'):
                    edited_df.to_csv(mr_run_path, index=False)
                    st.success("MR Run CSV saved successfully.")
            except Exception as e:
                st.info(f"Could not load mr_run.csv: {str(e)}")
        else:
            st.info("mr_run.csv not found")

        # 在最后面显示下载按钮
        st.markdown("#### Download Results")
        create_download_button(st.session_state.agent_path)


# # 百度统计
components.html(
'''
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?d8a4c130d7263e954bf9df2496e692c3";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>

''',
    height=30)
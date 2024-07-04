# MRAgent: LLM-based Automatic Two-sample Mendelian Randomization Agent


## Abstract
Mendelian randomization (MR) is a powerful analytical method that uses genetic variation to infer causal relationships between modifiable exposures and health outcomes. Despite the availability of standardized MR analysis pipelines, such as the TwoSampleMR R package, the process still requires significant intellectual input from professionals, including tasks such as Genome-Wide Association Study (GWAS) data selection, script writing, and result interpretation. With the advent of Large Language Models (LLMs) demonstrating human-level intelligence, LLM-based agents have shown potential in perceiving external information and executing actions, inspiring the development of automated MR analysis tools. Here, we propose the LLM-based automatic Mendelian randomization agent (MRAgent). MRAgent provides an automated analysis pipeline, replacing the manual components of traditional MR analysis. It autonomously scans and analyzes relevant literature, identifies potential exposures or outcomes related to diseases, and performs MR analysis to determine causal relationships, generating comprehensive reports. We designed experiments for automatic evaluation and human evaluation to compare the performance of different LLMs in operating MRAgent. Additionally, we provide a proof-of-concept case demonstrating the complete workflow. MRAgent offers clinicians and researchers a rapid and reliable tool for exploring and validating the causal factors associated with diseases, significantly reducing the time and expertise required for MR studies.

## MRAgent Architecture
![MRAgent Architecture](./images/f1.png)

## MRAgent Workflow
<div align="center">
	<img src="./images/f2.png" width="60%">
</div>


## Preparation
### LLMs API Key
Before using MRAgent, you need to obtain the API Key for the LLMs, or run the LLM locally.
The following LLM APIs are currently supported:

- [OpenAI GPT](https://platform.openai.com/docs/overview) 
- [Google Gemini](https://ai.google.dev/#gemini-api)
- [Anthropic Claude](https://www.anthropic.com/claude)
- [Aliyun Qwen](https://help.aliyun.com/zh/dashscope/developer-reference/api-details?disableWebsiteRedirect=true)

You can also run LLM locally, and we currently support all open source models running on ollama:

[Ollama](https://markdown.com.cn)
     
You need to follow the steps to install ollama and follow the ollama python support package:
```shell
pip install ollama
```
### GWAS token
You need to get the **GWAS token** for the OpenGWAS data.
- [OpenGWAS API](https://api.opengwas.io/)

## Usage
### "Knowledge Discovery" mode
> TODO
### "Causal Validation" mode
> TODO

## Experiments
> TODO
> 
## Citation
> TODO
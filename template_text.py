MRorNot_text = """Here are articles about {Exposure} and {Outcome} from PubMed, presented in JSON format with the index, title, and abstract of each article. 
Please review each paper sequentially. If the Exposure: {Exposure} and Outcome: {Outcome} have been studied using Mendelian randomization, print the title of the relevant study. If none of the articles have studied the exposure and outcome, print "Exposure and Outcome were not subjected to Mendelian randomization." 
Please note that you only need to output either the title or the phrase "Exposure and Outcome were not subjected to Mendelian randomization.", without any additional words or symbols. 
Once again, please carefully evaluate each paper and output the results accordingly.

json file:
{pubmed_out}"""

pubmed_text = """Below I will give index, title and abstract of most recent {num} paper related to {Outcome} in json format.
Please read each paper in turn, help me find the {Outcome} with what has done correlation studies but not causal inference, which can be further Mendelian randomization studies in the future.

Carefully read each paper and output the judgment results for each article. If a Mendelian randomization study can be performed, explicitly output Outcome and Exposure and the title of the corresponding article. If there are more than one Exposure and Outcome in an article, you should output more than one Exposure and Outcome, as well as the title of the corresponding article. 

The output json list format is as follows:
[{{"index":xxx, "Outcome": xxx, "Exposure": xxx, "title": xxx}},{{"index":xxx, "Outcome": xxx, "Exposure": xxx, "title": xxx}}, …, {{"index":xxx, "Outcome": xxx, "Exposure": xxx, "title": xxx}}]
        
Again, carefully judge each paper and output the results. The results must be output strictly in the required format.

json file:
{pubmed_out}"""

pubmed_text_obo = """Below I will give title and abstract of most recent paper related to {Outcome}.
Please read the paper and help me determine if {Outcome} in the paper has done a correlation study with an influencing factor or another disease, but no causal inference has been made. This can be done in the future with further Mendelian randomisation studies.
Carefully read paper and output the judgment results. If a Mendelian randomization study can be performed, explicitly output Outcome and Exposure.Here Outcome or Exposure should be related to the {Outcome}. If there are more than one Exposure and Outcome in an article, you should output more than one Exposure and Outcome, as well as the title of the corresponding article. 
The output json list format is as follows:
[{{"Outcome": "xxx", "Exposure": "xxx"}},{{"Outcome": "xxx", "Exposure": "xxx"}}, …, {{"Outcome": "xxx", "Exposure": "xxx"}}]
If you think that the paper does not meet the requirements, please output "[{{"Outcome": null, "Exposure": null}}]" directly.

title:
{title}

abstract:
{abstract}

Again, carefully judge each paper and output the results. The results must be output strictly in the required format. Please do not output any extra characters.
"""

synonyms_text = """Please help me find synonyms for "{OE}" in the medical field. If the number of synonyms is more than 7, just output the 7 most relevant synonyms. Output in csv list format.
Note that you only need to output synonyms and commas in csv format, not any other text or symbols(including '' "" . :)."""

gwas_id_text = """When conducting a Mendelian randomization study, it is often necessary to find the SNPs associated with the study in the OpenGWAS database and record the GWAS ID.
Below is the result of searching in OpenGWAS using the keyword {keyword}, output in json list format, saving the GWAS ID,Year,Trait,Consortium,Sample size,Number of SNPs.
I want to get the most suitable GWAS ID, please help me with the following tasks.
1. You are asked to read the Trait and find out if there is a Trait that directly matches {keyword}, and if not, find the Trait that is most relevant to {keyword}.
2. If there are several matching or related Trait at the same time, these can be output at the same time.
3. Output the final corresponding GWAS ID. Output in python list format.

Note that you only need to output gwas_id and the comma in python list format:
['gwas_id1', 'gwas_id2', …, 'gwas_idn']

There is no need to output any other text, including steps, explanations, thought processes, etc. There is no need to output any additional symbols. (including '' "" . :).

json list:
{json_list}"""

LLM_MR_template = """Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}), please read and understand the results in the table and generate a paragraph describing the results in detail in academic language. Typically, significance can be judged by the Inverse variance weighted method of pval<0.05. or>1 there is a positive correlation and or<1 there is a negative correlation.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}"""


LLM_MR_MOE_template = """Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}).
Mendelian randomization analysis was performed based on the Mixture of experts (MOE) function in TwoSampleMR. Once all MR methods have been applied to a summary set, you can then use the mixture of experts to predict the method most likely to be the most accurate. The MOE column, which is a predictor for each method for how well it performs in terms of high power and low type 1 error (scaled 0-1, where 1 is best performance). It orders the table to be in order of best performing method.
Please read and understand the results in the table and generate a paragraph describing the results in detail in academic language.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}"""

LLM_conclusion_template = """Below is all results report of Mendelian randomization analysis with Exposure: {Exposure} and Outcome: {Outcome}.
I conducted MR studies using different SNPs from Outcome and Exposure in the openGWAS database. Below are the results of the study for the different SNPs, differentiated by GWAS ID. Please help me to summarise the above results and write CONCLUSION in academic language to analyse whether there is a causal effect of Outcome: {Outcome} and Exposure: {Exposure}.
If a causal effect exists, it should be written which Exposure_id and Outcome_id are present in the analysis. If there is no causal effect, it should be made clear that there is no evidence to support a causal inference between Exposure and Outcome.
Try to specify in the analysis which SNPs (Exposure_id and Outcome_id) got this sentence analysed.

# Mendelian randomization analysis results
{MRresult}
"""

LLM_Introduction_template = """I have completed a Mendelian randomization analysis of Exposure: {Exposure} and Outcome: {Outcome}, and I am going to write a paper on this analysis. Please help me write an introduction according to the following:
1. Introduce the current state of research on {Outcome} and its shortcomings
2. Propose the hypothesis that Outcome: {Outcome} may be related to Exposure: {Exposure}.
3. Analyse the effect of Exposure: {Exposure} on Outcome: {Outcome} using Mendelian Randomization analysis.
Note that you should refer to the literature given below when writing the Introduction and label the referenced literature in APA format.

Below I found some related articles on PubMed for your reference:
About {Exposure}.
{Exposure_pubmed}

About {Outcome}.
{Outcome_pubmed}

About {Exposure} and {Outcome}.
{Exposure_Outcome_pubmed}
"""
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
{pleiotropy}

I will also give another completed report for your reference.

The referenced report:

Mendelian randomization (MR) analyses of fresh fruit intake (ukb-b-3881) and asthma (finn-b-J10_ASTHMA) was conducted using summary data from genome-wide association studies (GWAS). Five different MR methods including MR Egger regression, weighted median, inverse variance weighted, simple mode and weighted mode were applied. 53 single nucleotide polymorphisms (SNPs) were included in the final MR analysis.

The MR analyses provided evidence that higher fruit intake causally decreases asthma risk. Specifically, the inverse-variance weighted (IVW) algorithm showed a statistically significant association between fruit intake and lower asthma risk (OR = 0.509, 95% CI: 0.334 - 0.775; P = 0.001). Furthermore, this causal association was supported by the weighted median (OR = 0.499, 95% CI: 0.274 - 0.907; P = 0.02). All methods were directionally consistent.

A series of sensitivity analyses were conducted to evaluate potential sources of bias heterogeneity and pleiotropy in our MR analysis. First, we conducted heterogeneity testing using the IVW and MR-Egger methods, and the results revealed no heterogeneity among the instruments (Q pval >0.05). Next, MR-Egger regression intercepts were examined to detect the horizontal pleiotropy, defined as a genetic variant influencing both exposure and outcome through independent biological pathways and no evidence of pleiotropy was identified (P = 0.44).  

In summary, this Mendelian randomization analysis provides supportive evidence that higher fresh fruit intake has a causal protective effect on reducing asthma risk. Sensitivity analyses validated the robustness of these causal relationships against biases from pleiotropy, outliers or reverse causation.
"""


LLM_MR_MOE_template = """Below is a csv file of the results of Mendelian randomization analysis with Exposure: {Exposure} (GWAS ID: {Exposure_id}) and Outcome: {Outcome} (GWAS ID: {Outcome_id}).
Mendelian randomization analysis was performed based on the Mixture of experts (MOE) function in TwoSampleMR. Once all MR methods have been applied to a summary set, you can then use the mixture of experts to predict the method most likely to be the most accurate. The MOE column, which is a predictor for each method for how well it performs in terms of high power and low type 1 error (scaled 0-1, where 1 is best performance). It orders the table to be in order of best performing method.
Please read and understand the results in the table and generate a paragraph describing the results in detail in academic language.

#Mendelian randomization analysis results table
{MRresult}

#Heterogeneity analysis results table
{heterogeneity}

#Pleiotropy test results table
{pleiotropy}

I will also give another completed report for your reference.

The referenced report:
The Mendelian randomization (MR) analysis, leveraging the Mixture of experts (MOE) function in TwoSampleMR, investigated the causal relationship between Type 2 diabetes (Exposure; GWAS ID: ebi-a-GCST006867) and Bone mineral density (Outcome; GWAS ID: ebi-a-GCST90014022). The results span various MR methods, displaying a range of estimates for the causal effect, alongside their precision and statistical significance.

The Penalised mode method yielded a statistically significant association (b = 0.0330, SE = 0.0083, CI: 0.0168 to 0.0493, p = 0.00012), suggesting a potential causal relationship between Type 2 diabetes and an increased risk of Bone mineral density. This outcome was corroborated by the Random Effects Inverse Variance Weighted (RE IVW) and Fixed Effects Egger (FE Egger) methods, although with varying effect sizes and confidence intervals, indicating some differences in the robustness and interpretation of the causal estimate across these methods.

The analysis performed checks for both heterogeneity and pleiotropy, critical aspects that can affect the validity of MR estimates. The heterogeneity analysis, assessed through the Cochran’s Q test, indicated no significant heterogeneity across the instrumental variables used in the IVW (Q = 1159.35, P = 1.46E-173) and Egger (Q = 1160.9793, P = 2.1555E-174) methods, suggesting that the instrumental variables contributed similarly to the estimation of the causal effect. The pleiotropy test, using the Egger intercept, showed no evidence of pleiotropy (intercept = 0.000795, SE = 0.00162, p = 0.625171), implying that the instrumental variables were not affecting the outcome through pathways other than the exposure, thus supporting the validity of the MR findings.

These comprehensive analyses, when considered together, provide evidence to suggest a potential causal association between Type 2 diabetes and Bone mineral density. The consistency of significant findings across multiple MR methods strengthens the confidence in the observed association, albeit recognizing the importance of further investigative studies to confirm these results and elucidate underlying mechanisms.
"""



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

LLM_template_MR_effect_evaluation = """
Below is an article on a Mendelian randomization study. Please read it carefully and assess its adherence to the STROBE-MR checklist. For each item on the checklist, return a JSON object where each item (including sub-items, such as 4(a)) is marked as "yes" or "no" based on the article's content. Only provide the JSON output without any additional explanation or commentary. This means you should strictly return the JSON object without any text before or after it.

STROBE-MR Checklist Items:

TITLE and ABSTRACT:
   - 1. Indicate Mendelian randomization (MR) as the study’s design in the title and/or the abstract if that is a main purpose of the study.

INTRODUCTION:
   - 2. Background: Explain the scientific background and rationale for the reported study. What is the exposure? Is a potential causal relationship between exposure and outcome plausible? Justify why MR is a helpful method to address the study question.
   - 3. Objectives: State specific objectives clearly, including pre-specified causal hypotheses (if any). State that MR is a method that, under specific assumptions, intends to estimate causal effects.

METHODS:
   - 4. Study design and data sources:
     a) Setting: Describe the study design and the underlying population, if possible. Describe the setting, locations, and relevant dates, including periods of recruitment, exposure, follow-up, and data collection, when available.
     b) Participants: Give the eligibility criteria, and the sources and methods of selection of participants. Report the sample size, and whether any power or sample size calculations were carried out prior to the main analysis.
     c) Describe measurement, quality control and selection of genetic variants.
     d) For each exposure, outcome, and other relevant variables, describe methods of assessment and diagnostic criteria for diseases.
     e) Provide details of ethics committee approval and participant informed consent, if relevant.

   - 5. Assumptions: Explicitly state the three core IV assumptions for the main analysis (relevance, independence and exclusion restriction) as well assumptions for any additional or sensitivity analysis.

   - 6. Statistical methods: main analysis:
     a) Describe how quantitative variables were handled in the analyses (i.e., scale, units, model).
     b) Describe how genetic variants were handled in the analyses and, if applicable, how their weights were selected.
     c) Describe the MR estimator (e.g., two-stage least squares, Wald ratio) and related statistics. Detail the included covariates and, in case of two-sample MR, whether the same covariate set was used for adjustment in the two samples.
     d) Explain how missing data were addressed.
     e) If applicable, indicate how multiple testing was addressed.

   - 7. Assessment of assumptions: Describe any methods or prior knowledge used to assess the assumptions or justify their validity.

   - 8. Sensitivity analyses and additional analyses: Describe any sensitivity analyses or additional analyses performed (e.g., comparison of effect estimates from different approaches, independent replication, bias analytic techniques, validation of instruments, simulations).

   - 9. Software and pre-registration:
     a) Name statistical software and package(s), including version and settings used.
     b) State whether the study protocol and details were pre-registered (as well as when and where).

RESULTS:
   - 10. Descriptive data:
     a) Report the numbers of individuals at each stage of included studies and reasons for exclusion. Consider use of a flow diagram.
     b) Report summary statistics for phenotypic exposure(s), outcome(s), and other relevant variables (e.g., means, SDs, proportions).
     c) If the data sources include meta-analyses of previous studies, provide the assessments of heterogeneity across these studies.
     d) For two-sample MR:
        i. Provide justification of the similarity of the genetic variant-exposure associations between the exposure and outcome samples.
        ii. Provide information on the number of individuals who overlap between the exposure and outcome studies.

   - 11. Main results:
     a) Report the associations between genetic variant and exposure, and between genetic variant and outcome, preferably on an interpretable scale.
     b) Report MR estimates of the relationship between exposure and outcome, and the measures of uncertainty from the MR analysis, on an interpretable scale, such as odds ratio or relative risk per SD difference.
     c) If relevant, consider translating estimates of relative risk into absolute risk for a meaningful time period.
     d) Consider plots to visualize results (e.g., forest plot, scatterplot of associations between genetic variants and outcome versus between genetic variants and exposure).

   - 12. Assessment of assumptions:
     a) Report the assessment of the validity of the assumptions.
     b) Report any additional statistics (e.g., assessments of heterogeneity across genetic variants, such as I2, Q statistic or E-value).

   - 13. Sensitivity analyses and additional analyses:
     a) Report any sensitivity analyses to assess the robustness of the main results to violations of the assumptions.
     b) Report results from other sensitivity analyses or additional analyses.
     c) Report any assessment of direction of causal relationship (e.g., bidirectional MR).
     d) When relevant, report and compare with estimates from non-MR analyses.
     e) Consider additional plots to visualize results (e.g., leave-one-out analyses).

DISCUSSION:
   - 14. Key results: Summarize key results with reference to study objectives.
   - 15. Limitations: Discuss limitations of the study, taking into account the validity of the IV assumptions, other sources of potential bias, and imprecision. Discuss both direction and magnitude of any potential bias and any efforts to address them.
   - 16. Interpretation:
     a) Meaning: Give a cautious overall interpretation of results in the context of their limitations and in comparison with other studies.
     b) Mechanism: Discuss underlying biological mechanisms that could drive a potential causal relationship between the investigated exposure and the outcome, and whether the gene-environment equivalence assumption is reasonable. Use causal language carefully, clarifying that IV estimates may provide causal effects only under certain assumptions.
     c) Clinical relevance: Discuss whether the results have clinical or public policy relevance, and to what extent they inform effect sizes of possible interventions.

   - 17. Generalizability: Discuss the generalizability of the study results (a) to other populations, (b) across other exposure periods/timings, and (c) across other levels of exposure.

OTHER INFORMATION:
   - 18. Funding: Describe sources of funding and the role of funders in the present study and, if applicable, sources of funding for the databases and original study or studies on which the present study is based.
   - 19. Data and data sharing: Provide the data used to perform all analyses or report where and how the data can be accessed, and reference these sources in the article. Provide the statistical code needed to reproduce the results in the article, or report whether the code is publicly accessible and if so, where.
   - 20. Conflicts of Interest: All authors should declare all potential conflicts of interest.

Example Output: {{"1": "yes", "2": "no", "3": "yes", "4a": "yes", "4b": "no", "4c": "yes", "4d": "yes", "4e": "no", "5": "yes", "6a": "no", "6b": "yes", "6c": "yes", "6d": "no", "6e": "yes", "7": "no", "8": "yes", "9a": "yes", "9b": "no", "10a": "yes", "10b": "no", "10c": "yes", "10d_i": "no", "10d_ii": "yes", "11a": "yes", "11b": "no", "11c": "yes", "11d": "no", "12a": "yes", "12b": "no", "13a": "yes", "13b": "no", "13c": "yes", "13d": "no", "13e": "yes", "14": "no", "15": "yes", "16a": "no", "16b": "yes", "16c": "no", "17": "yes", "18": "no", "19": "yes", "20": "no"}}


The following is the full text, recorded in json format:
{paper_details}
"""


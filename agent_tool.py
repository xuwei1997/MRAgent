# import json
from Bio import Entrez
import requests
from bs4 import BeautifulSoup
# import pandas as pd
# # from rpy2.robjects import r
# import time
# import subprocess
import os
import json
# import re
import time


# 爬虫爬取PubMed数据
def pubmed_crawler(keyword, num_records, sort_order, json_str=True):
    Entrez.email = '670525744@qq.com'  # 请替换为你的邮箱

    def search_pubmed(keyword, num_records, sort_order):
        handle = Entrez.esearch(db='pubmed',
                                sort=sort_order,
                                retmax=str(num_records),
                                retmode='xml',
                                term=keyword)
        results = Entrez.read(handle)
        return results

    def fetch_details(id_list):
        ids = ','.join(id_list)
        handle = Entrez.efetch(db='pubmed',
                               retmode='xml',
                               id=ids)
        results = Entrez.read(handle, validate=False)
        return results

    def get_paper_details(paper):
        try:
            title = paper['MedlineCitation']['Article']['ArticleTitle']
        except KeyError:
            title = 'NULL'

        try:
            abstract = paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
        except KeyError:
            abstract = 'NULL'

        return title, abstract

    def search_and_print_papers(keyword, num_records, sort_order):
        results = search_pubmed(keyword, num_records, sort_order)
        # print(results)
        id_list = results['IdList']
        if len(id_list) == 0:
            return json.dumps([{
                'index': 0,
                'title': 'No paper found',
                'abstract': 'No paper found'
            }])
        papers = fetch_details(id_list)
        # print(papers)
        paper_details = []
        for i, paper in enumerate(papers['PubmedArticle'], start=1):
            title, abstract = get_paper_details(paper)
            paper_details.append({
                'index': i,
                'title': title,
                'abstract': abstract
            })
        if json_str:
            return json.dumps(paper_details)
        else:
            return paper_details

    return search_and_print_papers(keyword, num_records, sort_order)


# 获取PubMed数据库中某个文章的详细信息
def get_paper_details(paper_title):
    Entrez.email = 'xuwei_chn@foxmail.com'  # 请替换为你的邮箱

    def search_pubmed(keyword, num_records, sort_order):
        handle = Entrez.esearch(db='pubmed',
                                sort=sort_order,
                                retmax=str(num_records),
                                retmode='xml',
                                term=keyword)
        results = Entrez.read(handle)
        return results

    def fetch_details(id_list):
        ids = ','.join(id_list)
        handle = Entrez.efetch(db='pubmed',
                               retmode='xml',
                               id=ids)
        results = Entrez.read(handle)
        return results

    def search_and_print_papers(keyword):
        results = search_pubmed(keyword, 1, 'relevance')
        # print(results)
        id_list = results['IdList']
        papers = fetch_details(id_list)
        paper = papers['PubmedArticle'][0]

        try:
            title = paper['MedlineCitation']['Article']['ArticleTitle']
        except KeyError:
            title = 'NULL'

        try:
            abstract = paper['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
        except KeyError:
            abstract = 'NULL'

        try:
            PMID = paper['MedlineCitation']['PMID']
        except KeyError:
            PMID = 'NULL'

        try:
            DOI = paper['MedlineCitation']['Article']['ELocationID'][0]
        except KeyError:
            DOI = 'NULL'

        try:
            Journal = paper['MedlineCitation']['Article']['Journal']['Title']
        except KeyError:
            Journal = 'NULL'

        try:
            Author = paper['MedlineCitation']['Article']['AuthorList'][0]['LastName']
        except KeyError:
            Author = 'NULL'

        try:
            Year = paper['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate']['Year']
        except KeyError:
            Year = 'NULL'

        print(title)
        print(PMID)
        print(DOI)
        print(Journal)
        print(Author)
        print(Year)
        print(abstract)
        return [title, PMID, DOI, Journal, Author, Year, abstract]

    return search_and_print_papers(paper_title)


# 检测关键词是否在OpenGWAS数据库中有对应的SNP
def check_keyword_in_opengwas(keyword):
    # OpenGWAS网页地址
    url = f"https://gwas.mrcieu.ac.uk/datasets/?trait__icontains={keyword}"

    # 发送GET请求
    response = requests.get(url)

    # 检查响应状态码
    if response.status_code == 200:
        # 如果状态码为200，表示请求成功
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # print(soup.text)
        # 检查是否存在指定的文本
        if "Filtered to 0 records" in soup.text:
            print(f"No SNP related to '{keyword}' was found in the OpenGWAS database.")
            return False
        else:
            print(f"SNP(s) related to '{keyword}' exist in the OpenGWAS database.")
            return True
    else:
        # 其他状态码表示发生了错误
        print(f"An error occurred while querying the OpenGWAS database. Status code: {response.status_code}")
        return None


# 获取OpenGWAS数据库中的GWAS ID
def get_gwas_id(keyword):
    def remove_newlines(lst):
        # Remove /n from each string in a list
        return [s.replace('\n', '') for s in lst]

    data = []
    for i in range(1, 11):
        # OpenGWAS网页地址
        url = f"https://gwas.mrcieu.ac.uk/datasets/?trait__icontains={keyword}&page={i}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        headers = [header.text for header in table.find_all('th')]
        headers = remove_newlines(headers)
        rows = table.find_all('tr')
        for row in rows[1:]:
            values = [value.text for value in row.find_all('td')]
            data.append(dict(zip(headers, values)))

    # data去重
    data = [dict(t) for t in {tuple(d.items()) for d in data}]
    print(data)

    return data


def MRtool(Exposure_id, Outcome_id, path, gwas_token):
    # 等待5s
    time.sleep(5)

    r_script = """
    #引用包
    Sys.setenv(OPENGWAS_JWT="{gwas_token}")
    library(TwoSampleMR)
    library(ieugwasr)
    
    # options(ieugwasr_api = 'gwas-api.mrcieu.ac.uk/')
    
    
    num_rows <- 0
    tryCatch({{
      p_value <- 5e-08
      exposure_dat <- extract_instruments(outcomes = '{Exposure_id}',
                                          p1=p_value,
                                          clump=TRUE,
                                          r2=0.001,
                                          kb=5000
      )
      num_rows <- nrow(exposure_dat)
      print(num_rows)
    }}, error = function(e) {{
      message("First time gwas data error.", e$message)
    }})
    
    if (num_rows < 11) {{
      tryCatch({{
        p_value <- 5e-06
        exposure_dat <- extract_instruments(outcomes = '{Exposure_id}',
                                            p1=p_value,
                                            clump=TRUE,
                                            r2=0.001,
                                            kb=5000
        )
        num_rows <- nrow(exposure_dat)
        print(num_rows)
      }}, error = function(e) {{
        message("Second time gwas data error. ", e$message)
      }})
    }}
    
    if (num_rows < 11) {{
      tryCatch({{
        p_value <- 5e-05
        exposure_dat <- extract_instruments(outcomes = '{Exposure_id}',
                                            p1=p_value,
                                            clump=TRUE,
                                            r2=0.001,
                                            kb=5000
        )
        num_rows <- nrow(exposure_dat)
        print(num_rows)
      }}, error = function(e) {{
        message("Third time gwas data error.", e$message)
      }})
    }}
    
    
    outcomeID="{Outcome_id}"
    #提取结局数据
    outcome_dat <- extract_outcome_data(snps=exposure_dat$SNP, outcomes=outcomeID)
    dat <- harmonise_data(exposure_dat, outcome_dat)
    outTab=dat[dat$mr_keep=="TRUE",]
    write.csv(outTab, file=".//{path}//table.SNP.csv", row.names=F)

    #孟德尔随机化分析
    mrResult=mr(dat)
    #mr_method_list()$obj
    # mrResult=mr(dat, method_list=c("mr_ivw", "mr_egger_regression", "mr_weighted_median", "mr_simple_mode", "mr_weighted_mode"))
    #对结果进行OR值的计算
    mrTab=generate_odds_ratios(mrResult)
    write.csv(mrTab, file=".//{path}//table.MRresult.csv", row.names=F)


    #异质性分析
    heterTab=mr_heterogeneity(dat)
    write.csv(heterTab, file=".//{path}//table.heterogeneity.csv", row.names=F)

    #多效性检验
    pleioTab=mr_pleiotropy_test(dat)
    write.csv(pleioTab, file=".//{path}//table.pleiotropy.csv", row.names=F)

    #绘制散点图
    pdf(file=".//{path}//pic.scatter_plot.pdf", width=7.5, height=7)
    mr_scatter_plot(mrResult, dat)
    dev.off()

    #森林图
    res_single=mr_singlesnp(dat)      #得到每个工具变量对结局的影响
    pdf(file=".//{path}//pic.forest.pdf", width=7, height=5.5)
    mr_forest_plot(res_single)
    dev.off()

    #漏斗图
    pdf(file=".//{path}//pic.funnel_plot.pdf", width=7, height=6.5)
    mr_funnel_plot(singlesnp_results = res_single)
    dev.off()

    #留一法敏感性分析
    pdf(file=".//{path}//pic.leaveoneout.pdf", width=7, height=5.5)
    mr_leaveoneout_plot(leaveoneout_results = mr_leaveoneout(dat))
    dev.off()

        """
    r_script_run = r_script.format(Exposure_id=Exposure_id, Outcome_id=Outcome_id, path=path, gwas_token=gwas_token)

    with open('test.R', 'w', encoding='utf-8') as f:
        f.write(r_script_run)

    os.system('R --slave --no-save --no-restore --no-site-file --no-environ -f  test.R --args')


def MRtool_MOE(Exposure_id, Outcome_id, path, gwas_token):
    # 等待5s
    time.sleep(5)

    r_script = """
    #引用包
    Sys.setenv(OPENGWAS_JWT="{gwas_token}")
    library(TwoSampleMR)
    library(ieugwasr)
    library(dplyr)
    
    # options(ieugwasr_api = 'gwas-api.mrcieu.ac.uk/')
    
    p_value <- 5e-08
    exposure_dat <- extract_instruments(outcomes = '{Exposure_id}',
                                        p1=p_value,
                                        clump=TRUE,
                                        r2=0.001,
                                        kb=5000,
                                        # access_token = NULL
    )
    
    num_rows <- nrow(exposure_dat)
    print(num_rows)
    if (num_rows < 5) {{
      p_value <- 5e-06
      exposure_dat <- extract_instruments(outcomes = '{Exposure_id}',
                                          p1=p_value,
                                          clump=TRUE,
                                          r2=0.001,
                                          kb=5000,
                                          # access_token = NULL
      )
        num_rows <- nrow(exposure_dat)
        print(num_rows)
    }}
    
    outcomeID="{Outcome_id}"
    #提取结局数据
    outcome_dat <- extract_outcome_data(snps=exposure_dat$SNP, outcomes=outcomeID)
    dat <- harmonise_data(exposure_dat, outcome_dat)
    outTab=dat[dat$mr_keep=="TRUE",]
    write.csv(outTab, file=".//{path}//table.SNP.csv", row.names=F)
    
    
    # Apply all MR methods
    r <- mr_wrapper(dat)
    
    # Load the rf object containing the trained models
    load("rf.rdata")
    # Update the results with mixture of experts
    r <- mr_moe(r, rf)
    
    # Now you can view the estimates, and see that they have
    # been sorted in order from most likely to least likely to
    # be accurate, based on MOE prediction
    r[[1]]$estimates
    head(r)
    
    # save the results csv
    write.csv(r[[1]]$estimates, file=".//{path}//MR.MRresult.csv", row.names=F)
    write.csv(r[[1]]$heterogeneity, file=".//{path}//MR.heterogeneity.csv", row.names=F)
    
    #异质性分析
    heterTab=mr_heterogeneity(dat)
    write.csv(heterTab, file=".//{path}//MR.table.heterogeneity.csv", row.names=F)
    
    #多效性检验
    pleioTab=mr_pleiotropy_test(dat)
    write.csv(pleioTab, file=".//{path}//MR.table.pleiotropy.csv", row.names=F)
    
    # #绘制散点图
    pdf(file=".//{path}//pic.scatter_plot.pdf", width=7.5, height=7)
    mr_scatter_plot(r[[1]]$estimates, dat)
    dev.off()
    
    #森林图
    res_single=mr_singlesnp(dat)      #得到每个工具变量对结局的影响
    pdf(file=".//{path}//pic.forest.pdf", width=7, height=5.5)
    mr_forest_plot(res_single)
    dev.off()
    
    #漏斗图
    pdf(file=".//{path}//pic.funnel_plot.pdf", width=7, height=6.5)
    mr_funnel_plot(singlesnp_results = res_single)
    dev.off()
    
    #留一法敏感性分析
    pdf(file=".//{path}//pic.leaveoneout.pdf", width=7, height=5.5)
    mr_leaveoneout_plot(leaveoneout_results = mr_leaveoneout(dat))
    dev.off()
    """
    r_script_run = r_script.format(Exposure_id=Exposure_id, Outcome_id=Outcome_id, path=path, gwas_token=gwas_token)

    with open('test.R', 'w', encoding='utf-8') as f:
        f.write(r_script_run)

    os.system('R --slave --no-save --no-restore --no-site-file --no-environ -f  test.R --args')


def get_synonyms(term, api_key):
    try:
        # 获取cui
        url = "https://uts-ws.nlm.nih.gov/rest/search/current?apiKey={apiKey}&string={term}&pageNumber=1&pageSize=1".format(
            apiKey=api_key, term=term)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text.encode('utf8'))
        cui = response.json()["result"]["results"][0]["ui"]
        # print(cui)

        # 获取同义词
        url = "https://uts-ws.nlm.nih.gov/rest/content/current/CUI/{cui}/atoms?apiKey={apiKey}&ttys=&language=ENG&pageSize=25".format(
            apiKey=api_key, cui=cui)
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.json())
        synonyms = [result["name"] for result in response.json()["result"]]

        # 全体小写
        synonyms = [synonym.lower() for synonym in synonyms]

        # 去重
        synonyms = list(set(synonyms))

    except Exception as e:
        print(e)
        synonyms = []

    # print(len(synonyms))
    print(synonyms)

    return synonyms


if __name__ == '__main__':
    # get_synonyms('BMI', 'd6382a8b-5ca8-493a-98ca-2b02fffcaeb5')
    print(get_gwas_id('BMI'))
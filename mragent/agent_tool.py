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
import urllib


def timer(func):
    def func_wrapper(*args, **kwargs):
        from time import time
        time_start = time()
        result = func(*args, **kwargs)
        time_end = time()
        time_spend = time_end - time_start
        print('%s cost time: %.3f s' % (func.__name__, time_spend))
        return result

    return func_wrapper


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
        print(papers)
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


def get_paper_details_pmc(paper_title):
    Entrez.email = 'xuwei_chn@foxmail.com'  # 请替换为你的邮箱

    def search_pubmed(keyword, num_records, sort_order):
        handle = Entrez.esearch(db='pubmed',
                                sort=sort_order,
                                retmax=str(num_records),
                                retmode='xml',
                                term=keyword)
        results = Entrez.read(handle)
        return results

    def get_pcm_full_text(pmc_id):
        # 直接访问接口网站获取json全文
        # https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/[ID]/unicode
        url = f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/{pmc_id}/unicode"
        print(url)
        response = urllib.request.urlopen(url)
        full_text = response.read().decode('utf-8')
        return full_text

    def search_and_print_papers(keyword):
        results = search_pubmed(keyword, 1, 'relevance')
        id_list = results['IdList']
        if len(id_list) == 0:
            print("No papers found for the given query.")
            return None
        else:
            paper_id = id_list[0]
            full_text = get_pcm_full_text(paper_id)
            if 'No record can be found for the input' in full_text:
                print("No full text found for the given query.")
                return None
            else:
                return full_text

    return search_and_print_papers(paper_title)


@timer
def MRtool(Exposure_id, Outcome_id, path, gwas_token):
    # 等待5s
    time.sleep(5)

    r_script = """
    # 安装并加载必要的包
    if (!requireNamespace("TwoSampleMR", quietly = TRUE)) {{
      install.packages("TwoSampleMR")
    }}
    if (!requireNamespace("ieugwasr", quietly = TRUE)) {{
      install.packages("ieugwasr")
    }}


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


@timer
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


@timer
def MRtool_MRlap(Exposure_id, Outcome_id, path, N_exposure, N_outcome):
    r_script = """
# 安装并加载必要的包
if (!requireNamespace("httr", quietly = TRUE)) {{
  install.packages("httr")
}}
if (!requireNamespace("vcfR", quietly = TRUE)) {{
  install.packages("vcfR")
}}
if (!requireNamespace("MRlap", quietly = TRUE)) {{
  install.packages("MRlap")
}}
if (!requireNamespace("jsonlite", quietly = TRUE)) {{
  install.packages("jsonlite")
}}

library(httr)
library(vcfR)
library(MRlap)
library(jsonlite)

# 定义下载函数
download_vcf <- function(base_url, file_name, dest_dir = ".", min_size = 1 * 1024 * 1024) {{  # min_size 默认 1MB
  # 提取文件标识符 (如 ukb-b-10807)
  file_id <- gsub("(.*)\\\.vcf\\\.gz", "\\\\1", file_name)

  # 构建完整的文件 URL (如 ukb-b-10807/ukb-b-10807.vcf.gz)
  file_url <- paste0(base_url, file_id, "/", file_name)
  print(paste("Attempting to download from:", file_url))

  # 构建文件的本地保存路径
  dest_file <- file.path(dest_dir, file_name)
  print(paste("Saving to:", dest_file))

  # 检查文件是否已经存在并且大小是否合适
  if (file.exists(dest_file)) {{
    file_info <- file.info(dest_file)
    file_size <- file_info$size

    # 如果文件存在且大小大于 1MB，则不重新下载
    if (file_size >= min_size) {{
      message(paste("File already exists and is larger than", round(min_size / (1024 * 1024), 2), "MB. Skipping download."))
      return(TRUE)  # 文件已经存在且大小合适，跳过下载
    }} else {{
      message(paste("File exists but is too small (", round(file_size / (1024 * 1024), 2), "MB). Redownloading..."))
    }}
  }}

  # 尝试直接下载文件，并捕获可能的错误
  tryCatch({{
    # 使用 curl 来下载并显示进度条
    download.file(file_url, destfile = dest_file, method = "curl", mode = "wb")

    # 下载完成后检查文件大小
    file_info <- file.info(dest_file)
    file_size <- file_info$size

    # 如果文件小于 1MB，视为下载失败
    if (file_size < min_size) {{
      message(paste("File size is too small (", round(file_size / (1024 * 1024), 2), "MB). Deleting file:", dest_file))
      file.remove(dest_file)  # 删除文件
      return(FALSE)  # 返回 FALSE 表示下载失败
    }} else {{
      message(paste("Download complete:", dest_file, "File size:", round(file_size / (1024 * 1024), 2), "MB"))
      return(TRUE)  # 返回 TRUE 表示下载成功
    }}

  }}, error = function(e) {{
    # 如果出现错误（如 404），处理错误
    if (grepl("404", e$message)) {{
      message(paste("File not found (404):", file_name))
    }} else {{
      message(paste("Error downloading file:", file_name, "Error message:", e$message))
    }}
    return(FALSE)  # 返回 FALSE 表示下载失败
  }})
}}

# 定义提取数据的函数
extract_data_from_vcf <- function(vcf_file, N) {{
  # 读取 VCF 文件
  vcf <- read.vcfR(vcf_file)

  # 查看样本列名，确保 sample_name 存在
  sample_columns <- colnames(vcf@gt)
  sample_name <- sample_columns[-1]  # 使用第一个样本列
  print("Available sample columns in the VCF:")
  print(sample_name)  # 打印使用的样本列名

  # 提取固定字段（CHROM, POS, ID, REF, ALT）
  fix_data <- as.data.frame(vcf@fix)

  # 检查 POS 列是否可以正确转换为数值
  print("Checking POS column:")
  print(summary(fix_data$POS))  # 打印 POS 列的摘要信息
  fix_data$POS <- as.numeric(fix_data$POS)
  if (any(is.na(fix_data$POS))) {{
    warning("Some positions (POS) could not be converted to numeric. Check the VCF file for inconsistencies.")
  }}

  # 提取基因型字段（ES, SE, LP, AF, ID）
  gt_data <- as.data.frame(vcf@gt)

  # 解析 GT 字段中的 ES, SE, LP, AF, ID
  gt_parsed <- do.call(rbind, strsplit(gt_data[, sample_name], ":"))

  # 检查 gt_parsed 的行数是否与 fix_data 的行数一致
  if (nrow(gt_parsed) != nrow(fix_data)) {{
    stop("The number of rows in the genotype data does not match the fixed fields. Check the VCF file for inconsistencies.")
  }}

  # 创建一个 data.frame，符合 MRlap 的要求
  df <- data.frame(
    chr = fix_data$CHROM,               # 染色体编号
    pos = fix_data$POS,                 # 位置
    rsid = fix_data$ID,                 # SNP 标识符
    ref = fix_data$REF,                 # 参考等位基因
    alt = fix_data$ALT,                 # 替代等位基因
    beta = as.numeric(gt_parsed[, 1]),  # 效应量 (ES)
    se = as.numeric(gt_parsed[, 2]),    # 标准误差 (SE)
    zscore = as.numeric(gt_parsed[, 1]) / as.numeric(gt_parsed[, 2]),  # 计算 Z 分数
    N = N                               # 样本量 (TotalControls + TotalCases)
  )

  print(head(df))  # 查看生成的 data.frame
  print("Data extraction complete.")

  return(df)
}}

# 定义基础 URL 和文件名
base_url <- "https://gwas.mrcieu.ac.uk/files/"
exposure_file_name <- "{Exposure_id}.vcf.gz"
outcome_file_name <- "{Outcome_id}.vcf.gz"

# 定义暴露和结果数据的样本量
N_exposure <- {N_exposure}  # 替换为你的暴露数据样本量
N_outcome <- {N_outcome}  # 替换为你的结果数据样本量

# 定义 LD 和 HapMap3 文件路径
ld_file <- "./eur_w_ld_chr"  # 替换为你的 LD 文件路径
hm3_file <- "./w_hm3.snplist"  # 替换为你的 HapMap3 文件路径

# 下载暴露数据文件
if (download_vcf(base_url, exposure_file_name)) {{
  # 下载成功或文件已存在，提取暴露数据
  exposure_data <- extract_data_from_vcf(exposure_file_name, N_exposure)
}} else {{
  stop("Failed to download exposure data.")
}}

# 下载结果数据文件
if (download_vcf(base_url, outcome_file_name)) {{
  # 下载成功或文件已存在，提取结果数据
  outcome_data <- extract_data_from_vcf(outcome_file_name, N_outcome)
}} else {{
  stop("Failed to download outcome data.")
}}

# 使用 MRlap 进行分析
result <- MRlap(
  exposure = exposure_data,
  exposure_name = "Exposure",
  outcome = outcome_data,
  outcome_name = "Outcome",
  ld = ld_file,
  hm3 = hm3_file,
  MR_threshold = 5e-6  # 设置 MR 阈值
)

# 查看结果
print(result)

# 保存结果
# write.csv(result, file = "MRlap_results.csv", row.names = FALSE)
result_json <- toJSON(result, pretty=TRUE)
write(result_json, file = ".//{path}//MRlap_results.json")
    """
    r_script_run = r_script.format(Exposure_id=Exposure_id, Outcome_id=Outcome_id, path=path, N_exposure=N_exposure,
                                   N_outcome=N_outcome)
    # print(r_script_run)

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
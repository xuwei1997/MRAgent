import re
import csv
import pandas as pd
from agent_tool import pubmed_crawler, check_keyword_in_opengwas, get_gwas_id, MRtool, get_paper_details, MRtool_MOE, \
    get_synonyms
import os

from template_text import MRorNot_text, synonyms_text, gwas_id_text, pubmed_text, LLM_MR_template, LLM_MR_MOE_template, \
    LLM_conclusion_template, LLM_Introduction_template, pubmed_text_obo

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from PyPDF2 import PdfMerger
import time
import sys
from LLM import llm_chat
import json
import difflib
import math


class MRAgent:
    def __init__(self, mode='O', exposure=None, outcome=None, AI_key=None, model='MR', num=100, bidirectional=False,
                 synonyms=True, introduction=True, LLM_model='gpt-4-turbo-preview', gwas_token=None,
                 opengwas_mode='csv'):
        # 加多一个参数，控制是否从csv中读取gwas列表'csv'或'online'

        self.exposure = exposure
        self.outcome = outcome
        self.AI_key = AI_key
        # 模式选择 OE O E
        self.mode = mode
        # MR模型选择 MR or MR_MOE
        self.model = model
        # 是否双向
        self.bidirectional = bidirectional
        # 是否进行同义词扩充
        self.synonyms = synonyms
        # 是否进行引言
        self.introduction = introduction
        # 若模式为E，则将outcome赋值为exposure，下方步骤中outcome和exposure是等价的
        if self.mode == 'E':
            self.outcome = exposure
        # OE模式已开新类
        # LLM模型选择
        self.LLM_model = LLM_model
        # 定义path
        self.define_path()
        # 从pubmed获取文章数量
        self.num = num
        # gwas_token
        self.gwas_token = gwas_token
        # opengwas模式
        self.opengwas_mode = opengwas_mode
        if self.opengwas_mode == 'csv':
            self.opengwas_csv_init()

    # 定义path并创建文件夹
    def define_path(self):
        if self.mode == 'OE':
            self.path = os.path.join('output', self.exposure + '_' + self.outcome + '_' + self.LLM_model)
        elif self.mode == 'O':
            self.path = os.path.join('output', self.outcome + '_' + self.LLM_model)
        elif self.mode == 'E':
            self.path = os.path.join('output', self.exposure + '_' + self.LLM_model)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    # outcome与什么做了相关性但是没有做因果性
    def step1(self):
        # 1.1 从pubmed获取相关文章
        pubmed_out = pubmed_crawler(self.outcome, self.num, 'most recent', json_str=False)
        print(pubmed_out)
        # # 保存为json文件
        # out_path = os.path.join(self.path, 'pubmed_out.json')
        # with open(out_path, 'w', encoding='utf-8') as f:
        #     f.write(json.dumps(pubmed_out))

        # 1.2 输出文章信息
        # 创建一个空列表，用于存放结果
        out = []
        # 提示词
        template = pubmed_text_obo
        for paper in pubmed_out:
            print(paper)
            # 分别取出index, title, abstract
            index = paper['index']
            title = paper['title']
            abstract = paper['abstract']
            # 1.3 LLM判断
            try:
                t = template.format(Outcome=self.outcome, title=title, abstract=abstract)
                gpt_out = llm_chat(t, self.LLM_model, self.AI_key)
                print('gpt_out:')
                print(gpt_out)
                # 利用正则表达式提取结果中的json list
                if '[' in gpt_out and ']' in gpt_out:
                    gpt_out = gpt_out.split('[')[1].split(']')[0]
                    gpt_out = '[' + gpt_out + ']'
                else:
                    gpt_out = '[{"Outcome": null, "Exposure": null}]'
                print('gpt_out_list:')
                print(gpt_out)

                # 1.4 保存结果
                # 转换为json
                items = json.loads(gpt_out)
                print('items:')
                print(items)
                for item in items:
                    # 不为空
                    if item['Outcome'] is not None:
                        # 将index加入item
                        item['index'] = index
                        # 将 title 加入item
                        item['title'] = title
                        # 将 abstract 加入item
                        item['abstract'] = abstract
                        out.append(item)
                print('\n')
            except Exception as e:
                print('error:', e)
        print(out)

        # 1.4 转换为DataFrame
        df = pd.DataFrame(out, columns=['index', 'Outcome', 'Exposure', 'title', 'abstract'])
        # 增加一列nID oeID
        # df['nID'] = range(0, len(df))
        df['oeID'] = range(0, len(df))
        print(df)

        # 1.5 保存
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')

    # 查看outcome和exposure是否做了MR
    def outcome_exposure_MRorNot(self, outcome, exposure):
        # 休眠1秒
        time.sleep(1)
        # 从pubmed获取相关文章
        pub_text = '({Exposure}[Title/Abstract]) AND ({Outcome}[Title/Abstract]) AND (Mendelian randomization[Title/Abstract])'
        pub_text = pub_text.format(Outcome=outcome, Exposure=exposure)
        print(pub_text)
        pubmed_out = pubmed_crawler(pub_text, 10, 'relevance')
        # 调用GPT
        # GPT
        template = MRorNot_text
        t = template.format(Exposure=exposure, Outcome=outcome, pubmed_out=pubmed_out)

        gpt_out = llm_chat(t, self.LLM_model, self.AI_key)
        print(gpt_out)

        # 若输出中包含"Exposure and Outcome were not subjected to Mendelian randomisation."，则说明没有Mendelian randomisation studies，返回True, 否则返回False
        if "Exposure and Outcome were not subjected to Mendelian randomization." in gpt_out:
            print('No')
            return 'No'
        else:
            print('Yes')
            return 'Yes'

    # 第一次查看是否做了MR
    def step2(self):
        # 2.1 读取step1的结果
        step1_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df = pd.read_csv(step1_path)
        # print(df)

        # 2.2 查看outcome和exposure是否做了MR
        # 提取outcome和exposure，去重
        df_oe = df[['Exposure', 'Outcome']].drop_duplicates()
        # print(df_oe)
        # 查看df_oe是否做了MR
        df_oe['MRorNot'] = df_oe.apply(lambda x: self.outcome_exposure_MRorNot(x['Outcome'], x['Exposure']), axis=1)
        # print(df_oe)
        # 以df为基础，将df_oe的MRorNot合并到df中， 'Outcome'和 'Exposure'  是主键
        df = pd.merge(df, df_oe, on=['Exposure', 'Outcome'], how='left')

        # # 2.3 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')

    #  同义词扩充。提取出所有O和E，新建2表，去重，然后GPT寻找同义词
    def step3(self):
        # 3.1 读取step2的结果
        step2_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df = pd.read_csv(step2_path)
        # 去除MRorNot为Yes的行
        df = df[df['MRorNot'] != 'Yes']
        # 判断df是否为空
        if df.empty:
            print('There is no MR studies')
            sys.exit(0)

        # print(df)

        # 3.2 提取所有的Outcome和Exposure
        outcome_list = df['Outcome'].tolist()
        exposure_list = df['Exposure'].tolist()
        # 合并后去重
        all_list = outcome_list + exposure_list
        all_list = list(set(all_list))
        print(all_list)

        # 3.3 建立表2
        df2 = pd.DataFrame(all_list, columns=['OE'])
        # 增加一列nID sID
        # df2['nID'] = range(0, len(df2))
        df2['sID'] = range(0, len(df2))
        # print(df2)

        # 3.4 从df1中提取OE，寻找同义词，并合并到df2中。要求nID继续递增，但是sID还是原来OE的sID
        if self.synonyms:
            for index, row in df2.iterrows():
                # 3.4.1 提取OE和sID
                OE = row['OE']
                sID = row['sID']
                # 3.4.2 调用UMLS
                python_list = get_synonyms(OE, "d6382a8b-5ca8-493a-98ca-2b02fffcaeb5")

                # 3.4.3 合并到df2中
                df3 = pd.DataFrame(python_list, columns=['OE'])
                # 增加一列sID
                df3['sID'] = sID
                print(df3)
                # 合并到df2中
                df2 = pd.concat([df2, df3], ignore_index=True)
                # print(df2)

        # 3.5 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'Outcome_SNP.csv')
        df2.to_csv(out_path, index=False, encoding='utf-8')

    # 查看OE是否在opengwas中
    def opengwas_csv_init(self):
        # 读取opengwas csv文件
        opengwas_path = 'opengwas.csv'
        df = pd.read_csv(opengwas_path)
        df['trait'] = df['trait'].astype(str)
        self.opengwas_df = df
        self.opengwas_list = df['trait'].tolist()

    def check_keyword_in_opengwas_csv(self, keyword):
        # 从opengwas_df中查找keyword
        # 模糊匹配方式
        # matches = difflib.get_close_matches(keyword, self.opengwas_list, n=10, cutoff=0.4)
        # print(keyword)
        # # print(matches)
        # if len(matches) > 0:
        #     print('True')
        #     return True
        # else:
        #     print('False')
        #     return False

        # 字符串匹配,不区分大小写
        return any(keyword.lower() in s.lower() for s in self.opengwas_list)

    def step4(self):
        # 4.1 读取step3的结果
        step3_path = os.path.join(self.path, 'Outcome_SNP.csv')
        df = pd.read_csv(step3_path)
        # print(df)

        # 4.2 查看OE是否在opengwas中
        if self.opengwas_mode == 'csv':
            df['opengwas'] = df.apply(lambda x: self.check_keyword_in_opengwas_csv(x['OE']), axis=1)
        elif self.opengwas_mode == 'online':
            df['opengwas'] = df.apply(lambda x: check_keyword_in_opengwas(x['OE']), axis=1)
        print(df)

        # 4.3 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'Outcome_SNP.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')

    # 获取OpenGWAS数据库中的GWAS ID
    def get_gwas_id_csv(self, keyword):
        # 根据opengwas_df中的'trait'列，查找与keyword字符串匹配（不区分大小写）的行
        # 查self.opengwas_list找匹配的行，字符串匹配，不区分大小写
        trait_list = []
        for s in self.opengwas_list:
            if keyword.lower() in s.lower():
                trait_list.append(s)
        # trait_list = (s for s in self.opengwas_list if keyword.lower() in s.lower())
        # 如果trait_list长度大于30，则取前30个
        if len(trait_list) > 30:
            trait_list = trait_list[:30]
        # 找到self.opengwas_df中匹配的行
        df = self.opengwas_df[self.opengwas_df['trait'].isin(trait_list)]
        # print(df)

        # 转换为json list
        json_list = []
        # 逐行获取df
        for index, row in df.iterrows():
            # 提取gwas_id
            gwas_id = row['id']
            # 判断year的数据类型为float，则转换为int
            year = row['year']
            if not math.isnan(year):
                year = int(year)

            trait = row['trait']
            consortium = row['consortium']

            samplesize = row['sample_size']
            if not math.isnan(samplesize):
                samplesize = int(samplesize)

            nsnp = row['nsnp']
            if not math.isnan(nsnp):
                nsnp = int(nsnp)

            # # 转换为json 保存了 GWAS ID、Year、Trait、Consortium、Sample size、Number of SNPs
            json_list.append(json.dumps({'gwas_id': gwas_id, 'year': year, 'trait': trait, 'consortium': consortium,
                                         'Sample size': samplesize, 'Number of SNPs': nsnp}))
        print(json_list)

        return json_list

    def step5_get_gwas_id(self, keyword):
        if self.opengwas_mode == 'online':
            json_list = get_gwas_id(keyword)
        elif self.opengwas_mode == 'csv':
            json_list = self.get_gwas_id_csv(keyword)
        # get_gwas_id改为csv模式
        template = gwas_id_text
        t = template.format(keyword=keyword, json_list=json_list)
        gpt_out = llm_chat(t, self.LLM_model, self.AI_key)
        print(gpt_out)
        # 运用正则表达式提取结果中的gwas_id list
        if '[' in gpt_out and ']' in gpt_out:
            gpt_out = gpt_out.split('[')[1].split(']')[0]
            gpt_out = '[' + gpt_out + ']'
        else:
            gpt_out = ['null']

        print(gpt_out)
        # python_list = [item.strip() for item in gpt_out.split(",")]
        # return python_list
        # 取用时再进行处理
        return gpt_out

    # 有了GWAS数据的OE获取所有相关gwas_id
    def step5(self):
        # 5.1 读取step4的结果
        step5_path = os.path.join(self.path, 'Outcome_SNP.csv')
        df = pd.read_csv(step5_path)
        # print(df)

        # 5.2 取出opengwas为True的行
        df_oe = df[df['opengwas'] == True]
        # 按照OE去重
        df_oe = df_oe.drop_duplicates(subset=['OE'])

        # 5.3 获取df_oe所有相关gwas_id
        df_oe['gwas_id'] = df_oe.apply(lambda x: self.step5_get_gwas_id(x['OE']), axis=1)

        # 5.4 将df_oe的gwas_id列按OE合并到df中
        df = pd.merge(df, df_oe[['OE', 'gwas_id']], on='OE', how='left')

        # 5.5 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'Outcome_SNP.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')

    # 求笛卡尔积，获取所有outcome和exposure可能的组合
    def step6(self):
        # 6.1 读取Exposure_and_Outcome.csv
        step1_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df = pd.read_csv(step1_path)
        # 取出MRorNot为No的行
        df_noMR = df[df['MRorNot'] == 'No']
        # print(df_noMR)

        # 6.2 读取Outcome_SNP.csv
        step5_path = os.path.join(self.path, 'Outcome_SNP.csv')
        df_snp = pd.read_csv(step5_path)
        # 取出opengwas为True的行
        # df_snp = df2[df2['opengwas'] == True]

        # 6.3 逐行迭代df_noMR
        for index, row in df_noMR.iterrows():
            # 6.3.1 提取Outcome和Exposure
            Outcome = row['Outcome']
            Exposure = row['Exposure']
            oeID = row['oeID']
            print(Outcome, Exposure)
            # 6.3.2 从df_snp中查找Outcome和Exposure匹配的sID,并分别提取OE为list,并求笛卡尔积
            outcome_id = df_snp[df_snp['OE'] == Outcome]['sID']
            exposure_id = df_snp[df_snp['OE'] == Exposure]['sID']
            # 将提取出的id转换为int
            # print(outcome_id, exposure_id)
            outcome_id = outcome_id.to_numpy()[0]
            exposure_id = exposure_id.to_numpy()[0]
            # print(outcome_id, exposure_id)

            # 6.3.3 按照outcome_id和exposure_id寻找OE，转换为list，求笛卡尔积
            outcome_list = df_snp[df_snp['sID'] == outcome_id]['OE'].to_list()
            exposure_list = df_snp[df_snp['sID'] == exposure_id]['OE'].to_list()
            # print(outcome_list, exposure_list)
            # 求笛卡尔积
            cartesian_product = [(i, j) for i in exposure_list for j in outcome_list]
            # print(cartesian_product)

            # 6.3.4 保存为df_cartesian,合并到df中,oeID为oeID
            df_cartesian = pd.DataFrame(cartesian_product, columns=['Exposure', 'Outcome'])
            df_cartesian['oeID'] = oeID
            # 合并到df中
            df = pd.concat([df, df_cartesian], ignore_index=True)

        # 6.4 查看df中的Outcome和Exposure是否都有snp，匹配df_snp中的OE，查看opengwas列都为True才返回True
        for index, row in df.iterrows():
            # 6.4.1 提取Outcome和Exposure
            Outcome = row['Outcome']
            Exposure = row['Exposure']
            # 6.4.2 查看Outcome和Exposure是否都有snp
            outcome_opengwas = df_snp[df_snp['OE'] == Outcome]['opengwas']
            exposure_opengwas = df_snp[df_snp['OE'] == Exposure]['opengwas']
            # print(outcome_opengwas, exposure_opengwas)
            # 6.4.3 查看opengwas列都为True才返回True
            if outcome_opengwas.all() and exposure_opengwas.all():
                df.loc[index, 'opengwas'] = True
            else:
                df.loc[index, 'opengwas'] = False

        # 6.4 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')

    # Exposure_and_Outcome中，opengwas为TRUE的，并MRorNot这里为Nan的，查看是否做了MR
    def step7(self):
        # 7.1 读取Exposure_and_Outcome.csv
        step1_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df = pd.read_csv(step1_path)
        # 按Outcome和Exposure去重，保留第一次出现的
        df2 = df.drop_duplicates(subset=['Exposure', 'Outcome'])
        print(df2)
        # 取出opengwas为True的行
        df_mr = df2[df2['opengwas'] == True]
        print(df_mr)
        # 取出MRorNot为Nan的行
        df_mr = df_mr[df_mr['MRorNot'].isnull()]
        print(df_mr)
        # df_mr去重
        df_mr = df_mr.drop_duplicates(subset=['Exposure', 'Outcome'])
        print(df_mr)

        # 判断df_mr不为空
        if not df_mr.empty:
            # 7.2 查看outcome和exposure是否做了MR
            df_mr['MRorNot'] = df_mr.apply(lambda x: self.outcome_exposure_MRorNot(x['Outcome'], x['Exposure']), axis=1)

            # 按Outcome和Exposure合并到df中，'Outcome'和 'Exposure'  是主键，替换MRorNot列
            df = pd.merge(df, df_mr[['Exposure', 'Outcome', 'MRorNot']], on=['Exposure', 'Outcome'], how='left',
                          suffixes=('', '_y'))
            # 使用df_mr中的'MRorNot'列替换df中的NaN值
            df['MRorNot'] = df['MRorNot'].combine_first(df['MRorNot_y'])
            # 删除多余的'MRorNot_y'列
            df = df.drop(columns='MRorNot_y')

        # 7.3 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df.to_csv(out_path, index=False, encoding='utf-8')

    # 最终选出Outcome和Exposure进行MR
    def step8(self):
        # 8.1 读取Exposure_and_Outcome.csv
        step1_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df = pd.read_csv(step1_path)

        # 8.2 选出所有Outcome和Exposure都没有进行MR的oeID
        # 创建新的df空表df_mr
        df_mr = pd.DataFrame(columns=df.columns)

        # 提取所有的oeID
        oeID_set = set(df['oeID'].tolist())
        print(oeID_set)
        for i in oeID_set:
            # print(i)
            df_oeID = df[df['oeID'] == i]
            # print(df_oeID)
            # 查看是否有MRorNot为Yes的行，若没有，则选出来放入df_mr
            if not 'Yes' in df_oeID['MRorNot'].tolist():
                # print(df_oeID)
                df_mr = pd.concat([df_mr, df_oeID], ignore_index=True)

        # df_mr去重 去除opengwas为False的行
        # print(df_mr)
        df_mr = df_mr.drop_duplicates(subset=['Exposure', 'Outcome'])
        df_mr = df_mr[df_mr['opengwas'] == True]
        print(df_mr)

        # 8.3 保存为csv
        # 将结果写入CSV文件,utf-8编码
        out_path = os.path.join(self.path, 'mr_run.csv')
        df_mr.to_csv(out_path, index=False, encoding='utf-8')

    # 调用GPT解释MR的结果
    def LLM_MR(self, Exposure, Outcome, Exposure_id, Outcome_id, snp_path):

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
            with open(os.path.join(snp_path, 'LLM_result.txt'), 'w') as file:
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
            with open(os.path.join(snp_path, 'LLM_result.txt'), 'w') as file:
                file.write(gpt_out)

        # # 生成PDF####################################
        # 创建
        doc = SimpleDocTemplate(os.path.join(snp_path, "Report.pdf"), pagesize=letter)
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
        pdfs = [os.path.join(snp_path, "Report.pdf"), os.path.join(snp_path, 'pic.scatter_plot.pdf'),
                os.path.join(snp_path, 'pic.forest.pdf'), os.path.join(snp_path, 'pic.funnel_plot.pdf'),
                os.path.join(snp_path, 'pic.leaveoneout.pdf')]
        # 循环遍历 PDF 文件并将它们添加到合并器
        for pdf in pdfs:
            merger.append(pdf)
        # 写入合并的 PDF 文件
        merger.write(os.path.join(snp_path, "Report.pdf"))
        # 关闭合并器
        merger.close()

        return gpt_out

    def LLM_Introduction(self, Exposure, Outcome, path):
        # GPT写引言####################################
        # pubmed获取Outcome相关文章
        pub_text = '{Outcome}[Title/Abstract]'
        pub_text = pub_text.format(Outcome=Outcome)
        print(pub_text)
        Outcome_pubmed = pubmed_crawler(pub_text, 50, 'relevance')
        # pubmed获取Exposure相关文章
        pub_text = '{Exposure}[Title/Abstract]'
        pub_text = pub_text.format(Exposure=Exposure)
        print(pub_text)
        Exposure_pubmed = pubmed_crawler(pub_text, 50, 'relevance')
        # pubmed获取Exposure和Outcome相关文章
        pub_text = '(({Exposure}[Title/Abstract]) AND ({Outcome}[Title/Abstract]))'
        pub_text = pub_text.format(Exposure=Exposure, Outcome=Outcome)
        print(pub_text)
        Exposure_Outcome_pubmed = pubmed_crawler(pub_text, 50, 'relevance')
        # GPT
        template = LLM_Introduction_template
        t = template.format(Outcome=Outcome, Exposure=Exposure, Outcome_pubmed=Outcome_pubmed,
                            Exposure_pubmed=Exposure_pubmed, Exposure_Outcome_pubmed=Exposure_Outcome_pubmed)
        gpt_out = llm_chat(t, self.LLM_model, self.AI_key)
        # 保存输出结果
        with open(os.path.join(path, 'LLM_Introduction.txt'), 'w', encoding='utf-8') as file:
            file.write(gpt_out)

        ### 获取PubMed数据库中参考文章的详细信息####################################
        # O或E时才获取文章详细信息
        if self.mode == 'O' or self.mode == 'E':
            # 读取CSV文件
            df = pd.read_csv(os.path.join(self.path, 'Exposure_and_Outcome.csv'))
            df = df[(df['Exposure'] == Exposure) & (df['Outcome'] == Outcome)]
            print(df)
            df = df[['title']]
            print(df)
            # 去重
            df = df.drop_duplicates()
            # 转为list
            title_list = df['title'].tolist()
            # 获取文章详细信息
            details_list = []
            for title in title_list:
                # print(title)
                details_list.append(get_paper_details(title))

        # 创建PDF####################################
        doc = SimpleDocTemplate(os.path.join(path, "Introduction.pdf"), pagesize=letter)
        # 设置样式
        styles = getSampleStyleSheet()
        # 创建一个空的 Story 列表来保存文档内容
        story = []
        # 添加标题
        title = Paragraph("A Mendelian randomisation study about " + Exposure + " and " + Outcome, styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))

        styles["BodyText"].fontSize = 12  # 设置字体大小为 14
        styles["BodyText"].alignment = 4  # 设置文字居中 4
        styles["BodyText"].fontName = 'Times-Roman'  # 设置字体

        # 引言
        subtitle = Paragraph("Introduction", styles["Heading2"])
        story.append(subtitle)
        # 引言内容
        gpt_out_list = gpt_out.split('\n')
        for gpt_out_i in gpt_out_list:
            text = Paragraph(gpt_out_i, styles["BodyText"])
            story.append(text)

        if self.mode == 'O' or self.mode == 'E':
            # 参考文献
            subtitle = Paragraph("Important References", styles["Heading2"])
            story.append(subtitle)
            for details in details_list:
                text = Paragraph('Title: ' + details[0], styles["BodyText"])
                story.append(text)
                text = Paragraph('PMID: ' + details[1], styles["BodyText"])
                story.append(text)
                text = Paragraph('DOI: ' + details[2], styles["BodyText"])
                story.append(text)
                text = Paragraph('Journal:' + details[3], styles["BodyText"])
                story.append(text)
                text = Paragraph('Author: ' + details[4], styles["BodyText"])
                story.append(text)
                text = Paragraph('Year: ' + details[5], styles["BodyText"])
                story.append(text)
                text = Paragraph('Abstract: ' + details[6], styles["BodyText"])
                story.append(text)
                story.append(Spacer(1, 12))
        # 构建 PDF
        doc.build(story)

    # 总结各个SNP的结果，生成一个综合结果和PDF
    def LLM_conclusion(self, Exposure, Outcome, path):
        # 调用GPT解释MR的结果
        # 打开文件
        with open(os.path.join(path, self.model + '_LLM_result_all.txt'), 'r') as file:
            LLM_result_all = file.read()
        template = LLM_conclusion_template
        t = template.format(Outcome=Outcome, Exposure=Exposure, MRresult=LLM_result_all)
        gpt_out = llm_chat(t, self.LLM_model, self.AI_key)
        # 保存输出结果
        with open(os.path.join(path, self.model + '_LLM_result_all_conclusion.txt'), 'w', encoding='utf-8') as file:
            file.write(gpt_out)

        # # 生成PDF####################################
        # 创建
        doc = SimpleDocTemplate(os.path.join(path, "Conclusion.pdf"), pagesize=letter)
        # 设置样式
        styles = getSampleStyleSheet()
        # 创建一个空的 Story 列表来保存文档内容
        story = []
        # 添加标题
        title = Paragraph("A Mendelian randomisation study about " + Exposure + " and " + Outcome,
                          styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))

        # 添加Conclusion
        subtitle = Paragraph("Conclusion", styles["Heading2"])
        story.append(subtitle)

        gpt_out_list = gpt_out.split('\n')
        for gpt_out_i in gpt_out_list:
            text = Paragraph(gpt_out_i, styles["BodyText"])
            # story.append(Spacer(1, 12))
            story.append(text)

        # 构建 PDF
        doc.build(story)

    def step9_run_mr_LLM(self, Exposure, Outcome, path, cartesian_product):
        for i, j in cartesian_product:
            # i = str(i)
            # j = str(j)
            try:
                print(i, j)
                if self.model == 'MR':
                    snp_path = os.path.join(path, 'MR_' + i + '_' + j)
                    if not os.path.exists(snp_path):
                        os.makedirs(snp_path)
                    snp_path = snp_path.replace('\\', '//')
                    print(snp_path)
                    MRtool(i, j, snp_path, self.gwas_token)
                    # 调用GPT解释MR的结果
                    self.LLM_MR(Exposure=Exposure, Outcome=Outcome, Exposure_id=i, Outcome_id=j, snp_path=snp_path)
                elif self.model == 'MR_MOE':
                    snp_path = os.path.join(path, 'MR_MOE_' + i + '_' + j)
                    if not os.path.exists(snp_path):
                        os.makedirs(snp_path)
                    snp_path = snp_path.replace('\\', '//')
                    print(snp_path)
                    MRtool_MOE(i, j, snp_path, self.gwas_token)
                    self.LLM_MR(Exposure=Exposure, Outcome=Outcome, Exposure_id=i, Outcome_id=j, snp_path=snp_path)
            except Exception as e:
                print(' step9_run_mr_LLM Error')
                print(e)

        # 总结各个SNP的结果，生成一个综合结果和PDF
        # 读取snp_path下的所有LLM_result.txt
        # 合并为一个文件
        print(Exposure, Outcome, 'conclusion')
        k = 0
        for i, j in cartesian_product:
            try:
                if self.model == 'MR':
                    snp_path = os.path.join(path, 'MR_' + i + '_' + j, 'LLM_result.txt')
                elif self.model == 'MR_MOE':
                    snp_path = os.path.join(path, 'MR_MOE_' + i + '_' + j, 'LLM_result.txt')
                with open(snp_path, 'r') as file:
                    LLM_result = file.read()
                with open(os.path.join(path, self.model + '_LLM_result_all.txt'), 'a') as file:
                    # 写入gwas_id
                    file.write('index: ' + str(k) + '\n')
                    file.write('Exposure_id: ' + i + '\n')
                    file.write('Outcome_id: ' + j + '\n')
                    # 写入文件
                    file.write(LLM_result)
                    file.write('\n\n')
                    k += 1
            except Exception as e:
                print(e)
                print('Error')
        # 生成PDF
        try:
            self.LLM_conclusion(Exposure, Outcome, path)
        except Exception as e:
            print(e)
            print('LLM_conclusion Error')

    # 运行MR
    def step9(self):
        # 9.1 读取mr_run.csv
        global snp_path
        step9_path = os.path.join(self.path, 'mr_run.csv')
        df = pd.read_csv(step9_path)
        # print(df)
        # 读取Outcome_snp.csv
        step5_path = os.path.join(self.path, 'Outcome_SNP.csv')
        df_snp = pd.read_csv(step5_path)
        # 读取Exposure_and_Outcome.csv
        step1_path = os.path.join(self.path, 'Exposure_and_Outcome.csv')
        df_oe = pd.read_csv(step1_path)

        # 9.2 按oeID运行MR
        # 提取所有的oeID
        oeID_set = set(df['oeID'].tolist())
        print(oeID_set)
        for id in oeID_set:
            df_oeID = df[df['oeID'] == id]
            # print(df_oeID)
            # 从df_oe中提取oeID匹配的第一个Outcome和Exposure
            oe_Outcome = df_oe[df_oe['oeID'] == id]['Outcome'].to_list()[0]
            oe_Exposure = df_oe[df_oe['oeID'] == id]['Exposure'].to_list()[0]
            print(oe_Exposure, oe_Outcome)

            # 创建文件夹
            oe_path = os.path.join(self.path, oe_Exposure + '_' + oe_Outcome)
            if not os.path.exists(oe_path):
                os.makedirs(oe_path)

            # 写introduction
            if self.introduction:
                self.LLM_Introduction(Exposure=oe_Exposure, Outcome=oe_Outcome, path=oe_path)

            # 循环oeID 取同义词
            for index, row in df_oeID.iterrows():
                Outcome = row['Outcome']
                Exposure = row['Exposure']
                oeID = row['oeID']
                print(Exposure, Outcome, oeID)
                # 在df_snp中查找Outcome和Exposure匹配的gwad_id
                Outcome_id = df_snp[df_snp['OE'] == Outcome]['gwas_id']
                Exposure_id = df_snp[df_snp['OE'] == Exposure]['gwas_id']
                #
                # # 将提取出的id转换为str
                # Outcome_id = Outcome_id.to_numpy()[0]
                # Exposure_id = Exposure_id.to_numpy()[0]
                # Outcome_id_list = [item.strip() for item in Outcome_id.split(",")]
                # Exposure_id_list = [item.strip() for item in Exposure_id.split(",")]
                # print(Outcome_id_list, Exposure_id_list)

                # 将提取出的python list形式的str转换为list
                Outcome_id = Outcome_id.to_numpy()[0]
                Exposure_id = Exposure_id.to_numpy()[0]
                print(Outcome_id, Exposure_id)
                Outcome_id_list = eval(Outcome_id)
                Exposure_id_list = eval(Exposure_id)
                print(Outcome_id_list, Exposure_id_list)

                # 创建文件夹
                path = os.path.join(oe_path, Exposure + '_' + Outcome)
                if not os.path.exists(path):
                    os.makedirs(path)
                # Outcome_id_list, Exposure_id_list 笛卡尔积
                # TODO 此处应该加入人群种族的判断
                cartesian_product = [(i, j) for i in Exposure_id_list for j in Outcome_id_list]
                print(cartesian_product)
                # 运行MR
                self.step9_run_mr_LLM(Exposure=Exposure, Outcome=Outcome, path=path,
                                      cartesian_product=cartesian_product)

                # 双向
                if self.bidirectional:
                    path = os.path.join(oe_path, Outcome + '_' + Exposure)
                    if not os.path.exists(path):
                        os.makedirs(path)
                    cartesian_product = [(j, i) for i in Exposure_id_list for j in Outcome_id_list]
                    print(cartesian_product)
                    # 运行MR
                    self.step9_run_mr_LLM(Exposure=Outcome, Outcome=Exposure, path=path,
                                          cartesian_product=cartesian_product)

    def run(self, step=None):
        # 判断是否需要进行step1
        if step is None:
            step = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if 1 in step:
            print('#########step1#########')
            self.step1()
        if 2 in step:
            print('#########step2#########')
            self.step2()
        if 3 in step:
            print('#########step3#########')
            self.step3()
        if 4 in step:
            print('#########step4#########')
            self.step4()
        if 5 in step:
            print('#########step5#########')
            self.step5()
        if 6 in step:
            print('#########step6#########')
            self.step6()
        if 7 in step:
            print('#########step7#########')
            self.step7()
        if 8 in step:
            print('#########step8#########')
            self.step8()
        if 9 in step:
            print('#########step9#########')
            self.step9()


if __name__ == '__main__':
    mr_key = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImFwaS1qd3QiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJhcGkub3Blbmd3YXMuaW8iLCJhdWQiOiJhcGkub3Blbmd3YXMuaW8iLCJzdWIiOiI2NzA1MjU3NDRAcXEuY29tIiwiaWF0IjoxNzI0ODE3ODIwLCJleHAiOjE3MjYwMjc0MjB9.LW149mOujc5_Fwk4KxVncGcRudg3yJBarIlPOYEAool_UcDWf8HJESxl6tfrs7kPTU9r2jnxoCTb-w9vEe4LTAvUBFIUNZ5p38sW2S_d4VU1O2fpRmVuo7inlmJeTkFsoIMGI_Mg6559SFczs8nbYCkBQh515K6-NHU4vRMZS8fMVSQRfTwgVJKxStnzZweOC4XBvBwCb8RfUj3ypkRt_cHsn_dNyjkqEkuJ4Af98RmZrR6g6M9F8CcPwuoCumfsT9CJKevBa0aF0-yqerW8HY2_AQYj2J6-TuqvIR2itNlWMFv6FBP99fRSqSfHiY8-tmh0Calq1EZSvwJgmZ8CRQ'  # 提示词中已经加入ID

    # agent = MRAgent(outcome='back pain', AI_key='',
    #                 model='MR', LLM_model='gemini-pro')

    # # mixtral:instruct gemma
    # agent = MRAgent(outcome='back pain', model='MR', LLM_model='llama3:70b', gwas_token=mr_key)
    # agent.run(step=[9])

    # gpt-4-1106-preview gpt-4-turbo-preview gpt-3.5-turbo
    agent = MRAgent(outcome='back pain', model='MR', LLM_model='qwen-max',
                    AI_key='sk-afac4adcb4974723a26f4a05ee586dbc', gwas_token=mr_key, bidirectional=True,
                    introduction=True, num=300)
    agent.run(step=[8])

    # TODO 输出时的暴露结局的顺序需要注意

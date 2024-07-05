# 计算SimCSE相似度
# 最终的最终版本

from simcse import SimCSE
import pandas as pd
import numpy as np


def get_csv(file_path):
    df = pd.read_csv(file_path)

    data = []
    for i in range(1, 31):
        # print(i)
        # 提取index=i的行
        df_i = df.loc[df['index'] == i]
        # 所有的 Exposure, Outcome, 组成一个dict
        # 判断df_i是否为空
        if df_i.empty:
            # data.append({'index': i, 'Exposure and Outcome': []})
            data.append({'index': i, 'Exposure and Outcome': []})
        else:
            data_i = []
            for index, row in df_i.iterrows():
                # data_i.append({'Exposure': row['Exposure'], 'Outcome': row['Outcome']})
                data_i.append([row['Exposure'], row['Outcome']])
            data.append({'index': i, 'Exposure and Outcome': data_i})
    return data


def list_preprocess(data1, data2):
    # 输入的data1, data2是list of dict，每个dict有两个key: 'index', 'Exposure and Outcome'，判断data1data2相同index中元素的'Exposure and Outcome'是否同时为空，若为空则删除
    # 返回的是两个list of dict，每个dict有两个key: 'index', 'Exposure and Outcome'，相同index中元素的'Exposure and Outcome'同时为空的已经删除
    #
    data1_new = []
    data2_new = []
    # 遮罩list
    mask = []

    for i in range(len(data1)):
        if data1[i]['Exposure and Outcome'] != [] and data2[i]['Exposure and Outcome'] != []:
            data1_new.append(str(data1[i]))
            data2_new.append(str(data2[i]))
            mask.append(1)
        elif data1[i]['Exposure and Outcome'] == [] and data2[i]['Exposure and Outcome'] != []:
            data1_new.append('')
            data2_new.append(str(data2[i]['Exposure and Outcome']))
            mask.append(0)
        elif data1[i]['Exposure and Outcome'] != [] and data2[i]['Exposure and Outcome'] == []:
            data1_new.append(str(data1[i]['Exposure and Outcome']))
            data2_new.append('')
            mask.append(0)
    return data1_new, data2_new, mask


def get_sim(csv1, csv2, model):
    hum_dict, llm_dict, mask = list_preprocess(csv1, csv2)
    similarities = model.similarity(hum_dict, llm_dict)
    # print(similarities)
    # similarities 取对角线元素
    similarities_diag = np.diag(similarities)
    # print(similarities_diag)
    # 对角线元素遮罩
    similarities_diag_mask = similarities_diag * mask
    # print(similarities_diag_mask)
    # similarities 取对角线元素求和
    similarities_diag_sum = np.sum(similarities_diag_mask)
    # print(similarities_diag_sum)
    # similarities 取对角线元素求和除以总数
    similarities_diag_sum_mean = similarities_diag_sum / len(similarities_diag)
    print(similarities_diag_sum_mean)
    return similarities_diag_sum_mean


def main(name):
    # humam
    hum_path = 'MRAgentTest1/' + name + '_hum.csv'
    hum_dict_0 = get_csv(hum_path)

    # SimCSE
    # model = SimCSE("princeton-nlp/unsup-simcse-roberta-large")
    model = SimCSE("princeton-nlp/unsup-simcse-bert-large-uncased")

    # claude-3-opus-20240229
    print('claude-3-opus-20240229')
    llm_path_1 = 'MRAgentTest1/' + name + '_claude-3-opus-20240229_Exposure_and_Outcome.csv'
    llm_dict_1 = get_csv(llm_path_1)
    out = get_sim(hum_dict_0, llm_dict_1, model)
    # 保存结果txt文件
    with open('MRAgentTest1/' + name + '_result.txt', 'a') as f:
        f.write('claude-3-opus-20240229: \n')
        f.write(str(out) + '\n')

    # gpt-3.5-turbo
    print('gpt-3.5-turbo')
    llm_path_2 = 'MRAgentTest1/' + name + '_gpt-3.5-turbo_Exposure_and_Outcome.csv'
    llm_dict_2 = get_csv(llm_path_2)
    out = get_sim(hum_dict_0, llm_dict_2, model)
    # 保存结果txt文件
    with open('MRAgentTest1/' + name + '_result.txt', 'a') as f:
        f.write('gpt-3.5-turbo: \n')
        f.write(str(out) + '\n')

    # gpt-4-turbo-preview
    print('gpt-4-turbo-preview')
    llm_path_3 = 'MRAgentTest1/' + name + '_gpt-4-turbo-preview_Exposure_and_Outcome.csv'
    llm_dict_3 = get_csv(llm_path_3)
    out = get_sim(hum_dict_0, llm_dict_3, model)
    # 保存结果txt文件
    with open('MRAgentTest1/' + name + '_result.txt', 'a') as f:
        f.write('gpt-4-turbo-preview: \n')
        f.write(str(out) + '\n')

    # llama3:8b
    print('llama3:8b')
    llm_path_4 = 'MRAgentTest1/' + name + '_llama3_8b_Exposure_and_Outcome.csv'
    llm_dict_4 = get_csv(llm_path_4)
    out = get_sim(hum_dict_0, llm_dict_4, model)
    # 保存结果txt文件
    with open('MRAgentTest1/' + name + '_result.txt', 'a') as f:
        f.write('llama3:8b: \n')
        f.write(str(out) + '\n')

    # llama3:70b
    print('llama3:70b')
    llm_path_5 = 'MRAgentTest1/' + name + '_llama3_70b_Exposure_and_Outcome.csv'
    llm_dict_5 = get_csv(llm_path_5)
    out = get_sim(hum_dict_0, llm_dict_5, model)
    # 保存结果txt文件
    with open('MRAgentTest1/' + name + '_result.txt', 'a') as f:
        f.write('llama3:70b: \n')
        f.write(str(out) + '\n')

    # mixtral_8x22b
    print('mixtral_8x22b')
    llm_path_6 = 'MRAgentTest1/' + name + '_mixtral_8x22b_Exposure_and_Outcome.csv'
    llm_dict_6 = get_csv(llm_path_6)
    out = get_sim(hum_dict_0, llm_dict_6, model)
    # 保存结果txt文件
    with open('MRAgentTest1/' + name + '_result.txt', 'a') as f:
        f.write('mixtral_8x22b: \n')
        f.write(str(out) + '\n')

    # qwen-max-0403
    print('qwen-max-0403')
    llm_path_7 = 'MRAgentTest1/' + name + '_qwen-max-0403_Exposure_and_Outcome.csv'
    llm_dict_7 = get_csv(llm_path_7)
    out = get_sim(hum_dict_0, llm_dict_7, model)
    # 保存结果txt文件
    with open('MRAgentTest1/' + name + '_result.txt', 'a') as f:
        f.write('qwen-max-0403: \n')
        f.write(str(out) + '\n')



if __name__ == '__main__':
    name = 'Lung cancer'
    main(name)

    name = 'Chronic kidney disease'
    main(name)

    name = 'Alzheimer'
    main(name)
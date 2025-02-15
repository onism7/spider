import requests
import pandas as pd

# 人口数量excel文件保存路径
POPULATION_EXCEL_PATH = 'population.xlsx'


def spider_population():
    """
    爬取人口数据
    """
    # 请求参数 sj(时间) zb(指标)
    # 总人口
    dfwds1 = '[{"wdcode": "sj", "valuecode": "LAST70"}, {"wdcode":"zb","valuecode":"A0301"}]'
    # 增长率
    dfwds2 = '[{"wdcode": "sj", "valuecode": "LAST70"}, {"wdcode":"zb","valuecode":"A0302"}]'
    # 人口结构
    dfwds3 = '[{"wdcode": "sj", "valuecode": "LAST70"}, {"wdcode":"zb","valuecode":"A0303"}]'
    url = 'http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=hgnd&rowcode=zb&colcode=sj&wds=[]&dfwds={}'
    population_dict = {
        '2019': [2019, 140005, 71527, 68478, 84843, 55162, 10.48, 7.14, 3.34, 140005, 25061, 97341, 17603, 43.82942439,
                 25.74557483, 18.08384956]}
    response1 = requests.get(url.format(dfwds1))
    get_population_info(population_dict, response1.json())
    response2 = requests.get(url.format(dfwds1))
    get_population_info(population_dict, response2.json())
    response3 = requests.get(url.format(dfwds1))
    get_population_info(population_dict, response3.json())

    save_excel(population_dict)

    return population_dict


def get_population_info(population_dict, json_obj):
    """
    提取人口数量信息
    """
    data_nodes = json_obj['returndata']['datanodes']
    for node in data_nodes:
        # 获取年份
        year = node['code'][-4:]
        # 获取数值
        data = node['data']['data']
        if year in population_dict.keys():
            population_dict[year].append(data)
        else:
            population_dict[year] = [int(year), data]
    return population_dict


def save_excel(population_dict):
    """
    人口数据生成
    """
    # .T 行列转换
    df = pd.DataFrame(population_dict).T[::-1]
    # columns 参数用于指定生成excel中列的顺序
    df.columns = ['年份', '年末总人口(万人)', '男性人口(万人)', '女性人口(万人)', '城镇人口(万人)', '乡村人口(万人)', '人口出生率(‰)', '人口死亡率(‰)',
                  '人口自然增长率(‰)', '年末总人口(万人)', '0-14岁人口(万人)', '15-64岁人口(万人)', '65岁及以上人口(万人)', '总抚养比(%)',
                  '少儿抚养比(%)', '老年抚养比(%)']
    writer = pd.ExcelWriter(POPULATION_EXCEL_PATH)
    df.to_excel(excel_writer=writer, index=False, encoding='utf-8', sheet_name='中国70年人口数据')
    writer.save()
    writer.close()


if __name__ == '__main__':
    result_dict = spider_population()
    # print(result_dict)

import os
import pandas as pd
from tqdm import tqdm
from data_get import get_file_folder, get_data


def test_csv_data(list_msg, list_num, path):
    import csv
    ff = open(path)
    reader = csv.reader(ff)
    header = next(reader)
    list_num.append(len(header))
    print(path)
    list_msg.append(['表头'] + [path] + header)
    row = next(reader)
    list_msg.append(['第一行'] + [path] + row)
    ff.close()
    return list_msg, list_num


def jz_card_to_all(paths, method=1):
    """
    合并文件夹下经侦调取的银行卡，原始数据为易明细信息、账户信息、人员信息的csv文件
    报错:No columns to parse from file 有空文件中无表头
    :return: file :一个字典，包含合并多张表，交易明细信息、账户信息、人员信息等
    """
    # 合并经侦银行卡
    import re
    import collections
    path = paths
    bool_value = True
    deal, staff, account, contact, location, compulsion, task, under = [[], [], [], [], [], [], [], []]  # 定义list
    file = {"交易明细": deal,
            '关联子账户': under,
            "账户信息": account,
            "人员信息": staff,
            '人员联系方式信息': contact,
            '人员住址信息': location,
            '强制措施信息': compulsion,
            '任务信息': task}

    def get_file(file_dir):
        for parent, dirnames, filenames in os.walk(file_dir):
            # 第一个参数是文件夹路径，第二个参数是子文件夹，第三个参数是文件名
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.csv':
                    if re.search('子', filename):  # 匹配关键字
                        continue
                    for m in file.keys():
                        if re.search(m, filename):  # 匹配关键字
                            a = os.path.join(parent, filename)
                            file[m].append(a)

            if bool_value is False:
                dirnames.clear()  # 清除子文件夹列表

    get_file(path)

    for i in file.keys():
        if i == "交易明细" and method == 1:
            if os.path.exists(f'{os.path.dirname(path)}/{os.path.basename(path)}交易流水.csv'):
                os.remove(f'{os.path.dirname(path)}/{os.path.basename(path)}交易流水.csv')
            line_nums = []
            biao_test = []
            for k in tqdm(file[i], desc='数据合并'):
                # csv表头获取
                # r = test_csv_data(biao_test, line_nums, k)
                # biao_test = r[0]
                # line_nums = r[1]
                # 合并csv
                fr = open(k, 'rb').read()
                with open(f'{os.path.dirname(path)}/{os.path.basename(path)}交易流水.csv',
                          'ab') as f:  # 将结果保存为result.csv
                    f.write(fr)
            pd.DataFrame(biao_test).to_excel(f'{os.path.dirname(path)}/{os.path.basename(path)}交易表头.xlsx',
                                             index=False)
            # 获取最多出现的列数
            # counter = collections.Counter(line_nums)
            # most_common_element = counter.most_common(1)
            # most_lenth = most_common_element[0][0]
            # print(f'共{most_lenth}列')
            print('交易明细合并完毕！')
            print('正在读取交易明细')
            df = pd.read_csv(f'{os.path.dirname(path)}/{os.path.basename(path)}交易流水.csv',
                             dtype=str, encoding="GB18030", on_bad_lines='skip', encoding_errors='ignore',
                             )  # usecols=range(0, most_lenth)
            print('读取完毕！')
            df.drop_duplicates(keep='first', inplace=True)
            file[i] = df
        else:
            try:
                total = pd.DataFrame()
                line_nums = []
                biao_test = []
                for j in file[i]:  # 循环字典value里的list
                    if i == '交易明细' and method == 2:
                        r = test_csv_data(biao_test, line_nums, j)
                        biao_test = r[0]
                        b = pd.read_csv(j, encoding="GB18030", dtype=str, on_bad_lines='skip', encoding_errors='ignore')
                    else:
                        b = pd.read_csv(j, encoding="GB18030", dtype=str)
                        if i == '账户信息':
                            b['来源'] = j
                    # encoding = "gbk"使用gbk编码读csv
                    total = pd.concat([b, total], ignore_index=True, copy=False)
                if i == '交易明细':
                    pd.DataFrame(biao_test).to_excel(f'{os.path.dirname(path)}/{os.path.basename(path)}交易表头.xlsx',
                                                     index=False)
                total.drop_duplicates(keep='first', inplace=True)
                file[i] = total  # 将合并表赋值给对应value
            except:
                if i == '交易明细':
                    pd.DataFrame(biao_test).to_excel(f'{os.path.dirname(path)}/{os.path.basename(path)}交易表头.xlsx',
                                                     index=False)

    return file


def xlsx_to_all(paths):
    path = paths
    bool_value = True

    def get_file(file_dir):
        file_name = []
        for parent, dirnames, filenames in os.walk(file_dir):
            # 第一个参数是文件夹路径，第二个参数是子文件夹，第三个参数是文件名
            for filename in filenames:
                if os.path.splitext(filename)[1] == '.xlsx' or os.path.splitext(filename)[1] == '.xls':
                    a = os.path.join(parent, filename)
                    file_name.append(a)

            if bool_value is False:
                dirnames.clear()  # 清除子文件夹列表
        return file_name

    file_s = get_file(path)

    total = pd.DataFrame()
    for k in tqdm(file_s, desc='数据合并'):
        b = pd.read_excel(k, dtype=str)
        total = pd.concat([b, total], ignore_index=True, copy=False)
    total.drop_duplicates(keep='first', inplace=True)
    return total


def sheet_to_all(sheet: str):
    """
    合并文件夹下指定xlsx文件sheet
    :param sheet: 指定sheet名
    :return: data: 合并表
    """
    from data_get import get_file_folder
    path = get_file_folder()
    list1 = os.listdir(path)
    data = pd.DataFrame()
    for i in list1:
        b = pd.read_excel(f"{path}/" + i, sheet_name=sheet, dtype=str)
        b = b.where(b.notnull(), '')
        data = pd.concat([b, data], ignore_index=True)
    return data


def pivot_table_deal_distinct(df_df):
    """
    对透视文件xslx，主对端银行卡都有记录，借贷重复去重
    :return: df:双向去重后数据表
    """
    df = df_df
    df["出"] = pd.to_numeric(df["出"])
    df["进"] = pd.to_numeric(df["进"])
    for row in tqdm(df.index):
        # 筛选主对端相反的数据 若用双循环遍历较慢，因此用相反的账号做两个筛选，最后取交集速度大幅加快
        data = df[(df['主端卡号'] == df.loc[row, '对端账号卡号']) & (df['对端账号卡号'] == df.loc[row, '主端卡号'])]
        if data.empty:
            continue
        else:
            # data.index为列表，包含切片内容的行号与数据类型
            # print(data.index)
            if df.loc[row]['进'] >= df.loc[data.index[0], '出']:
                df.loc[data.index[0], '出'] = None
            else:
                df.loc[row, '进'] = None

            if df.loc[row]['出'] >= df.loc[data.index[0], '进']:
                df.loc[data.index[0], '进'] = None
            else:
                df.loc[row, '出'] = None
    return df


def multiple_sheet_to_all(sheet_name_list: list = None):
    """
    合并多sheet的excel
    :param sheet_name_list:
    :return: dict_all: 存放多表的字典
    """
    if sheet_name_list is None:
        sheet_name_list = ['注册信息', '登录日志', '账户明细']
    path = get_file_folder()
    filename = os.listdir(path)

    dict_all = {}
    for j in sheet_name_list:
        data = pd.DataFrame()
        for i in tqdm(filename):
            b = pd.read_excel(path + "/" + i, sheet_name=j, dtype=str)
            b = b.where(b.notnull(), '')
            data = pd.concat([b, data], ignore_index=True)
        dict_all[j] = data

    return dict_all


def pivot_deduplication_unify_the_direction(df_df):
    # 禁用科学计数法
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    # 将透视表统一成出款方向
    df = df_df

    pt = df.pivot_table(index=['主端卡号', '对端账号卡号'], columns='收付标志', values='交易金额',
                        aggfunc='sum').reset_index()
    # pt_time = df.pivot_table(index=['主端卡号', '对端账号卡号'], columns='收付标志', values='交易金额',
    #                     aggfunc='sum').reset_index()
    jin = pt[pt['进'].notna()][['主端卡号', '对端账号卡号', '进']].rename(
        columns={'进': '出', '主端卡号': '对端账号卡号', '对端账号卡号': '主端卡号'})
    chu = pt[pt['出'].notna()][['主端卡号', '对端账号卡号', '出']]

    new = pd.concat([jin, chu])[['主端卡号', '对端账号卡号', '出']]
    new = new.reset_index().drop('index', axis=1)
    new = new.sort_values(by='出', ascending=False)
    # 删除自身转账
    new = new[new['主端卡号'] != new['对端账号卡号']]
    # 多层数据透视去重
    new['key'] = new['主端卡号'] + new['对端账号卡号']
    new = new.drop_duplicates(subset=['key'], keep='first')
    new = new.drop('key', axis=1)

    return new


def str_of_num(num):
    """
    递归实现，精确为最大单位值 + 小数点后三位
    """

    def strof_size(num, level):
        if level >= 2:
            return num, level
        elif num >= 10000:
            num /= 10000
            level += 1
            return strof_size(num, level)
        else:
            return num, level

    units = ['', '万', '亿']
    num, level = strof_size(num, 0)
    return '{}{}'.format(round(num, 3), units[level])


def luhn_iscard(card_num):
    if type(card_num) == float:
        return False
    for c in card_num:
        if not c.isdigit():
            return False
    s = 0
    card_num_length = len(card_num)
    start_with = ('6', '5', '4', '3', '9')
    if card_num_length >= 10 and card_num.startswith(start_with):
        # if card_num_length >= 10:
        for _ in range(1, card_num_length + 1):
            t = int(card_num[card_num_length - _])
            if _ % 2 == 0:
                t *= 2
                s += t if t < 10 else t % 10 + t // 10
            else:
                s += t
        return s % 10 == 0
    else:
        return False


def deal_str(data):
    data = str(data) + '\t'
    return data


def extract_first_string(x):  # 取最多出现的字符串
    k = list(x)
    most_common_element = max(k, key=k.count)
    return most_common_element


def format_time(x):
    from datetime import datetime
    for f in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y%m%d%H%M%S', '%Y/%m/%d %H:%M:%S']:
        try:
            formatted_date = datetime.strptime(x, f).strftime('%Y-%m-%d %H:%M:%S')
            return formatted_date
        except ValueError:
            pass
    return pd.NaT


def table_splitting(df_df, lie: str):
    """
    按某列拆分文件
    :param df_df: 需要拆分的数据
    :param lie: 拆分列
    """
    df = df_df
    path = get_file_folder()
    card_list = list(set(df[lie]))
    for card in tqdm(card_list):
        if pd.isnull(card):
            continue
        card_data = df[df[lie] == card]
        card_data.to_excel(path + '/' + card + '.xlsx', index=False)


def files_classify():
    """
    以移动清单移动文件，需要准备一个文件清单包含需要移动的文件名和移动后的文件夹。
    也可完成每个文件建一个文件夹
    """
    # 读取清单.xlsx
    checklist = pd.read_excel(get_data(), dtype='str')

    # 读取需要整理的文件夹
    folder_path = get_file_folder()

    # 遍历清单中的每一行
    for index, row in checklist.iterrows():
        # 获取文件名和文件夹名
        file_name = row[0]
        folder_name = row[1]
        # 在需要整理的文件夹下新建文件夹
        new_folder_path = os.path.join(folder_path, folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        # 遍历需要整理的文件夹下的文件
        for file in os.listdir(folder_path):
            # 如果文件名包含清单中的字符串，则移动到相应文件夹
            if file_name in file:
                old_file_path = os.path.join(folder_path, file)
                new_file_path = os.path.join(new_folder_path, file)
                os.rename(old_file_path, new_file_path)


def plot_graph(transactions, path, key='', value='', duke=None):
    import networkx as nx
    import matplotlib.pyplot as plt
    # 设置matplotlib的中文字体，确保中文显示正确
    if duke is None:
        duke = []
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    tmp = transactions.copy()
    chu = tmp[tmp['收付标志'] == '出'][['查询卡号', '交易方户名', '交易时间', '交易金额', '交易对手账卡号', '对手户名']]
    jin = tmp[tmp['收付标志'] == '进'][['查询卡号', '交易方户名', '交易时间', '交易金额', '交易对手账卡号', '对手户名']].rename(
        columns={'查询卡号': '交易对手账卡号', '交易方户名': '对手户名', '交易对手账卡号': '查询卡号', '对手户名': '交易方户名'})
    df = pd.concat([jin, chu]).drop_duplicates(keep='first')

    # 创建一个有向图
    G = nx.DiGraph()
    # 添加节点和边
    count = 0
    special_nodes = []
    for ind, row in df.iterrows():
        # 合并卡号和姓名作为节点标签
        src_name = row['交易方户名']
        dst_name = row['对手户名']
        if row['查询卡号'] in duke:
            src_name = row['交易方户名'] + '\n赌客'
        if row['交易对手账卡号'] in duke:
            dst_name = row['对手户名'] + '\n赌客'

        if row['查询卡号'] == key:
            src_name = row['交易方户名'] + '\n' + value
            count = 1
        if row['交易对手账卡号'] == key:
            dst_name = row['对手户名'] + '\n' + value
            count = 2

        src_label = f"{row['查询卡号']}\n{src_name}"
        dst_label = f"{row['交易对手账卡号']}\n{dst_name}"

        if count == 1:
            special_nodes.append(src_label)

        if count == 2:
            special_nodes.append(dst_label)
        count = 0

        # 如果节点不存在，则添加节点
        if src_label not in G:
            G.add_node(src_label)
        if dst_label not in G:
            G.add_node(dst_label)

        # 添加边，设置'weight'为交易金额，'time'为交易时间
        # 同时创建一个标签，包含时间和金额
        label = f"{row['交易时间']}\n¥{row['交易金额']}"
        G.add_edge(src_label, dst_label, weight=float(row['交易金额']), time=row['交易时间'], label=label)

    # 绘制图
    plt.figure(figsize=(30, 30))

    pos = nx.kamada_kawai_layout(G)
    # pos = nx.spring_layout(G, scale=2)  # 为图形设置布局
    pos = nx.random_layout(G)

    # 特殊处理指定节点
    special_node_color = 'green'
    default_node_color = 'skyblue'
    default_font_weight = 'normal'

    # 使用nx.draw_networkx一次性绘制节点、边和边标签
    nx.draw_networkx(G, pos, arrows=True, node_color=default_node_color, edge_color='k', font_weight=default_font_weight, node_size=5000)

    # 对特殊节点进行处理
    for node in special_nodes:
        nx.draw_networkx_nodes(G, pos, nodelist=[node], node_color=special_node_color, node_size=5000)
        # nx.draw_networkx_labels(G, pos, labels={node: node}, font_weight=special_nodes[node]['font_weight'])

    # 绘制边的标签（时间和金额）
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')
    plt.savefig(f"{path}/{key}.png")
    # plt.show()

def removeDup(mylist:list) -> list:
    if len(mylist) < 1:
        raise Exception("形参异常")
    result = [mylist[0]]
    for i in mylist:
        if i not in result:
            result.append(i)
    return result

def calculate_hash(row):
    import hashlib
    new_row = row[['主端卡号', '对端卡号', '收付标志', '交易金额', '交易余额', '交易时间', '交易结果']]
    row_str = ','.join(map(str, new_row))
    return hashlib.md5(row_str.encode('utf-8')).hexdigest()

def show(df):
    return df.head(10).style.set_table_attributes('style="width:100%; white-space: nowrap;"')
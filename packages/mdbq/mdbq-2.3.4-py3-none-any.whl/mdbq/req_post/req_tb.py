# -*- coding: UTF-8 –*-
import os
import time
import datetime
import pandas as pd
import warnings
import requests
from mdbq.other import ua_sj
from mdbq.config import get_myconf
from mdbq.mysql import mysql
import json
import socket
import platform
import random

warnings.filterwarnings('ignore')


class RequestData:
    def __init__(self):
        self.date = datetime.date.today().strftime('%Y%m%d')
        self.url = None
        self.headers = None
        self.cookies = None
        self.datas = []
        self.path = None
        self.filename = None
        self.is_json_file = False

    def request_data(self, date, url, headers, cookies, path, filename):
        """ 活动预售页面 流量来源 """
        # date = datetime.date.today().strftime('%Y%m%d')
        # url = (f'https://sycm.taobao.com/datawar/v6/activity/detail/guide/chl/presale/online/v4.json?'
        #        f'dateRange={date}%7C{date}'
        #        f'&dateType=today'
        #        f'&pageSize=10'
        #        f'&page=1'
        #        f'&order=desc'
        #        f'&orderBy=frontPreheatUv'  # 必传参数
        #        f'&activityId=94040472'  # 关键，必传参数
        #        # f'&activityStatus=3'
        #        # f'&device=2'
        #        # f'&indexCode=frontPreheatUv%2CfrontPayByrCnt%2CfrontPayRate'
        #        # f'&_=1729079731795'
        #        # f'&token=7e94ba030'
        #        )
        # headers = {
        #     "referer": "https://dmp.taobao.com/index_new.html",
        #     'User-Agent': ua_sj.get_ua(),
        # }
        # cookies = {
        #     'session': 't=c198527347800dafa75165f084784668; thw=cn; xlly_s=1; _tb_token_=rPWSGun4nUou9aKxviPg; _samesite_flag_=true; 3PcFlag=1729054801593; cookie2=130befc055eed2df29935197bd2b514b; sgcookie=E100aLOltfWHqLLH1qtyH3it%2BLrGH2v3MAnIBdSfu7xwjEpSyh101lblDVcj3zGpAOLv%2FXcrVNbT%2FN%2BI8KZeCoE4HBzHQk0ANtSqjOG5gIzdKamfirBxGWJyVEccitvvDZhK; unb=2210244713719; sn=%E4%B8%87%E9%87%8C%E9%A9%AC%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%8E%A8%E5%B9%BF; uc1=cookie21=W5iHLLyFfoaZ&cookie14=UoYcCoAfJ7pSQA%3D%3D; csg=1e2bdb8a; _cc_=Vq8l%2BKCLiw%3D%3D; cancelledSubSites=empty; skt=f813f8478f7318f8; v=0; cna=8+iAHxeojXcCAXjsc5Mt+BAV; mtop_partitioned_detect=1; _m_h5_tk=88c56a84a93c1199f8abe086a132c7eb_1729068459392; _m_h5_tk_enc=4b0ed8316f46edae303547d3863982a4; XSRF-TOKEN=4ef3d151-14c4-445a-9249-595e9a24df75; JSESSIONID=9EE8C8DCF6162DCA2FE0187C29BF0B8A; tfstk=gyaEdSAx842sxMbj1f3rgEWrJ50LN2XbxzMSZ7VoOvDheWNubSerd_IKRlkzIRk3O76JzQqgCk9QZzGuzR3n2kMSdYuzw-51hZ_b9W3--t6flZ3LgJuxZBYHFAYiG40ZtLV_9W3J6C9lclVpUV2YVJ0uEVmiwj0kr00l_ccjZ4YnqexMIAhor4YoqVDiwjvkr80l_5DttHciSWVk7jihGd0FW1QAcqH0tA8kuIhKxg2JVH-emXiZncbekEC-TDk0tAWAnqwo4JoU5wJxTlV4BXyRke3n4kqm-zWV8VVYfJcaEt-rIozLzmaF3nH3JYeq-lWM840Kg7obf_xqCuVT7czFcQhTR74KcqbvKYZ_gzlzyTQa3W2Umm4HLgz6efAQOzEeE3on6fkf_1ySvoccWpB-m3K-jqhZh6GB23nnhfkf_1-J2cDo_x1IO; isg=BLm5J8RI-qdgDKdAgF_DSgcFyCOTxq14BgKdB9vjgONeYsD0IReUSUT05GaUWkWw'}

        self.date = date
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.path = path
        self.filename = filename
        result = requests.get(
            self.url,
            headers=self.headers,
            cookies=self.cookies,
        )
        m_data = json.loads(result.text)
        update_time = m_data['data']['updateTime']
        # pt_data = data['data']['data'][0]  # 平台流量
        # gg_data = data['data']['data'][1]  # 广告流量
        for all_data in m_data['data']['data']:
            self.datas.append({
                'frontPayByrCnt': all_data['frontPayByrCnt']['value'],
                '一级标识id': all_data['pageId']['value'],
                '二级标识id': '',
                '三级标识id': '',
                '一级来源': all_data['pageName']['value'],
                '二级来源': '',
                '三级来源': '',
                '活动商品访客数（定金期）': all_data['frontPreheatUv']['value'],
                '定金支付买家数': all_data['frontPayByrCnt']['value'],
                '定金支付转化率': all_data['frontPayRate']['value'],
                '日期': all_data['statDateStr']['value'],
                '更新时间': update_time,
                '促销活动': '2024双11预售',
            })
            if 'children' not in all_data.keys():  # 这一句有点多余，因为一级来源必定细分有二级来源
                continue
            for children_data in all_data['children']:
                one_source_id = children_data['pPageId']['value']
                one_source_name = children_data['pPageName']['value']
                self.datas.append(
                    {
                        'frontPayByrCnt': children_data['frontPayByrCnt']['value'],
                        '一级标识id': children_data['pPageId']['value'],
                        '二级标识id': children_data['pageId']['value'],
                        '三级标识id': '',
                        '一级来源': children_data['pPageName']['value'],
                        '二级来源': children_data['pageName']['value'],
                        '三级来源': '',
                        '活动商品访客数（定金期）': children_data['frontPreheatUv']['value'],
                        '定金支付买家数': children_data['frontPayByrCnt']['value'],
                        '定金支付转化率': children_data['frontPayRate']['value'],
                        '日期': children_data['statDateStr']['value'],
                        '更新时间': update_time,
                        '促销活动': '2024双11预售',
                    }
                )
                # print(children_data['children'])
                # print(children_data)
                if 'children' not in children_data.keys():  # 部分二级来源没有细分的三级来源，因为需要跳过 children 字段
                    continue
                for children_children_data in children_data['children']:
                    # print(children_children_data)
                    # print(one_source_name)
                    self.datas.append(
                        {
                            'frontPayByrCnt': children_children_data['frontPayByrCnt']['value'],
                            '一级标识id': one_source_id,
                            '二级标识id': children_children_data['pPageId']['value'],
                            '三级标识id': children_children_data['pageId']['value'],
                            '一级来源': one_source_name,
                            '二级来源': children_children_data['pPageName']['value'],
                            '三级来源': children_children_data['pageName']['value'],
                            '活动商品访客数（定金期）': children_children_data['frontPreheatUv']['value'],
                            '定金支付买家数': children_children_data['frontPayByrCnt']['value'],
                            '定金支付转化率': children_children_data['frontPayRate']['value'],
                            '日期': children_children_data['statDateStr']['value'],
                            '更新时间': update_time,
                            '促销活动': '2024双11预售',
                        }
                    )
        for item in self.datas:
            if item['日期'] != '':
                item.update({'日期': f'{item['日期'][0:4]}-{item['日期'][4:6]}-{item['日期'][6:8]}'})
        if self.is_json_file:
            with open(os.path.join(self.path, f'{self.filename}.json'), 'w') as f:
                json.dump(self.datas, f, ensure_ascii=False, sort_keys=True, indent=4)

    def hd_sp(self, date, url, headers, cookies, path, filename, pages=5):
        """ 活动预售页面 分商品效果 """

        self.date = date
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.path = path
        self.filename = filename
        for page in range(1, pages + 1):
            self.url = f'{self.url}&page={page}'
            result = requests.get(
                self.url,
                headers=self.headers,
                cookies=self.cookies,
            )
            m_data = json.loads(result.text)
            # print(m_data)
            # with open(os.path.join(self.path, f'{self.filename}.json'), 'w') as f:
            #     json.dump(m_data, f, ensure_ascii=False, sort_keys=True, indent=4)
            update_time = m_data['data']['updateTime']
            time_stamp = m_data['data']['timestamp']
            # pt_data = data['data']['data'][0]  # 平台流量
            # gg_data = data['data']['data'][1]  # 广告流量
            for all_data in m_data['data']['data']['data']:
                self.datas.append({
                    'activityItemDepUv': all_data['activityItemDepUv']['value'],
                    '商品链接': all_data['item']['detailUrl'],
                    '商品id': all_data['item']['itemId'],
                    '商品图片': all_data['item']['pictUrl'],
                    'startDate': all_data['item']['startDate'],
                    '商品标题': all_data['item']['title'],
                    '预售订单金额': all_data['presaleOrdAmt']['value'],
                    '定金支付件数': all_data['presalePayItemCnt']['value'],
                    '预售访客人数': all_data['presaleUv']['value'],
                    '定金支付金额': all_data['sumPayDepositAmt']['value'],
                    '定金支付买家数': all_data['sumPayDepositByrCnt']['value'],
                    '支付转化率': all_data['uvPayRate']['value'],
                    '日期': date,
                    '时间戳': time_stamp,
                    '更新时间': update_time,
                    '促销活动': '2024双11预售',
                    '类型': '分商品效果',
                })
            time.sleep(random.randint(5, 10))
        for item in self.datas:
            if item['日期'] != '':
                item.update({'日期': f'{item['日期'][0:4]}-{item['日期'][4:6]}-{item['日期'][6:8]}'})
        if self.is_json_file:
            with open(os.path.join(self.path, f'{self.filename}.json'), 'w') as f:
                json.dump(self.datas, f, ensure_ascii=False, sort_keys=True, indent=4)

    def request_jd(self, date, url, headers, cookies, path, filename):
        """ 京东 """
        self.date = date
        self.url = url
        self.headers = headers
        self.cookies = cookies
        self.path = path
        self.filename = filename
        result = requests.post(
            url,
            headers=headers,
            cookies=cookies,
        )
        print(result.text)


def tb_data(service_databases=[], db_name=None, table_name=None):
    """ 2024双11预售实时流量分析 """
    date = datetime.date.today().strftime('%Y%m%d')
    url = (f'https://sycm.taobao.com/datawar/v6/activity/detail/guide/chl/presale/online/v4.json?'
           f'dateRange={date}%7C{date}'
           f'&dateType=today'
           f'&pageSize=10'
           f'&page=1'
           f'&order=desc'
           f'&orderBy=frontPreheatUv'  # 必传参数
           f'&activityId=94040472'  # 关键，必传参数
           # f'&activityStatus=3'
           # f'&device=2'
           # f'&indexCode=frontPreheatUv%2CfrontPayByrCnt%2CfrontPayRate'
           # f'&_=1729079731795'
           # f'&token=7e94ba030'
           )
    headers = {
        "referer": "https://dmp.taobao.com/index_new.html",
        'User-Agent': ua_sj.get_ua(),
    }
    cookies = {
        'session': 't=c198527347800dafa75165f084784668; thw=cn; xlly_s=1; _tb_token_=rPWSGun4nUou9aKxviPg; _samesite_flag_=true; 3PcFlag=1729054801593; cookie2=130befc055eed2df29935197bd2b514b; sgcookie=E100aLOltfWHqLLH1qtyH3it%2BLrGH2v3MAnIBdSfu7xwjEpSyh101lblDVcj3zGpAOLv%2FXcrVNbT%2FN%2BI8KZeCoE4HBzHQk0ANtSqjOG5gIzdKamfirBxGWJyVEccitvvDZhK; unb=2210244713719; sn=%E4%B8%87%E9%87%8C%E9%A9%AC%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%8E%A8%E5%B9%BF; uc1=cookie21=W5iHLLyFfoaZ&cookie14=UoYcCoAfJ7pSQA%3D%3D; csg=1e2bdb8a; _cc_=Vq8l%2BKCLiw%3D%3D; cancelledSubSites=empty; skt=f813f8478f7318f8; v=0; cna=8+iAHxeojXcCAXjsc5Mt+BAV; mtop_partitioned_detect=1; _m_h5_tk=88c56a84a93c1199f8abe086a132c7eb_1729068459392; _m_h5_tk_enc=4b0ed8316f46edae303547d3863982a4; XSRF-TOKEN=4ef3d151-14c4-445a-9249-595e9a24df75; JSESSIONID=9EE8C8DCF6162DCA2FE0187C29BF0B8A; tfstk=gyaEdSAx842sxMbj1f3rgEWrJ50LN2XbxzMSZ7VoOvDheWNubSerd_IKRlkzIRk3O76JzQqgCk9QZzGuzR3n2kMSdYuzw-51hZ_b9W3--t6flZ3LgJuxZBYHFAYiG40ZtLV_9W3J6C9lclVpUV2YVJ0uEVmiwj0kr00l_ccjZ4YnqexMIAhor4YoqVDiwjvkr80l_5DttHciSWVk7jihGd0FW1QAcqH0tA8kuIhKxg2JVH-emXiZncbekEC-TDk0tAWAnqwo4JoU5wJxTlV4BXyRke3n4kqm-zWV8VVYfJcaEt-rIozLzmaF3nH3JYeq-lWM840Kg7obf_xqCuVT7czFcQhTR74KcqbvKYZ_gzlzyTQa3W2Umm4HLgz6efAQOzEeE3on6fkf_1ySvoccWpB-m3K-jqhZh6GB23nnhfkf_1-J2cDo_x1IO; isg=BLm5J8RI-qdgDKdAgF_DSgcFyCOTxq14BgKdB9vjgONeYsD0IReUSUT05GaUWkWw'}
    path = '/Users/xigua/Downloads'
    filename = 'test'
    r = RequestData()
    r.is_json_file = False
    r.request_data(
        date=date,
        url=url,
        headers=headers,
        cookies=cookies,
        path=path,
        filename=filename,
    )
    # print(r.datas)
    df = pd.DataFrame(r.datas)
    # df.to_csv(os.path.join(path, 'test.csv'), index=False, header=True, encoding='utf-8_sig')

    if not service_databases:
        return
    if not db_name or not table_name:
        print(f'尚未指定 db_name/table_name 参数')
        return
    for dt in service_databases:
        for service_name, database in dt.items():
            username, password, host, port = get_myconf.select_config_values(
                target_service=service_name,
                database=database,
            )
            m = mysql.MysqlUpload(
                username=username,
                password=password,
                host=host,
                port=port,
            )
            m.df_to_mysql(
                df=df,
                db_name=db_name,
                table_name=table_name,
                move_insert=False,  # 先删除，再插入
                df_sql=False,  # 值为 True 时使用 df.to_sql 函数上传整个表, 不会排重
                drop_duplicates=False,  # 值为 True 时检查重复数据再插入，反之直接上传，会比较慢
                filename=None,  # 用来追踪处理进度
                service_database=dt,  # 字典
            )


def company_run():
    if platform.system() == 'Windows' and socket.gethostname() == 'company':
        while True:
            tb_data(service_databases=[{'company': 'mysql'}], db_name='生意参谋2',
                    table_name='2024双11预售实时流量分析')
            time.sleep(random.randint(1500, 2000))


def hd_sp_data(service_databases=[], db_name=None, table_name=None, pages=5):
    """ 2024双11预售 分商品效果 """
    date = datetime.date.today().strftime('%Y%m%d')
    url = (
        f'https://sycm.taobao.com/datawar/v7/presaleActivity/itemCoreIndex/getItemListLive.json?'
        f'activityId=94040472'
        f'&itemType=0'  # 必传， 查看全部商品 0， 活动商品 1 ， 跨店满减商品 2 ，官方立减 3（无数据）
        f'&device=1'
        f'&dateRange={date}%7C{date}'
        f'&dateType=today'
        f'&pageSize=10'  # 必传
        # f'&page=1'   # 必传
        # f'&order=desc'
        # f'&orderBy=presaleOrdAmt'
        # f'&indexCode=presaleOrdAmt%2CsumPayDepositByrCnt%2CpresalePayItemCnt'
        # f'&_=1729133575797'
           )
    headers = {
        # "referer": "https://dmp.taobao.com/index_new.html",
        'User-Agent': ua_sj.get_ua(),
    }
    cookies = {
        'session': 't=c198527347800dafa75165f084784668; thw=cn; xlly_s=1; _tb_token_=rPWSGun4nUou9aKxviPg; _samesite_flag_=true; 3PcFlag=1729054801593; cookie2=130befc055eed2df29935197bd2b514b; sgcookie=E100aLOltfWHqLLH1qtyH3it%2BLrGH2v3MAnIBdSfu7xwjEpSyh101lblDVcj3zGpAOLv%2FXcrVNbT%2FN%2BI8KZeCoE4HBzHQk0ANtSqjOG5gIzdKamfirBxGWJyVEccitvvDZhK; unb=2210244713719; sn=%E4%B8%87%E9%87%8C%E9%A9%AC%E5%AE%98%E6%96%B9%E6%97%97%E8%88%B0%E5%BA%97%3A%E6%8E%A8%E5%B9%BF; uc1=cookie21=W5iHLLyFfoaZ&cookie14=UoYcCoAfJ7pSQA%3D%3D; csg=1e2bdb8a; _cc_=Vq8l%2BKCLiw%3D%3D; cancelledSubSites=empty; skt=f813f8478f7318f8; v=0; cna=8+iAHxeojXcCAXjsc5Mt+BAV; mtop_partitioned_detect=1; _m_h5_tk=88c56a84a93c1199f8abe086a132c7eb_1729068459392; _m_h5_tk_enc=4b0ed8316f46edae303547d3863982a4; XSRF-TOKEN=4ef3d151-14c4-445a-9249-595e9a24df75; JSESSIONID=9EE8C8DCF6162DCA2FE0187C29BF0B8A; tfstk=gyaEdSAx842sxMbj1f3rgEWrJ50LN2XbxzMSZ7VoOvDheWNubSerd_IKRlkzIRk3O76JzQqgCk9QZzGuzR3n2kMSdYuzw-51hZ_b9W3--t6flZ3LgJuxZBYHFAYiG40ZtLV_9W3J6C9lclVpUV2YVJ0uEVmiwj0kr00l_ccjZ4YnqexMIAhor4YoqVDiwjvkr80l_5DttHciSWVk7jihGd0FW1QAcqH0tA8kuIhKxg2JVH-emXiZncbekEC-TDk0tAWAnqwo4JoU5wJxTlV4BXyRke3n4kqm-zWV8VVYfJcaEt-rIozLzmaF3nH3JYeq-lWM840Kg7obf_xqCuVT7czFcQhTR74KcqbvKYZ_gzlzyTQa3W2Umm4HLgz6efAQOzEeE3on6fkf_1ySvoccWpB-m3K-jqhZh6GB23nnhfkf_1-J2cDo_x1IO; isg=BLm5J8RI-qdgDKdAgF_DSgcFyCOTxq14BgKdB9vjgONeYsD0IReUSUT05GaUWkWw'}
    path = '/Users/xigua/Downloads'
    filename = 'test'
    r = RequestData()
    r.is_json_file = False
    r.hd_sp(
        date=date,
        url=url,
        headers=headers,
        cookies=cookies,
        path=path,
        filename=filename,
        pages = pages,
    )
    # print(r.datas)
    df = pd.DataFrame(r.datas)
    df.to_csv(os.path.join(path, 'test.csv'), index=False, header=True, encoding='utf-8_sig')


if __name__ == '__main__':
    company_run()
    # tb_data(service_databases=[{'company': 'mysql'}], db_name='生意参谋2', table_name='2024双11预售实时流量分析')
    hd_sp_data(
        service_databases=[{'company': 'mysql'}],
        # db_name='生意参谋2',
        # table_name='2024双11预售实时流量分析',
    )

"""
    macro china
"""
import sys
import json
import akshare as ak
import gopup as gp

import datetime


class MacroChinaService(object):
    #lpr信息
    @staticmethod
    def lpr(samples):
        macro_china_lpr_df = ak.macro_china_lpr()

        #删除NaN所在行
        macro_china_lpr_df = macro_china_lpr_df.dropna()

        list_data = []

        if samples < macro_china_lpr_df.size:
               macro_china_lpr_df = macro_china_lpr_df.tail(samples)

        for row in macro_china_lpr_df.itertuples():
            data = {'trade_date':str(getattr(row, 'TRADE_DATE')),
                'lpr1y': getattr(row, 'LPR1Y'),
                'lpr5y':getattr(row, 'LPR5Y'),
                'rate1':getattr(row, 'RATE_1'),
                'rate2':getattr(row, 'RATE_2')}

            list_data.append(data)

        return list_data

    #同业拆借利率（上海）
    @staticmethod
    def shibor():
        macro_china_shibor_all = ak.macro_china_shibor_all()

        #去除第一行
        macro_china_shibor_all = macro_china_shibor_all.tail(macro_china_shibor_all.shape[0]-1)

        list_data = []
        for index, row in macro_china_shibor_all.iterrows():
            tmp_dict = {
                'date': index,
                'O/N_定价' : getattr(row, 'O/N_定价'),
                'O/N_涨跌幅' : getattr(row, 'O/N_涨跌幅'),
                '1W_定价' : getattr(row, '1W_定价'),
                '1W_涨跌幅' : getattr(row, '1W_涨跌幅'),
                '2W_定价' : getattr(row, '2W_定价'),
                '2W_涨跌幅' : getattr(row, '2W_涨跌幅'),
                '1M_定价' : getattr(row, '1M_定价'),
                '1M_涨跌幅' : getattr(row, '1M_涨跌幅'),
                '3M_定价' : getattr(row, '3M_定价'),
                '3M_涨跌幅' : getattr(row, '3M_涨跌幅'),
                '6M_定价' : getattr(row, '6M_定价'),
                '6M_涨跌幅' : getattr(row, '6M_涨跌幅'),
                '9M_定价' : getattr(row, '9M_定价'),
                '9M_涨跌幅' : getattr(row, '9M_涨跌幅'),
                '1Y_定价' : getattr(row, '1Y_定价'),
                '1Y_涨跌幅' : getattr(row, '1Y_涨跌幅')}
            list_data.append(tmp_dict)

        return list_data

    #同业拆借利率（上海）
    @staticmethod
    def hk_market_info():
        macro_china_hk_market_info = ak.macro_china_hk_market_info()

        #去除第一行
        macro_china_hk_market_info = macro_china_hk_market_info.tail(macro_china_hk_market_info.shape[0]-1)

        list_data = []
        for index, row in macro_china_hk_market_info.iterrows():
            tmp_dict = {
                'date': index,
                'ON_定价' : getattr(row, 'ON_定价'),
                'ON_涨跌幅' : getattr(row, 'ON_涨跌幅'),
                '1W_定价' : getattr(row, '1W_定价'),
                '1W_涨跌幅' : getattr(row, '1W_涨跌幅'),
                '2W_定价' : getattr(row, '2W_定价'),
                '2W_涨跌幅' : getattr(row, '2W_涨跌幅'),
                '1M_定价' : getattr(row, '1M_定价'),
                '1M_涨跌幅' : getattr(row, '2M_涨跌幅'),
                '2M_定价': getattr(row, '2M_定价'),
                '2M_涨跌幅': getattr(row, '1M_涨跌幅'),
                '3M_定价' : getattr(row, '3M_定价'),
                '3M_涨跌幅' : getattr(row, '3M_涨跌幅'),
                '6M_定价' : getattr(row, '6M_定价'),
                '6M_涨跌幅' : getattr(row, '6M_涨跌幅'),
                '1Y_定价' : getattr(row, '1Y_定价'),
                '1Y_涨跌幅' : getattr(row, '1Y_涨跌幅')}
            list_data.append(tmp_dict)

        return list_data

    # 季度GDP
    @staticmethod
    def gdp():
        macro_china_dgp = gp.get_gdp_quarter()
        list_data = []
        for index, row in macro_china_dgp.iterrows():
            tmp_dict = {
                '季度' : str(getattr(row, '季度')),
                '国内生产总值绝对值(亿元)': getattr(row, '国内生产总值 绝对值(亿元)'),
                '国内生产总值同比增长': getattr(row, '国内生产总值 同比增长'),
                '第一产业绝对值(亿元）': getattr(row, '第一产业 绝对值(亿元)'),
                '第一产业同比增长': getattr(row, '第一产业 同比增长'),
                '第二产业绝对值(亿元)': getattr(row, '第二产业 绝对值(亿元)'),
                '第二产业同比增长': getattr(row, '第二产业 同比增长'),
                '第三产业绝对值(亿元)': getattr(row, '第三产业 绝对值(亿元)'),
                '第三产业同比增长': getattr(row, '第三产业 同比增长'),
            }
            list_data.append(tmp_dict)

        return  list_data

    # 年度GDP
    @staticmethod
    def gdp_yearly():
        macro_china_dgp = gp.get_gdp_quarter()

        totla_gdp = {} #年总gdp
        dycy_gdp = {}  #年第一产业总gdp
        decy_gdp = {}  #年第二产业总gdp
        dscy_gdp = {}  #年第三产业总gdp

        list_data = []
        for index, row in macro_china_dgp.iterrows():
            date_year = datetime.datetime.strptime(str(getattr(row, '季度')), '%Y-%m-%d').date()
            current_year = date_year.year

            if not bool(totla_gdp.get(current_year)):
                totla_gdp[current_year] = float(getattr(row, '国内生产总值 绝对值(亿元)'))
                dycy_gdp[current_year] = float(getattr(row, '第一产业 绝对值(亿元)'))
                decy_gdp[current_year] = float(getattr(row, '第二产业 绝对值(亿元)'))
                dscy_gdp[current_year] = float(getattr(row, '第三产业 绝对值(亿元)'))

        for key in totla_gdp:
            tmp_dict = {
                'date' : key,
                '总GDP' :  totla_gdp[key],
                '第一产业总GDP': dycy_gdp[key],
                '第二产业总GDP': decy_gdp[key],
                '第三产业总GDP': dscy_gdp[key],
            }
            list_data.append(tmp_dict)

        return list_data

        # 年度GDP

    @staticmethod
    def pmi():
        macro_china_pmi = ak.macro_china_pmi()

        list_data = []
        for index, row in macro_china_pmi.iterrows():
            tmp_dict = {
                '月份': getattr(row, '月份'),
                '制造业-指数': getattr(row, '制造业-指数'),
                '制造业-同比增长': getattr(row, '制造业-同比增长'),
                '非制造业-指数': getattr(row, '非制造业-指数'),
                '非制造业-同比增长': getattr(row, '非制造业-同比增长'),
            }
            list_data.append(tmp_dict)

        return list_data

    @staticmethod
    def ppi():
        macro_china_ppi = ak.macro_china_ppi()

        list_data = []
        for index, row in macro_china_ppi.iterrows():
            tmp_dict = {
                '月份': getattr(row, '月份'),
                '当月': getattr(row, '当月'),
                '当月同比增长': getattr(row, '当月同比增长'),
                '累计': getattr(row, '累计'),
            }
            list_data.append(tmp_dict)

        return list_data

    @staticmethod
    def ppi():
        macro_china_ppi = ak.macro_china_ppi()

        list_data = []
        for index, row in macro_china_ppi.iterrows():
            tmp_dict = {
                '月份': getattr(row, '月份'),
                '当月': getattr(row, '当月'),
                '当月同比增长': getattr(row, '当月同比增长'),
                '累计': getattr(row, '累计'),
            }
            list_data.append(tmp_dict)

        return list_data

    @staticmethod
    def cpi():
        macro_china_cpi = ak.macro_china_cpi()

        list_data = []
        for index, row in macro_china_cpi.iterrows():
            tmp_dict = {
                '全国-当月': getattr(row, '全国-当月'),
                '全国-同比增长': getattr(row, '全国-同比增长'),
                '全国-环比增长': getattr(row, '全国-环比增长'),
                '全国-累计': getattr(row, '全国-累计'),
                '城市-当月': getattr(row, '城市-当月'),
                '城市-同比增长': getattr(row, '城市-同比增长'),
                '城市-环比增长': getattr(row, '城市-环比增长'),
                '城市-累计': getattr(row, '城市-累计'),
                '农村-当月': getattr(row, '农村-当月'),
                '农村-同比增长': getattr(row, '农村-同比增长'),
                '农村-环比增长': getattr(row, '农村-环比增长'),
                '农村-累计': getattr(row, '农村-累计'),
            }
            list_data.append(tmp_dict)

        return list_data


if "__main__" == __name__:
    pass

"""
    macro china
"""
import sys
import json
import akshare as ak
import gopup as gp


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

    # 企业商品价格指数
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


if "__main__" == __name__:
    pass

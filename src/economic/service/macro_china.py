"""
    macro china
"""
import sys
import json
import akshare as ak
#import tushare as ts


class MacroChinaService(object):

    @staticmethod
    def gksccz():
        macro_china_gksccz_df = ak.macro_china_gksccz()
        print(macro_china_gksccz_df)

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

    @staticmethod
    def shibor():
        macro_china_shibor_all = ak.macro_china_shibor_all()
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
    def qyspjg():
        macro_china_qyspjg = ak.macro_china_qyspjg()
        print(macro_china_qyspjg)


if "__main__" == __name__:
    pass

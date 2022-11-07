"""
    macro china
"""
import sys
import json
import akshare as ak
import tushare as ts


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
            print(getattr(row, 'TRADE_DATE'), getattr(row, 'LPR1Y'))
            data = {'trade_date':str(getattr(row, 'TRADE_DATE')),
                'lpr1y': getattr(row, 'LPR1Y'),
                'lpr5y':getattr(row, 'LPR5Y'),
                'rate1':getattr(row, 'RATE_1'),
                'rate2':getattr(row, 'RATE_2')}

            list_data.append(data)

        return list_data

    # 企业商品价格指数
    @staticmethod
    def qyspjg():
        macro_china_qyspjg = ak.macro_china_qyspjg()
        print(macro_china_qyspjg)


if "__main__" == __name__:
    pass

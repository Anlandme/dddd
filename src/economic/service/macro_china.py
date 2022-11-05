"""
    macro china
"""
import sys
import json
import akshare as ak



class MacroChinaService(object):

    @staticmethod
    def gksccz():
        macro_china_lpr_df = ak.macro_china_lpr()
        return macro_china_lpr_df

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

if "__main__" == __name__:
    pass

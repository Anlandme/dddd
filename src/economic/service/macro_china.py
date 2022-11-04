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

        if samples < macro_china_lpr_df.size:
               macro_china_lpr_df = macro_china_lpr_df.tail(samples)

        trade_date = macro_china_lpr_df['TRADE_DATE'].tolist()
        lpr1y = macro_china_lpr_df['LPR1Y'].tolist()
        lpr5y = macro_china_lpr_df['LPR5Y'].tolist()
        rate1 = macro_china_lpr_df['RATE_1'].tolist()
        rate2 = macro_china_lpr_df['RATE_2'].tolist()
        trade_date_format = []

        for date in trade_date:
            trade_date_format.append(str(date))

        data = {'trade_date':trade_date_format,
                'lpr1y': lpr1y,
                'lpr5y':lpr5y,
                'rate1':rate1,
                'rate2':rate2}

        json_str = json.dumps(data, ensure_ascii=False)
        return json_str

if "__main__" == __name__:
    pass

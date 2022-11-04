"""
    商户信息
    sett_conf_v2.t_business_merchant_info
"""
from src import List, BaseBean, MySQLClient


class MerchantMapperData(BaseBean):
    def __init__(self):
        self.rule_id = ''
        self.merchant_id = ''
        self.merchant_name = ''
        self.mdm_merchant_id = ''

    @staticmethod
    def get_data_dict(db_midas_merchant: MySQLClient):
        sql = '''
            select A.FChannelRateRuleID as rule_id
                , B.FPayMdmMerchantID as merchant_id
                , C.FOU as merchant_name
                , A.FMdmMerchantID as mdm_merchant_id
            from sett_conf_v2.t_merchant_rateid_relation A
            left join midaspay_conf.t_midaspay_merchant_relation B
                on A.FMdmMerchantID = B.FMdmMerchantID
            left join mdm_merchant_conf.t_mdm_merchant_info C
                on A.FMdmMerchantID = C.FMdmMerchantID
            where A.FStatus = 1 and B.FStatus = 1 and C.FStatus = 1
        '''
        db_ret = db_midas_merchant.query(sql, cls=MerchantMapperData)
        data_list: List[MerchantMapperData] = db_ret.data

        data_dict = {}
        for data in data_list:
            data_dict[data.merchant_id] = data
        # end for
        return data_dict


if __name__ == '__main__':
    pass

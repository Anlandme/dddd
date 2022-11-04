CREATE DATABASE `midaspay_conf` DEFAULT CHARACTER SET utf8;
CREATE DATABASE `db_mpay_income` DEFAULT CHARACTER SET utf8;
CREATE DATABASE `db_mpay_channel` DEFAULT CHARACTER SET utf8;

/*
配置表-主数据
sett_conf.t_ou_list
sett_conf_v2.t_channel_mapping
sett_conf_v2.t_merchant_channel_mapping
sett_conf_v2.t_channel_rate_info
sett_conf_v2.t_channel_merchant_info
sett_conf_v2.t_oversea_channel_tax_rule
sett_conf_v2.t_merchant_channel_rate_info
sett_conf_v2.t_business_merchant_info
sett_conf_v2.t_merchant_rateid_relation
midaspay_conf.t_midaspay_merchant_relation

配置表-结算
db_gss_config.t_mpay_plt_info   | 新增
db_gss_config.t_config_mail_to  | 新增
db_gss_config.t_country_info
db_gss_config.t_exchange_rate_daily

暂估相关表
db_tdw_data.t_ssb_midaspay_sum    ｜ 新增
db_mpay_income.t_mpay_esti_base   ｜ 新增
db_mpay_income.t_boss_channel_esti ｜ 新增
db_sett_oversea.t_channel_month_plt_income ｜ 变更字段
db_sett_oversea.t_channel_month_agency_income ｜ 变更字段

账单相关表
db_sett_oversea_merchant_v2.t_merchant_sett_base | 商户结算基础表
db_mpay_channel.t_bill_settlement_unipin       ｜ 新增
db_mpay_channel.t_bill_settlement_mol_detail   ｜ 新增
db_mpay_channel.t_bill_settlement_base         ｜ 新增
db_mpay_income.t_mpay_bill_base_channel        ｜ 新增
db_mpay_income.t_mpay_bill_base_merchant       ｜ 新增
db_mpay_income.t_bill_base_exchange_data       ｜ 新增
db_mpay_income.t_boss_channel_bill             ｜ 新增
db_sett_oversea.t_channel_month_plt_bill       ｜ 变更字段
db_sett_oversea.t_channel_month_agency_bill    ｜ 变更字段
 */

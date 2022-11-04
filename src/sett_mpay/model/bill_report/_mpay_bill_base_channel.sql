-- db_mpay_income.t_mpay_bill_base_channel
USE db_mpay_income;
DROP TABLE IF EXISTS t_mpay_bill_base_channel;
CREATE TABLE `t_mpay_bill_base_channel` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `sett_month` varchar(64) DEFAULT '' COMMENT '结算月份',
  `bill_month` varchar(64) DEFAULT '' COMMENT '账单月份',
  `due_month` varchar(64) DEFAULT '' COMMENT '应收月份',
  `due_date` varchar(64) DEFAULT '' COMMENT '应收日期',
  `merchant_id` varchar(64) DEFAULT '' COMMENT '商户ID',
  `merchant_name` varchar(64) DEFAULT '' COMMENT '商户名称',
  `sub_merchant_id` varchar(64) DEFAULT '' COMMENT '子商户ID',
  `sub_merchant_name` varchar(64) DEFAULT '' COMMENT '子商户名称',
  `product_no` varchar(64) DEFAULT '' COMMENT '产品编号',
  `product_name` varchar(128) DEFAULT '' COMMENT '产品名称',
  `channel` varchar(64) DEFAULT '' COMMENT '渠道名称',
  `cid` varchar(64) DEFAULT '' COMMENT 'CID',
  `mcid` varchar(64) DEFAULT '' COMMENT 'MCID',
  `sub_channel` varchar(64) DEFAULT '' COMMENT '子渠道',
  `payment_period` varchar(64) DEFAULT '' COMMENT '付款周期',
  `channel_country_code` varchar(64) DEFAULT '' COMMENT '渠道国家代码',
  `channel_country_name` varchar(128) DEFAULT '' COMMENT '渠道国家名称',
  `midas_country_code` varchar(64) DEFAULT '' COMMENT '渠道国家代码',
  `midas_country_name` varchar(128) DEFAULT '' COMMENT '渠道国家名称',
  `ori_currency` varchar(64) DEFAULT '' COMMENT '原始币种',
  `ori_income` double(20,2) DEFAULT '0.00' COMMENT '交易金额（计费币种）',
  `ori_refund` double(20,2) DEFAULT '0.00' COMMENT '退款金额（计费币种）',
  `ori_channel_tax` double(20,2) DEFAULT '0.00' COMMENT '渠道代缴税（计费币种）',
  `ori_channel_tax_rate` double(20,2) DEFAULT '0.00' COMMENT '渠道代缴税率',
  `ori_channel_fee` double(20,2) DEFAULT '0.00' COMMENT '渠道费（计费币种）',
  `ori_channel_fee_rate` double(20,2) DEFAULT '0.00' COMMENT '渠道费率',
  `ori_merchant_fee` double(20,2) DEFAULT '0.00' COMMENT '商户费（计费币种）',
  `ori_merchant_fee_rate` double(20,2) DEFAULT '0.00' COMMENT '商户费率',
  `ori_plt_fee` double(20,2) DEFAULT '0.00' COMMENT '平台费（计费币种）',
  `ori_sett_currency_rate` double(20,8) DEFAULT '0.00000000' COMMENT '汇率（计费币种兑结算币种）',
  `sett_currency` varchar(64) DEFAULT '' COMMENT '结算币种',
  `sett_income` double(20,2) DEFAULT '0.00' COMMENT '交易金额（结算币种）',
  `sett_refund` double(20,2) DEFAULT '0.00' COMMENT '退款金额（结算币种）',
  `sett_channel_tax` double(20,2) DEFAULT '0.00' COMMENT '渠道代缴税（结算币种）',
  `sett_channel_fee` double(20,2) DEFAULT '0.00' COMMENT '渠道费（结算币种）',
  `sett_merchant_fee` double(20,2) DEFAULT '0.00' COMMENT '商户费（结算币种）',
  `sett_plt_fee` double(20,2) DEFAULT '0.00' COMMENT '平台费（结算币种）',
  `sett_rmb_currency_rate` double(20,8) DEFAULT '0.00000000' COMMENT '汇率（结算币种兑人民币）',
  `rmb_income` double(20,2) DEFAULT '0.00' COMMENT '交易金额（人民币）',
  `rmb_refund` double(20,2) DEFAULT '0.00' COMMENT '退款金额（人民币）',
  `rmb_channel_tax` double(20,2) DEFAULT '0.00' COMMENT '渠道代缴税（人民币）',
  `rmb_channel_fee` double(20,2) DEFAULT '0.00' COMMENT '渠道费（人民币）',
  `rmb_merchant_fee` double(20,2) DEFAULT '0.00' COMMENT '商户费（人民币）',
  `rmb_plt_fee` double(20,2) DEFAULT '0.00' COMMENT '平台费（人民币）',

  `plt_type` varchar(64) DEFAULT '' COMMENT '平台类型',
  `plt_ou_id` varchar(64) DEFAULT '' COMMENT '平台OU_ID',
  `plt_ou_name` varchar(128) DEFAULT '' COMMENT '平台OU名称',
  `plt_ou_short` varchar(128) DEFAULT '' COMMENT '平台OU简称',
  `plt_mdm_id` varchar(64) DEFAULT '' COMMENT '平台MDM_ID',
  `plt_mdm_name` varchar(128) DEFAULT '' COMMENT '平台MDM名称',
  `plt_coa_no` varchar(64) DEFAULT '' COMMENT '平台COA代码',
  `plt_coa_name` varchar(128) DEFAULT '' COMMENT '平台COA名称',
  `plt_cost_no` varchar(64) DEFAULT '' COMMENT '平台成本中心代码',
  `plt_cost_name` varchar(128) DEFAULT '' COMMENT '平台成本名称',

  `merchant_type` varchar(64) DEFAULT '' COMMENT '商户类型',
  `merchant_ou_id` varchar(64) DEFAULT '' COMMENT '商户OU_ID',
  `merchant_ou_name` varchar(128) DEFAULT '' COMMENT '商户OU名称',
  `merchant_ou_short` varchar(128) DEFAULT '' COMMENT '商户OU简称',
  `merchant_mdm_id` varchar(64) DEFAULT '' COMMENT '商户MDM_ID',
  `merchant_mdm_name` varchar(128) DEFAULT '' COMMENT '商户MDM名称',
  `merchant_coa_no` varchar(64) DEFAULT '' COMMENT '商户COA代码',
  `merchant_coa_name` varchar(128) DEFAULT '' COMMENT '商户COA名称',
  `merchant_cost_no` varchar(64) DEFAULT '' COMMENT '商户成本中心代码',
  `merchant_cost_name` varchar(128) DEFAULT '' COMMENT '商户成本名称',
  `merchant_contract_no` varchar(128) DEFAULT '' COMMENT '商户合同号',
  `channel_mdm_id` varchar(64) DEFAULT '' COMMENT '渠道MDM_ID',
  `channel_mdm_name` varchar(128) DEFAULT '' COMMENT '渠道MDM名称',
  `channel_contract_no` varchar(128) DEFAULT '' COMMENT '渠道合同号',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

-- db_mpay_channel.t_bill_settlement_adyen_detail
USE db_mpay_channel;
DROP TABLE IF EXISTS t_bill_settlement_adyen_detail;
CREATE TABLE `t_bill_settlement_adyen_detail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键',
  `bill_type` varchar(64) NOT NULL COMMENT '账单类型（HM、HS）',
  `bill_month` varchar(7) NOT NULL COMMENT '账单月份（YYYY-MM）',
  `due_month` varchar(7) NOT NULL COMMENT '应收月份（YYYY-MM）',
  `due_date` varchar(10) NOT NULL COMMENT '应收日期（YYYY-MM-DD）',
  `channel` varchar(64) NOT NULL COMMENT '渠道',
  `channel_product_no` varchar(64) NOT NULL COMMENT '渠道产品编号',
  `channel_product_name` varchar(64) NOT NULL COMMENT '渠道产品名称',
  `tran_type` varchar(64) NOT NULL COMMENT '交易类型',
  `sub_channel` varchar(64) NOT NULL COMMENT '子渠道',
  `country` varchar(64) NOT NULL COMMENT '国家',
  `ori_currency` varchar(64) NOT NULL COMMENT '原始币种',
  `company_account` varchar(64) DEFAULT '' COMMENT '公司账户',
  `merchant_account` varchar(64) DEFAULT '' COMMENT '商户账户',
  `psp_reference` varchar(64) DEFAULT '' COMMENT 'Adyen订单号',
  `merchant_reference` varchar(64) DEFAULT '' COMMENT '商户订单号',
  `payment_method` varchar(64) DEFAULT '' COMMENT '支付方法',
  `creation_date` varchar(64) DEFAULT '' COMMENT '创建时间',
  `time_zone` varchar(64) DEFAULT '' COMMENT '时区',
  `type` varchar(64) DEFAULT '' COMMENT '类型',
  `modification_reference` varchar(64) DEFAULT '' COMMENT '支付状态',
  `gross_currency` varchar(64) DEFAULT '' COMMENT '交易币种',
  `gross_debit_gc` varchar(64) DEFAULT '' COMMENT '应收金额（交易币种）',
  `gross_credit_gc` varchar(64) DEFAULT '' COMMENT '应付金额（交易币种）',
  `exchange_rate` varchar(64) DEFAULT '' COMMENT '汇率',
  `net_currency` varchar(64) DEFAULT '' COMMENT '结算币种',
  `net_debit_nc` varchar(64) DEFAULT '' COMMENT '应收金额（结算币种）',
  `net_credit_nc` varchar(64) DEFAULT '' COMMENT '应付金额（结算币种）',
  `commission_nc` varchar(64) DEFAULT '' COMMENT '渠道费',
  `markup_nc` varchar(64) DEFAULT '' COMMENT '收单行费用',
  `scheme_fees_nc` varchar(64) DEFAULT '' COMMENT '卡组织费用',
  `interchange_nc` varchar(64) DEFAULT '' COMMENT '发卡行费用',
  `payment_method_variant` varchar(64) DEFAULT '' COMMENT '支付方法2',
  `batch_number` int(20) DEFAULT '0' COMMENT '批次号',
  `modification_merchant_reference` varchar(64) DEFAULT '' COMMENT '支付状态',
  `issuer_country` varchar(64) DEFAULT '' COMMENT '发卡行国家',
  `shopper_country` varchar(64) DEFAULT '' COMMENT '用户IP国家',
  `file_md5` varchar(128) NOT NULL COMMENT '文件MD5',
  `file_name` varchar(128) NOT NULL COMMENT '文件名',
  `remark` varchar(256) NOT NULL DEFAULT '' COMMENT '备注',
  `special_note` varchar(128) NOT NULL COMMENT '特殊说明',
  `download_date` varchar(10) NOT NULL COMMENT '账单下载日期',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `modify_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;


alter table db_mpay_channel.t_bill_settlement_adyen_detail modify column `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键' after due_date;
alter table db_mpay_channel.t_bill_settlement_adyen_detail modify column `due_month` varchar(7) NOT NULL COMMENT '应收月份（YYYY-MM）' after bill_month;
alter table db_mpay_channel.t_bill_settlement_adyen_detail modify column `due_date` varchar(10) NOT NULL COMMENT '应收日期（YYYY-MM-DD）' after due_month;

alter table db_mpay_channel.t_bill_settlement_adyen_detail modify column `bill_month` varchar(7) NOT NULL COMMENT '账单月份（YYYY-MM）' after bill_type;
alter table db_mpay_channel.t_bill_settlement_adyen_detail add column `id` bigint(20) NOT NULL AUTO_INCREMENT PRIMARY KEY COMMENT '自增主键';
alter table db_mpay_channel.t_bill_settlement_adyen_detail add column `due_month` varchar(7) NOT NULL COMMENT '应收月份（YYYY-MM）' after bill_month;
alter table db_mpay_channel.t_bill_settlement_adyen_detail add column `due_date` varchar(10) NOT NULL COMMENT '应收日期（YYYY-MM-DD）' after due_month;
alter table db_mpay_channel.t_bill_settlement_adyen_detail add column `download_date` varchar(10) NOT NULL COMMENT '账单下载日期' after special_note;

alter table db_mpay_channel.t_bill_settlement_adyen_detail drop column sett_key;
alter table db_mpay_channel.t_bill_settlement_adyen_detail drop column sett_key_desc;
alter table db_mpay_channel.t_bill_settlement_adyen_detail drop column offer_id;
alter table db_mpay_channel.t_bill_settlement_adyen_detail drop column offer_name;
alter table db_mpay_channel.t_bill_settlement_adyen_detail drop column spoa_id;
alter table db_mpay_channel.t_bill_settlement_adyen_detail drop column spoa_name;
alter table db_mpay_channel.t_bill_settlement_adyen_detail drop column sett_group;
alter table db_mpay_channel.t_bill_settlement_adyen_detail drop column sett_group_name;

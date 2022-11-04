-- db_mpay_channel.t_bill_settlement_unipin
USE db_mpay_channel;
DROP TABLE IF EXISTS t_bill_settlement_unipin;
CREATE TABLE `t_bill_settlement_unipin` (
-- 基础信息
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `bill_type` varchar(64) NOT NULL COMMENT '账单类型（HM、HS）',
  `bill_month` varchar(7) NOT NULL COMMENT '账单月份（YYYY-MM）',
  `due_month` varchar(7) NOT NULL COMMENT '应收月份（YYYY-MM）',
  `due_date` varchar(10) NOT NULL COMMENT '应收日期（YYYY-MM-DD）',
  `channel` varchar(64) NOT NULL COMMENT '渠道',
  `channel_product_no` varchar(64) NOT NULL COMMENT '渠道产品编号',
  `channel_product_name` varchar(128) NOT NULL COMMENT '渠道产品名称',
  `sub_channel` varchar(64) NOT NULL COMMENT '子渠道',
  `country` varchar(64) NOT NULL COMMENT '国家',
  `tran_type` varchar(64) NOT NULL COMMENT '交易类型',
  `tran_currency` char(3) NOT NULL COMMENT '交易币种',
  `tran_amount` double(20,4) NOT NULL COMMENT '交易金额',
  `tran_numbers` double(20,4) NOT NULL COMMENT '交易总数',
  `ori_currency` char(3) NOT NULL COMMENT '计费币种',
  `ori_income` double(20,4) NOT NULL COMMENT '计费金额（计费币种）',
  `ori_refund` double(20,4) NOT NULL DEFAULT 0.0 COMMENT '退款金额（计费币种）',
  `ori_channel_tax` double(20,4) NOT NULL COMMENT '渠道代缴税（计费币种）',
  `ori_channel_fee` double(20,4) NOT NULL COMMENT '渠道手续费（计费币种）',
  `ori_settlement` double(20,4) NOT NULL COMMENT '结算金额（计费币种）',
  `sett_currency` char(3) NOT NULL COMMENT '结算币种',

-- 账单信息
  `description` varchar(128) NOT NULL COMMENT '账单描述',
  `sub_merchant` varchar(128) NOT NULL COMMENT '子商户',
  `currency` varchar(3) NOT NULL COMMENT '币种',
  `amount_charged_to_end_users` double(20,4) NOT NULL COMMENT '用户支付金额',
  `vat_rate` double(20,4) NOT NULL COMMENT 'VAT税率',
  `vat_amount` double(20,4) NOT NULL COMMENT 'VAT税金',
  `amount_excluding_tax` double(20,4) NOT NULL COMMENT '不含税的交易金额',
  `percent_fee_rate` double(20,4) NOT NULL COMMENT '百分比费率',
  `percent_fee_total` double(20,4) NOT NULL COMMENT '百分比费用总额',
  `per_transaction_fee` double(20,4) NOT NULL COMMENT '按笔手续费',
  `per_transaction_fee_total` double(20,4) NOT NULL COMMENT '按笔手续费总额',
  `transaction_numbers` double(20,4) NOT NULL COMMENT '交易数量',
  `payout_to_merchant_local` double(20,4) NOT NULL COMMENT '结算金额（当地币）',
  `payout_to_merchant_usd` double(20,4) NOT NULL COMMENT '结算金额（USD）',
  `exchange_rate` double(20,8) NOT NULL COMMENT '汇率',

-- 文件信息
  `file_md5` varchar(128) NOT NULL COMMENT '文件MD5值',
  `file_name` varchar(128) NOT NULL COMMENT '文件名',
  `remark` varchar(256) NOT NULL DEFAULT '' COMMENT '备注',
  `special_note` varchar(128) NOT NULL COMMENT '冗余字段，用于适配特殊场景',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;

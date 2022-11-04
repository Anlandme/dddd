-- db_mpay_channel.t_bill_settlement_mol_detail
USE db_mpay_channel;
DROP TABLE IF EXISTS t_bill_settlement_mol_detail;
CREATE TABLE `t_bill_settlement_mol_detail` (
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
  `tran_amount` double(20,4) NOT NULL DEFAULT '0.0000' COMMENT '交易金额',
  `tran_numbers` double(20,4) NOT NULL DEFAULT '0.0000' COMMENT '交易总数',
  `ori_currency` char(3) NOT NULL COMMENT '计费币种',
  `ori_income` double(20,4) NOT NULL DEFAULT '0.0000' COMMENT '计费金额（计费币种）',
  `ori_refund` double(20,4) NOT NULL DEFAULT '0.0000' COMMENT '退款金额（计费币种）',
  `ori_channel_tax` double(20,4) NOT NULL DEFAULT '0.0000' COMMENT '渠道代缴税（计费币种）',
  `ori_channel_fee` double(20,4) NOT NULL DEFAULT '0.0000' COMMENT '渠道手续费（计费币种）',
  `ori_settlement` double(20,4) NOT NULL DEFAULT '0.0000' COMMENT '结算金额（计费币种）',
  `sett_currency` char(3) NOT NULL COMMENT '结算币种',

-- 账单信息
  `serial_no` varchar(64) NOT NULL COMMENT '序号',
  `merchant_name` varchar(128) NOT NULL COMMENT '商户名称',
  `order_id` varchar(64) NOT NULL COMMENT '订单ID',
  `merchant_reference_id` varchar(64) NOT NULL COMMENT '商户订单ID',
  `payment_ref_id` varchar(64) NOT NULL COMMENT '支付订单ID',
  `origin_order_id` varchar(64) NOT NULL COMMENT '原始订单ID',
  `commission_territory` varchar(128) NOT NULL COMMENT '地区',
  `description` varchar(256) NOT NULL COMMENT '描述',
  `transaction_type` varchar(64) NOT NULL COMMENT '交易类型',
  `merchant_trans_currency` varchar(64) NOT NULL COMMENT '商户交易币种',
  `merchant_trans_amount` double(20,4) NOT NULL COMMENT '商户交易金额',
  `payment_term` double(20,4) NOT NULL COMMENT '付款周期',
  `commission_rate` double(20,4) NOT NULL COMMENT '百分比费率',
  `commission_amount` double(20,4) NOT NULL COMMENT '百分比费用总额',
  `transaction_datetime` varchar(64) NOT NULL COMMENT '交易时间',
  `payment_currency_code` varchar(32) NOT NULL COMMENT '支付币种',
  `payment_amount` double(20,4) NOT NULL COMMENT '支付金额',
  `service_charge_rate` double(20,4) NOT NULL COMMENT '服务费率',
  `service_charge_amount` double(20,4) NOT NULL COMMENT '服务费总额',
  `vat_gst_rate` double(20,4) NOT NULL COMMENT 'VAT/GST税率',
  `vat_gst_amount` double(20,4) NOT NULL COMMENT 'VAT/GST总额',
  `gross_end_user_price` double(20,4) NOT NULL COMMENT '用户价格',

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
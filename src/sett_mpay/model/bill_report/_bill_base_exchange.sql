-- 海外结算报表库
CREATE DATABASE `db_mpay_income` DEFAULT CHARACTER SET utf8;


-- db_mpay_income.t_bill_base_exchange_data
USE db_mpay_income;
DROP TABLE IF EXISTS t_bill_base_exchange_data;
CREATE TABLE `t_bill_base_exchange_data` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `data_type` varchar(64) NOT NULL DEFAULT '' COMMENT '数据类型（HM、HS）',
  `data_date` varchar(10) NOT NULL DEFAULT '' COMMENT '数据日期（YYYY-MM-DD）',
  `data_month` varchar(10) NOT NULL DEFAULT '' COMMENT '数据月份（YYYY-MM）',
  `channel` varchar(64) NOT NULL DEFAULT '' COMMENT '支付渠道',
  `cid` varchar(64) NOT NULL DEFAULT '' COMMENT '支付CID',
  `mcid` varchar(64) NOT NULL DEFAULT '' COMMENT '支付MCID',
  `merchant_id` varchar(64) NOT NULL DEFAULT '' COMMENT '商户号',
  `sub_merchant_id` varchar(64) NOT NULL DEFAULT '' COMMENT '子商户号',
  `tran_type` varchar(64) NOT NULL DEFAULT '' COMMENT '交易类型',
  `tran_currency` char(3) NOT NULL DEFAULT '' COMMENT '交易币种',
  `tran_amount` double(20, 4) NOT NULL DEFAULT 0.0 COMMENT '交易金额',
  `tran_sett_rate` double(20, 8) NOT NULL DEFAULT 0.0 COMMENT '汇率（交易币兑结算币）',
  `sett_currency` char(3) NOT NULL DEFAULT '' COMMENT '结算币种',
  `sett_amount` double(20, 4) NOT NULL DEFAULT 0.0 COMMENT '结算币种金额',
  `sett_rmb_rate` double(20, 8) NOT NULL DEFAULT 0.0 COMMENT '汇率（结算币兑人民币）',
  `rmb_amount` double(20, 4) NOT NULL DEFAULT 0.0 COMMENT 'RMB金额',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
;


-- db_mpay_income.v_bill_base_exchange_rate | 收入综合汇率
use db_mpay_income;
drop view if exists v_bill_base_exchange_rate;
create view v_bill_base_exchange_rate as
-- (
    select data_type
        , data_month
        , tran_currency as ori_currency
        , sett_currency as dst_currency
        , sum(sett_amount)/sum(tran_amount) as exchange_rate
    from db_mpay_income.t_bill_base_exchange_data
    where tran_amount is not null and abs(tran_amount) > 0
    group by data_type, data_month, tran_currency, sett_currency
    union all
    select data_type
        , data_month
        , sett_currency as ori_currency
        , 'CNY' as dst_currency
        , sum(rmb_amount)/sum(sett_amount) as exchange_rate
    from db_mpay_income.t_bill_base_exchange_data
    where tran_amount is not null and abs(tran_amount) > 0
    group by data_type, data_month, sett_currency
-- )
;

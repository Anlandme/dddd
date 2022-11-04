-- db_gss_config.t_mpay_plt_info  | 平台基础信息表
USE db_gss_config;
DROP TABLE IF EXISTS t_mpay_plt_info;
CREATE TABLE `t_mpay_plt_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '自增主键',
  `plt_type` varchar(64) DEFAULT '' COMMENT '平台类型',
  `plt_ou_id` varchar(64) DEFAULT '' COMMENT '平台OU_ID',
  `plt_ou_name` varchar(64) DEFAULT '' COMMENT '平台OU名称',
  `plt_ou_short` varchar(64) DEFAULT '' COMMENT '平台OU简称',
  `plt_mdm_id` varchar(64) DEFAULT '' COMMENT '平台MDM_ID',
  `plt_mdm_name` varchar(128) DEFAULT '' COMMENT '平台MDM名称',
  `plt_coa_no` varchar(64) DEFAULT '' COMMENT '平台COA代码',
  `plt_coa_name` varchar(64) DEFAULT '' COMMENT '平台COA名称',
  `plt_cost_no` varchar(64) DEFAULT '' COMMENT '平台成本中心代码',
  `plt_cost_name` varchar(64) DEFAULT '' COMMENT '平台成本中心名称',
  `status` varchar(1) DEFAULT '' COMMENT '状态（Y、N）',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY plt_ou_id(`plt_ou_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

insert into db_gss_config.t_mpay_plt_info(plt_type, plt_ou_id, plt_ou_name, plt_ou_short
    , plt_mdm_id, plt_mdm_name, plt_coa_no, plt_coa_name, plt_cost_no, plt_cost_name, status)
values
    ('MidasPay', '763', 'Harvest Sharp Limited', 'OU_544_Harvest Sharp(HKD)'
    , '72912231', 'Harvest Sharp Limited', '', '', '83500', 'IEG海外计费联合项目组-公共', 'Y')
;

CREATE DATABASE `db_gss_config` DEFAULT CHARACTER SET utf8;


-- db_gss_config.t_country_info | 国家信息表
USE db_gss_config;
DROP TABLE IF EXISTS t_country_info;
CREATE TABLE `t_country_info` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `country_desc` varchar(128) NOT NULL COMMENT '国家描述',
  `country_name` varchar(128) NOT NULL COMMENT '国家名称_EN',
  `country_name_cn` varchar(128) NOT NULL COMMENT '国家名称_CN',
  `country_code` char(8) NOT NULL COMMENT '国家代码（2位码）',
  `country_code3` char(8) NOT NULL DEFAULT '' COMMENT '国家代码（3位码）',
  `country_number` char(8) NOT NULL DEFAULT '' COMMENT '国家编号',
  `status` char(1) NOT NULL DEFAULT 'Y' COMMENT '状态',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQUE_KEY` (`country_desc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;

insert into db_gss_config.t_country_info(country_desc, country_name, country_name_cn, country_code, country_code3, country_number, status)
select country_name as country_desc, country_name_standard as country_name, country_name_cn, country_code, country_code3, country_number, 'Y'
from db_sett_oversea_config.t_country_info
;

insert into db_gss_config.t_country_info
(country_desc, country_name, country_name_cn, country_code, country_code3, country_number, status)
values
('OT', 'OT', '其他', 'OT', 'OT', 0, 'Y')
;
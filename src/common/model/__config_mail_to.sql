CREATE DATABASE `db_gss_config` DEFAULT CHARACTER SET utf8;


-- db_gss_config.t_config_mail_to | 收件人配置表
USE db_gss_config;
DROP TABLE IF EXISTS t_config_mail_to;
CREATE TABLE `t_config_mail_to` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `mail_key` varchar(128) NOT NULL COMMENT '查询主建',
  `mail_to` varchar(256) NOT NULL COMMENT '收件人',
  `status` char(1) NOT NULL DEFAULT 'Y' COMMENT '状态',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;


insert into db_gss_config.t_config_mail_to(mail_key, mail_to)
values ('download_007_mol.py', 'jiantaowu')
;

insert into db_gss_config.t_config_mail_to(mail_key, mail_to)
values ('DEFAULT', 'jiantaowu')
;
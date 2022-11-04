
CREATE DATABASE `db_gss_auth` DEFAULT CHARACTER SET utf8;


-- db_gss_auth.t_api_auth | API权限表
USE db_gss_auth;
DROP TABLE IF EXISTS t_api_auth;
CREATE TABLE `t_api_auth` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `secret_id` varchar(128) NOT NULL COMMENT '身份ID',
  `secret_key` varchar(128) NOT NULL COMMENT '密钥',
  `host` varchar(128) NOT NULL COMMENT '主机IP（用；拼接）',
  `system_provider` char(128) NOT NULL COMMENT '服务提供方系统名称',
  `system_consumer` char(128) NOT NULL DEFAULT '' COMMENT '服务调用方系统名称',
  `status` char(1) NOT NULL DEFAULT 'Y' COMMENT '状态',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `UNIQUE_KEY` (`secret_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
;


insert into db_gss_auth.t_api_auth(secret_id, secret_key, host, system_provider, system_consumer)
values('sett_api_0001', 'sett_sg_1234', '127.0.0.1', 'sett-api', 'local');

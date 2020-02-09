/*
Navicat MySQL Data Transfer

Source Server         : raspberry
Source Server Version : 50718
Source Host           : 192.168.31.101:3306
Source Database       : zjgtjy

Target Server Type    : MYSQL
Target Server Version : 50718
File Encoding         : 65001

Date: 2018-07-07 21:44:45
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for zjgtjy
-- ----------------------------
DROP TABLE IF EXISTS `zjgtjy`;
CREATE TABLE `zjgtjy` (
  `id` int(11) DEFAULT NULL,
  `dkbh` varchar(255) DEFAULT NULL COMMENT '地块编号',
  `gp_start_time` varchar(32) DEFAULT NULL COMMENT '挂牌起始时间',
  `gp_stop_time` varchar(32) DEFAULT NULL COMMENT '挂牌',
  `pm_start_time` varchar(32) DEFAULT NULL,
  `jj_start_time` varchar(32) DEFAULT NULL,
  `bm_start_time` varchar(32) DEFAULT NULL,
  `bm_stop_time` varchar(32) DEFAULT NULL,
  `bzj_stop_time` varchar(32) DEFAULT NULL,
  `have_dj` varchar(10) DEFAULT NULL,
  `dkmc` varchar(255) DEFAULT NULL,
  `tdwz` varchar(255) DEFAULT NULL,
  `tdyt` varchar(100) DEFAULT NULL,
  `rjl` varchar(50) DEFAULT NULL,
  `ssxzq` varchar(20) DEFAULT NULL,
  `crmj` varchar(255) DEFAULT NULL,
  `crnx` varchar(100) DEFAULT NULL,
  `qsj` varchar(30) DEFAULT NULL,
  `bzj` varchar(30) DEFAULT NULL,
  `zjfd` varchar(30) DEFAULT NULL,
  `tzqd` varchar(30) DEFAULT NULL,
  `jmrtj` varchar(1024) DEFAULT NULL,
  `lxr` varchar(100) DEFAULT NULL,
  `lxrdh` varchar(100) DEFAULT NULL,
  `lxrdz` varchar(255) DEFAULT NULL,
  `jssj` varchar(32) DEFAULT NULL,
  `zgbj` varchar(30) DEFAULT NULL,
  `zgbjdw` varchar(100) DEFAULT NULL,
  `zgxj` varchar(30) DEFAULT NULL,
  `tbzgzcbl` varchar(20) DEFAULT NULL,
  `tbzccsbl` varchar(20) DEFAULT NULL,
  `tbzcblfd` varchar(20) DEFAULT NULL,
  `ptyfqsmj` varchar(30) DEFAULT NULL,
  `tbptyffd` varchar(30) DEFAULT NULL,
  `cjsj` varchar(32) DEFAULT NULL,
  `cjj` varchar(30) DEFAULT NULL,
  `jddw` varchar(100) DEFAULT NULL,
  `status` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;

ALTER TABLE `zjgtjy`
ADD COLUMN `sydkcjsj`  date NULL AFTER `status`,
ADD COLUMN `ycjdkcjsj`  date NULL AFTER `sydkcjsj`,
ADD COLUMN `tdmj`  decimal(20,6) NULL DEFAULT NULL AFTER `ycjdkcjsj`,
ADD COLUMN `jrjm`  decimal(20,6) NULL AFTER `tdmj`,
ADD COLUMN `qplmj`  decimal(20,6) NULL AFTER `jrjm`,
ADD COLUMN `qpzj`  decimal(20,6) NULL AFTER `qplmj`,
ADD COLUMN `cjlmj`  decimal(20,6) NULL AFTER `qpzj`,
ADD COLUMN `cjzj`  decimal(20,6) NULL AFTER `cjlmj`,
ADD COLUMN `yjl`  decimal(20,6) NULL AFTER `cjzj`,
ADD COLUMN `zzbl`  decimal(20,6) NULL AFTER `yjl`,
ADD COLUMN `zzjm`  decimal(20,6) NULL AFTER `zzbl`;


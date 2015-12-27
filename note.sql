DROP TABLE IF EXISTS `account`;
CREATE TABLE  `account` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_bin NOT NULL,
  `email` varchar(128) COLLATE utf8_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
ALTER TABLE  `app_py001`.`account` ADD UNIQUE  `email` (  `email` )

DROP TABLE IF EXISTS `user_note`;
CREATE TABLE  `user_note` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) unsigned NOT NULL,
  `url_id` bigint(20) unsigned NOT NULL,
  `state` tinyint unsigned NOT NULL default 10,
  `view_time` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id-url_id` (`user_id`,`url_id`),
  KEY `url_id` (`url_id`),
  KEY `user_id-view_time` (`user_id`, `state`,`view_time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
DROP TABLE IF EXISTS `url`;
CREATE TABLE  `url` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `url` varbinary(999) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
DROP TABLE IF EXISTS `txt_log`;
CREATE TABLE  `txt_log` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `url_id` bigint(20) unsigned NOT NULL,
  `user_id` bigint(20) unsigned NOT NULL,
  `time` bigint(20) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `url_id-time` (`url_id`,`time`),
  KEY `user_id-time` (`user_id`,`time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

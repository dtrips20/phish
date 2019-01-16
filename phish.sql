use phish;


CREATE TABLE `urls` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `url` text,
  `sha256` char(64) DEFAULT NULL,
  `source` char(200) DEFAULT NULL,
  `label` int(11) DEFAULT NULL,
  `added_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3276 DEFAULT CHARSET=utf8mb4 ;

CREATE TABLE `features` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `sha256` char(64) NOT NULL,
  `label` int(11) NOT NULL DEFAULT '0',
  `count_dots` int(11) NOT NULL DEFAULT '0',
  `count_delimiters` int(11) NOT NULL DEFAULT '0',
  `is_domain_ip` int(11) NOT NULL DEFAULT '0',
  `is_hyphen_present` int(11) NOT NULL DEFAULT '0',
  `count_sub_dir` int(11) NOT NULL DEFAULT '0',
  `count_sub_domain` int(11) NOT NULL DEFAULT '0',
  `count_queries` int(11) NOT NULL DEFAULT '0',
  `shady_tld` int(11) NOT NULL DEFAULT '0',
  `is_suspicious_part_hidden` int(11) NOT NULL DEFAULT '0',
  `is_tiny_url` int(11) NOT NULL DEFAULT '0',
  `anchor_in_url` float Not Null DEFAULT -1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;



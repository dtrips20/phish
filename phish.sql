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
  `id` int(11) NOT NULL,
  `url_id` bigint(20) NOT NULL,
  `label` int(11) NOT NULL DEFAULT '0',
  `count_dot` int(11) NOT NULL DEFAULT '0',
  `count_delim` int(11) NOT NULL DEFAULT '0',
  `is_ip` int(11) NOT NULL DEFAULT '0',
  `is_hyphen_present` int(11) NOT NULL DEFAULT '0',
  `count_sub_dit` int(11) NOT NULL DEFAULT '0',
  `count_queries` int(11) NOT NULL DEFAULT '0',
  `is_shady_tld` int(11) NOT NULL DEFAULT '0',
  `is_suspicious_part_hidden` int(11) NOT NULL DEFAULT '0',
  `is_tiny_url` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ;



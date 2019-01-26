use phish;

drop table urls;
drop table features;
drop table url_html;

CREATE TABLE `urls` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT,
	`url` TEXT NOT NULL,
	`url_sha256` CHAR(64) NOT NULL,
	`source` CHAR(200) NOT NULL,
	`label` INT(11) NOT NULL,
	`added_date` DATETIME NOT NULL,
	`sub_domain` CHAR(255) NOT NULL,
	`domain` CHAR(255) NOT NULL,
	`suffix` CHAR(64) NOT NULL,
	`registered_domain` CHAR(255) NOT NULL,
	`target` CHAR(100) NULL DEFAULT NULL,

	PRIMARY KEY (`id`)
)

ENGINE=InnoDB
;


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

CREATE TABLE `url_html`(
  `id` bigint (20) not null auto_increment,
  `url` text not null,
  `url_sha256` CHAR(64) NOT NULL,
  `res_code` int,
	`html_sha256` CHAR(64) NOT NULL,
	`html` LONGTEXT NOT NULL,

	primary key (`id`)

)
ENGINE=InnoDB;

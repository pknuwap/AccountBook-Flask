
CREATE TABLE `accountBook`.`tbl_user`(
    `user_email` VARCHAR(200) NULL,
    `user_password` VARCHAR(200) NULL,
    `user_name` VARCHAR(200) NULL,
    `user_gender` INT(2),
    `user_grade` INT(2) DEFAULT 0,
    PRIMARY KEY (`user_email`)
);

CREATE TABLE `tbl_account` (
  `account_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_use_user` varchar(45) DEFAULT NULL,
  `account_use_description` varchar(5000) DEFAULT NULL,
`account_use_money` int(11) DEFAULT NULL,
  `account_use_date` int(11) DEFAULT NULL,
`account_write_date` int(11) DEFAULT NULL,
`account_write_user` varchar(45) DEFAULT NULL,
`account_use_option` int(11) DEFAULT NULL,
  PRIMARY KEY (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

# 장부 검색 함수(모든것)

DROP procedure IF EXISTS `accountBook`.`sp_search`;

DELIMITER $$
CREATE PROCEDURE `sp_search` (
IN p_search_number INT(11),
IN p_search_content VARCHAR(200)
)
BEGIN

IF p_search_number = 0 THEN
    select * from tbl_account where account_use_user like concat('%',p_search_content,'%');

ELSEIF p_search_number = 1 THEN
select * from tbl_account where account_write_user like concat('%',p_search_content,'%');

ELSEIF p_search_number = 2 THEN
select * from tbl_account where account_use_description like concat('%',p_search_content,'%');

ELSEIF p_search_number = 3 THEN
select * from tbl_account where account_use_date like concat('%',p_search_content,'%');

ELSEIF p_search_number = 4 THEN
select * from tbl_account where account_write_date like concat('%',p_search_content,'%');

ELSE
select * from tbl_account;

END IF;

END$$
DELIMITER ;

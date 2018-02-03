
# 장부추가 함수 생성
DELIMITER $$
USE `accountBook`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addAccount`(
    IN p_use_user varchar(45),
  IN p_use_description varchar(5000),
IN p_use_money INT,
IN p_use_date INT,
IN p_write_date INT,
IN p_write_user varchar(45),
IN p_use_option INT
)
BEGIN
    insert into tbl_account(
        account_use_user,
        account_use_description,
        account_use_money,
	account_use_date,
	account_write_date,
	account_write_user,
	account_use_option
    )
    values
    (
        p_use_user,
        p_use_description,
        p_use_money,
	p_use_date,
	p_write_date,
	p_write_user,
	p_use_option
    );
END$$

DELIMITER ;
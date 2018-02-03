# 모든 장부보기 함수
DELIMITER $$
USE `accountBook`$$
CREATE PROCEDURE `sp_GetAccountBookAll` (
)
BEGIN
    SELECT * FROM tbl_account ORDER BY account_id DESC;
END$$

DELIMITER ;
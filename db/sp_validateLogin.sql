
# 로그인

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
    IN p_email VARCHAR(200)
)
BEGIN
    select * from tbl_user where user_email = p_email;
END$$
DELIMITER ;
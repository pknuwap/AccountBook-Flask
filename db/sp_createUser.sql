# 신규유저, 회원가입

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser`(
    IN p_email VARCHAR(200),
    IN p_password VARCHAR(200),
    IN p_name VARCHAR(200),
    IN p_gender INT(2),
    IN p_grade INT(2)
)
BEGIN
    if(select exists(select 1 from tbl_user where user_email))THEN
        select '이미 있는 email 입니다';
    ELSE
        insert into tbl_user
        (
            user_email,
            user_password,
            user_name,
            user_gender,
            user_grade
        )
        values
        (
            p_email,
            p_password,
            p_name,
            p_gender,
            p_grade
        );
    END IF;
END$$
DELIMITER ;

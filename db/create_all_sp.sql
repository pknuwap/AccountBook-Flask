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

# 모든 장부보기 함수
DELIMITER $$
USE `accountBook`$$
CREATE PROCEDURE `sp_GetAccountBookAll` (
)
BEGIN
    SELECT * FROM tbl_account ORDER BY account_id DESC;
END$$

DELIMITER ;

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

#통계 페이지 전용 DB 서치 프로시져
DELIMITER $$
CREATE PROCEDURE `sp_search_stat`(
    IN p_year INT(11)
)
BEGIN
    select * from tbl_account where account_use_date like concat('%',p_year,'%');

END$$
DELIMITER ;


# 장부정렬 SQL

# 사용금액이 많은 순으로 정렬
DELIMITER $$
CREATE PROCEDURE `sp_muchUseMoney` (
)
BEGIN
    SELECT * FROM tbl_account ORDER BY account_use_money DESC;
END$$
DELIMITER ;

# 최신순으로 정렬
DELIMITER $$
CREATE PROCEDURE `sp_lastDay` (
)
BEGIN
    SELECT * FROM tbl_account ORDER BY account_use_date DESC;
END$$
DELIMITER ;



# 로그인

DELIMITER $$
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin`(
    IN p_email VARCHAR(200)
)
BEGIN
    select * from tbl_user where user_email = p_email;
END$$
DELIMITER ;

#통계 페이지 전용 DB 서치 프로시져
DELIMITER $$
CREATE PROCEDURE `sp_search_stat`(
    IN p_year INT(11)
)
BEGIN
    select * from tbl_account where account_use_date like concat('%',p_year,'%');

END$$
DELIMITER ;
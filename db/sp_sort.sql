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



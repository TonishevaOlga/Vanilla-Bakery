/
CREATE TABLE products1       
               (prod_id     NUMBER(6)
                   CONSTRAINT prod_id_pk       PRIMARY KEY,
                prod_name   VARCHAR2(60) 
                   CONSTRAINT prod_name_nn     NOT NULL,
                price	    NUMBER(10)
                   CONSTRAINT price_nn         NOT NULL
                   CONSTRAINT price_ck         CHECK (price>=0));
/
CREATE TABLE customers1       
               (cust_id     NUMBER(6)
                   CONSTRAINT cust_id_pk       PRIMARY KEY,
                last_n   	VARCHAR2(30),   
                first_n	    VARCHAR2(20),
                mail        VARCHAR2(50)
                   CONSTRAINT mail_nn         NOT NULL
                   CONSTRAINT mail_uk         UNIQUE,
                district    VARCHAR2(10));            
/
CREATE TABLE orders1       
               (ord_id      NUMBER(6)
                   CONSTRAINT ord_id_pk       PRIMARY KEY,
                ord_date    DATE 
                   CONSTRAINT date_nn         NOT NULL,
                prod_id     NUMBER(6)
                   CONSTRAINT prod_id_fk      REFERENCES
                    products1 (prod_id), 
                qty         NUMBER(6) 
                   CONSTRAINT qty_nn          NOT NULL,
                cust_id     NUMBER(6) 
                   CONSTRAINT cust_id_fk      REFERENCES
                    customers1 (cust_id));
/
CREATE TABLE ord_summ_f
               (ord_date   DATE,
                day_profit NUMBER(10));
/
CREATE TABLE month_summ
               (ord_month    VARCHAR2(10),
                month_profit NUMBER(15));
/
--создание пакета с процедурами, кот. заполн€ют табл. ord_summ_f и month_summ
/
CREATE OR REPLACE PACKAGE pkg_project
IS

  PROCEDURE make_final_aggr_ord_summ_f;
  PROCEDURE make_final_aggr_month;

END pkg_project;
/
CREATE OR REPLACE PACKAGE BODY pkg_project
IS

  PROCEDURE make_final_aggr_ord_summ_f
  IS
  BEGIN 
      EXECUTE IMMEDIATE 'TRUNCATE TABLE ord_summ_f DROP STORAGE';
      INSERT INTO ord_summ_f (ord_date, day_profit)
      SELECT o.ord_date, SUM(o.qty * p.price) as day_profit
      FROM orders1 o LEFT JOIN products1 p
            ON o.prod_id = p.prod_id 
      GROUP BY o.ord_date
      ORDER BY o.ord_date;
      COMMIT;
  END make_final_aggr_ord_summ_f;
  
  PROCEDURE make_final_aggr_month
  IS
  BEGIN 
      EXECUTE IMMEDIATE 'TRUNCATE TABLE month_summ DROP STORAGE';
      INSERT INTO month_summ (ord_month, month_profit)
      SELECT TO_CHAR(TRUNC (ord_date, 'mm'), 'mm') || '.' || TO_CHAR(TRUNC (ord_date, 'mm'), 'yyyy')  AS ord_month, SUM(day_profit) AS month_profit
      FROM ord_summ_f
      GROUP BY TRUNC(ord_date, 'mm');
      COMMIT;
  END make_final_aggr_month;

END pkg_project;

                
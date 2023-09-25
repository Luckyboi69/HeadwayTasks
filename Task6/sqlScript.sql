--ALTER USER hr IDENTIFIED BY hr account unlock;
--CREATE USER infa IDENTIFIED BY infa;
--CREATE USER core IDENTIFIED BY core;
--GRANT CONNECT , resource TO core
--GRANT dbo TO infa;

/* 
 * 	create table for row transaction
 * 
 * */

CREATE TABLE public.sales_transaction (
  ORDERNUMBER Integer,
  QUANTITYORDERED Integer,
  PRICEEACH Integer,
  ORDERLINENUMBER Integer,
  SALES Integer,
  ORDERDATE DATE,
  STATUS VARCHAR(50),
  QTR_ID Integer,
  MONTH_ID Integer,
  YEAR_ID Integer,
  PRODUCTLINE VARCHAR(50),
  MSRP Integer,
  PRODUCTCODE VARCHAR(50),
  CUSTOMERNAME VARCHAR(100),
  PHONE VARCHAR(20),
  ADDRESSLINE1 VARCHAR(100),
  ADDRESSLINE2 VARCHAR(100),
  CITY VARCHAR(100),
  STATE VARCHAR(50),
  POSTALCODE VARCHAR(20),
  COUNTRY VARCHAR(50),
  TERRITORY VARCHAR(50),
  CONTACTLASTNAME VARCHAR(50),
  CONTACTFIRSTNAME VARCHAR(50),
  DEALSIZE VARCHAR(50)
);

--DROP TABLE CORE.sales_transaction
--TRUNCATE TABLE core.SALES_TRANSACTION 
SELECT count(*) + 1 AS row_count FROM public.SALES_TRANSACTION st ;

SELECT * FROM public.SALES_TRANSACTION st ;


-------------------------------------------------------------------------------------------------------------------------
/*
 * 	Create table address 
 *  with column 
		    ADDRESSLINE1	
			ADDRESSLINE2	
			CITY	
			STATE	
			POSTALCODE	
			COUNTRY	
 * 
 * */



-------------------------------------------------------------------------------------------------------------------------
/*
 * 	Create table Customer 
 *  with column 
		    CUSTOMERNAME	
			PHONE	
			TERRITORY	
			CONTACTLASTNAME	
			CONTACTFIRSTNAME	
			DEALSIZE
 * */

--DROP TABLE public.customer;
CREATE  TABLE public.customer (
	customer_id Integer primary KEY NOT NULL ,
	CUSTOMERNAME varchar(100),
  	PHONE varchar(20),
  	TERRITORY  VARCHAR(50),
  	CONTACTLASTNAME	varchar(50),
	CONTACTFIRSTNAME varchar(50),	
	DEALSIZE varchar(50)
);
CREATE TABLE public.address (
    address_id Integer PRIMARY KEY,
    ADDRESSLINE1 VARCHAR(100),
    ADDRESSLINE2 VARCHAR(100),
    CITY VARCHAR(100),
    STATE VARCHAR(50),
    POSTALCODE VARCHAR(20),
    COUNTRY VARCHAR(50),
    customer_id INTEGER,
    FOREIGN KEY (customer_id) REFERENCES public.customer (customer_id)
); 

-- add foreign key for customer 
--ALTER TABLE CORE.customer
--ADD (product_id NUMBER,
--     CONSTRAINT fk_product_id
--     FOREIGN KEY (product_id)
--     REFERENCES core.product(product_id)
--);

-- DROP CONSTRAINTS IF YOU NEED
--ALTER TABLE CORE.CUSTOMER DROP CONSTRAINT fk_product_id

-- invistigate 
SELECT COUNT(*) FROM (SELECT DISTINCT CUSTOMERNAME ,PHONE,TERRITORY,CONTACTFIRSTNAME,CONTACTLASTNAME ,DEALSIZE   FROM public.SALES_TRANSACTION);


-- create sequence 
--DROP SEQUENCE public.customer_id_seq;
CREATE SEQUENCE public.customer_id_seq;

-- create trigger for this sequence

CREATE OR REPLACE FUNCTION customer_bi()
RETURNS TRIGGER AS $$
BEGIN
  NEW.customer_id := nextval('public.customer_id_seq');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER customer_bi
BEFORE INSERT ON public.customer
FOR EACH ROW
EXECUTE FUNCTION customer_bi();

INSERT INTO public.customer ( CUSTOMERNAME, PHONE, TERRITORY , CONTACTFIRSTNAME , CONTACTLASTNAME , DEALSIZE)  
	SELECT DISTINCT CUSTOMERNAME ,PHONE, TERRITORY,CONTACTFIRSTNAME,CONTACTLASTNAME ,DEALSIZE   FROM public.SALES_TRANSACTION;
	
	
-- analysis 
--SELECT count(*) FROM core.customer;
--SELECT * FROM core.customer;
--  Count of rows in the customer table
SELECT COUNT(*) AS row_count FROM public.customer;

--  Displaying customer and their associated addresses
SELECT
    c.customer_id,
    c.CUSTOMERNAME,
    c.PHONE,
    c.TERRITORY,
    a.ADDRESSLINE1,
    a.ADDRESSLINE2,
    a.CITY,
    a.STATE,
    a.POSTALCODE,
    a.COUNTRY
FROM
    public.customer c
INNER JOIN
    public.address a ON c.customer_id = a.customer_id;

--  Count of customers from 'Land of Toys Inc.' and their associated addresses
SELECT COUNT(*) AS customer_count
FROM public.customer c
INNER JOIN address a ON c.customer_id = a.customer_id
WHERE c.CUSTOMERNAME = 'Land of Toys Inc.';


-------------------------------------------------------------------------------------------------------------------------
/*
 * 	Create table product 
 *  with column 
		    PRODUCTLINE
			PRODUCTCODE
			MSRP
 * 
 * */
 CREATE TABLE public.product (
	product_id Integer PRIMARY KEY,
	PRODUCTLINE varchar(50),
  	PRODUCTCODE varchar(20),
  	MSRP Integer
);

-- create sequence 
--DROP SEQUENCE public.product_id_seq;
CREATE SEQUENCE public.product_id_seq;

-- Create or replace trigger for this sequence
CREATE OR REPLACE FUNCTION product_bi()
RETURNS TRIGGER AS $$
BEGIN
  NEW.product_id := nextval('public.product_id_seq');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER product_bi
BEFORE INSERT ON public.product
FOR EACH ROW
EXECUTE FUNCTION product_bi();


--DROP TABLE public.product;



-- ADD foreign column to another table 

-- Add the customer_id column to the product table
ALTER TABLE public.product
ADD COLUMN customer_id INTEGER;

-- Add a foreign key constraint
ALTER TABLE public.product
ADD CONSTRAINT fk_customer_id
    FOREIGN KEY (customer_id)
    REFERENCES public.customer(customer_id);


ALTER TABLE public.product DROP CONSTRAINT fk_customer_id;


-- insert product data into table 

INSERT INTO public.PRODUCT (PRODUCTLINE, PRODUCTCODE, MSRP) SELECT DISTINCT PRODUCTLINE, PRODUCTCODE, MSRP FROM public.SALES_TRANSACTION;

SELECT * FROM public.PRODUCT ;



-------------------------------------------------------------------------------------------------------------------------
/*
 * 	Create table Has_product   [Bridge]
 *  with column 
		    product_id 	
			customer_id 	
			
 * 
 * */

--DROP TABLE public.has_proberty;

CREATE  TABLE public.has_proberty (
	customer_id Integer ,
	product_id Integer ,
--  	PRIMARY KEY (customer_id,product_id),
  	FOREIGN KEY (customer_id) REFERENCES public.customer (customer_id),
  	FOREIGN KEY (product_id) REFERENCES public.product (product_id)
);

SELECT * FROM public.has_proberty;

INSERT INTO public.has_proberty (CUSTOMER_ID , product_id) 

SELECT c.CUSTOMER_ID , p.product_id 
	FROM public.CUSTOMER c 
		INNER JOIN public.SALES_TRANSACTION st 
			ON 
				c.CUSTOMERNAME = st.CUSTOMERNAME 
			AND 
				c.PHONE  = st.PHONE 
			AND 
				c.TERRITORY = st.TERRITORY
			AND 
				c.CONTACTLASTNAME = st.CONTACTLASTNAME
			AND 
				c.CONTACTFIRSTNAME = st.CONTACTFIRSTNAME
			AND 
				c.DEALSIZE = st.DEALSIZE
  		
		INNER JOIN public.PRODUCT p 
			ON 
				p.PRODUCTLINE = st.PRODUCTLINE 
			AND 
				p.PRODUCTCODE  = st.PRODUCTCODE 
			AND 
				p.MSRP  = st.MSRP ;

-------------------------------------------------------------------------------------------------------------------------

-- analysis 
				
SELECT count(*) FROM public.CUSTOMER c 
	INNER JOIN public.HAS_PROBERTY hp 
		ON hp.CUSTOMER_ID = c.CUSTOMER_ID 
	INNER JOIN public.PRODUCT p 
		ON p.PRODUCT_ID = hp.PRODUCT_ID 
	WHERE CUSTOMERNAME = 'Land of Toys Inc.';
-------------------------------------------------------------------------------------------------------------------------
/*
 * 	Create table date 
 *  with column 
		    ORDERDATE	
			QTR_ID	
			MONTH_ID	
			YEAR_ID
 * 
 * */


CREATE TABLE public.date_table (
    ORDERDATE DATE PRIMARY KEY,
    QTR_ID Integer,
    MONTH_ID Integer,
    YEAR_ID Integer
);




-------------------------------------------------------------------------------------------------------------------------
/*
 * 	Create table order 
 *  with column 
		    ORDERNUMBER	
			QUANTITYORDERED	
			PRICEEACH	
			ORDERLINENUMBER	
			SALES
			STATUS
 * 
 * */


CREATE TABLE public.order_table (
    ORDERNUMBER Integer,
    QUANTITYORDERED Integer,
    PRICEEACH NUMERIC(10, 2),
    ORDERLINENUMBER Integer,
    SALES NUMERIC(10, 2),
    STATUS VARCHAR(50),
    ORDERDATE DATE,
    CUSTOMER_ID INTEGER,
    FOREIGN KEY (ORDERDATE) REFERENCES public.date_table(ORDERDATE),
    FOREIGN KEY (CUSTOMER_ID) REFERENCES public.customer(customer_id)
);








-------------------------------------------------------------------------------------------------------------------------


SELECT 
    o.ORDERNUMBER,
    o.ORDERDATE,
    c.CUSTOMER_ID,
    (SELECT COUNT(*) FROM public.SALES_TRANSACTION st WHERE st.CUSTOMERNAME = 'Land of Toys Inc.') AS product
FROM 
    order_table o
JOIN
    public.CUSTOMER c ON o.CUSTOMER_ID = c.CUSTOMER_ID;

--SELECT count(*) AS product FROM core.SALES_TRANSACTION st 
	--WHERE CUSTOMERNAME ='Land of Toys Inc.'







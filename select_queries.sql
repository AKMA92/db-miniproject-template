-- ==========================================
-- SQL DML Select Statements
-- ==========================================

-- ==========================================
-- Company
-- ==========================================
 SELECT
    c.company_id       AS "Firma-ID",
    c.name             AS "Name",
    c.company_type     AS "Typ",
    c.email            AS "E-Mail",
    c.telephone_number AS "Telefonnummer",
    c.address          AS "Adresse"
 FROM company c;


select * from company;--getestet
select name, type from company;

-- ==========================================
-- Employee
-- ==========================================
select * from employee;--getestet
select last_name, telephone_number from employee; --getestet
select * from employee where employee_id < 20; --getestet
select * from employee where employee_id between 10 and 20; --getestet



SELECT
  e.employee_id      AS "Mitarbeiter-ID",
  c.company_id       AS "Firma-ID",
  e.first_name       AS "Vorname",
  e.last_name        AS "Nachname",
  e.email            AS "E-Mail",
  e.telephone_number AS "Telefonnummer",
  c.name             AS "Firma"
FROM employee e
JOIN employed em
  ON em.employee_id = e.employee_id
JOIN company c
  ON c.company_id = em.company_id;

-- ==========================================
-- Product
-- ==========================================
select * from product; --getestet
select type, name from product where category = 'hygiene'; --getestet
select type from product where



SELECT
  p.product_id       AS "Produkt-ID",
  p.name             AS "Name",
  p.category         AS "Kategorie",
  p.product_type     AS "Typ",
From product

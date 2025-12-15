DROP TABLE IF EXISTS DELIVERED CASCADE;
DROP TABLE IF EXISTS EMPLOYED CASCADE;
DROP TABLE IF EXISTS PRODUCT CASCADE;
DROP TABLE IF EXISTS EMPLOYEE CASCADE;
DROP TABLE IF EXISTS COMPANY CASCADE;

CREATE TABLE COMPANY (
    company_id        INTEGER PRIMARY KEY,
    name              VARCHAR(100) NOT NULL,
    company_type      VARCHAR(100) NOT NULL,
    email             VARCHAR(255) NOT NULL,
    telephone_number  VARCHAR(50) NOT NULL,
    address           TEXT NOT NULL,
    CONSTRAINT uq_company_email UNIQUE (email),
    CONSTRAINT chk_company_email CHECK (email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$'),
    CONSTRAINT chk_company_type CHECK (company_type IN ('Supplier','Customer','Own'))
);

CREATE TABLE EMPLOYEE (
    employee_id       INTEGER PRIMARY KEY,
    first_name        VARCHAR(100) NOT NULL,
    last_name         VARCHAR(100) NOT NULL,
    email             VARCHAR(255) NOT NULL,
    telephone_number  VARCHAR(50) NOT NULL,
    CONSTRAINT uq_employee_email UNIQUE (email),
    CONSTRAINT chk_employee_email CHECK (email ~ '^[^@\s]+@[^@\s]+\.[^@\s]+$')
);

CREATE TABLE PRODUCT (
    product_id    INTEGER PRIMARY KEY,
    name          VARCHAR(100) NOT NULL,
    category      VARCHAR(100) NOT NULL,
    product_type  VARCHAR(100) NULL,
    CONSTRAINT chk_product_category CHECK (category IN ('food','hygiene'))
);

CREATE TABLE EMPLOYED (
    employee_id INT PRIMARY KEY REFERENCES EMPLOYEE (employee_id),
    company_id  INT NOT NULL REFERENCES COMPANY (company_id)
);

CREATE TABLE DELIVERED (
    product_id INT NOT NULL REFERENCES PRODUCT (product_id),
    company_id INT NOT NULL REFERENCES COMPANY (company_id),
    PRIMARY KEY (product_id, company_id)
);

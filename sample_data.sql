-- ==========================================
-- SQL DML Insert Statements
-- ==========================================

insert into Employee(first_name, last_name, email, telephone_number, employee_id) values
('Maria', 'Maurer', 'maurer@elmex.ch', '078 888 88 99', 11),
('Laura', 'Steiner', 'steiner@elmex.ch', '079 888 88 99', 12),
('Hans', 'Schlegel', 'schlegel@evian.ch', '077 858 77 78', 21),
('Peter', 'Aebli', 'aebli@nestle.ch', '078 855 38 49', 31),
('Ursulla', 'Huber', 'huber@pampers.ch', '078 884 66 90', 41),
('Philip', 'Meili', 'meili@lindt.ch', '078 884 66 66', 51),
('Martina', 'Merz', 'merz@farmer.ch', '078 588 00 99', 61),
('Daniel', 'Keller', 'keller@nestle.ch', '079 555 12 34', 71),
('Sandra', 'Fischer', 'fischer@nestle.ch', '078 444 23 45', 81),
('Thomas', 'Brunner', 'brunner@nestle.ch', '077 333 34 56', 91);


insert into Company(name, company_type, email, telephone_number, address, company_id) values
('Elmex', 'Supplier','info@elmex.ch', '044 888 88 99', 'elmexstrasse 25 4500 zürich', 1),
('Evian', 'Supplier', 'info@evian.ch', '044 858 77 78', 'evianstrasse 6 8501 zürich',2),
('Nestlé', 'Supplier', 'info@nestle.ch', '044 855 38 49', 'nestléstrasse 7 8502 zürich',3),
('Pampers', 'Supplier', 'info@pampers.ch', '044 884 66 90', 'pampersstrasse 8 8500 zürich',4),
('Lindt', 'Supplier', 'info@lindt.ch', '044 884 66 66', 'lindtstrasse 9 8503 zürich',5),
('Farmer', 'Supplier', 'info@farmer.ch', '044 588 00 99', 'farmerstrasse 10 8504 zürich',6),
('Alnatura', 'Supplier', 'info@alnatura.ch', '044 600 00 55', 'alnaturastrasse 12 8604 zürich',7),
('You', 'Supplier', 'info@you.ch', '044 900 00 55', 'youstrasse 15 8606 zürich',8),
('Soft Comfort', 'Supplier', 'info@softcomfort.ch', '044 700 00 55', 'softcomfortstrasse 14 8609 zürich',9),
('Migros Bio', 'Own', 'info@migros.ch', '044 700 00 55', 'Migrosstrasse 14 8609 zürich',10);

INSERT INTO Product(product_id, name, category, product_type) VALUES
(1110, 'Elmex Sensitive Whitening', 'hygiene', 'toothpaste'),
(1111, 'Elmex Clean Pro Toothbrush', 'hygiene', 'toothbrush'),
(1112, 'Elmex Dental Floss Mint', 'hygiene', 'dental floss'),
(2220, 'Evian Natural Mineral Water 1.5L', 'food', 'Natural Mineral Water'),
(3330, 'Nestlé Baby Cereals Banana', 'food', 'Baby cereals'),
(4440, 'Pampers Fresh Clean Wipes 52', 'hygiene', 'Pampers Fresh Clean'),
(4441, 'Pampers Baby-Dry Pants Size 4', 'hygiene', 'Pampers baby-dry Pants'),
(5550, 'Lindt Dubai Style Chocolate 100g', 'food', 'Dubai Style Chocolate'),
(6660, 'Alnatura Dinkel Spaghettini 500g', 'food', 'Dinkel Spaghettini'),
(7770, 'You Green Smoothie 250ml', 'food', 'Smoothie'),
(8880, 'Soft Comfort Toilet Paper 3-ply 8-rolls', 'hygiene', 'Toilet paper');

insert into EMPLOYED (employee_id, company_id) values
(11,1),
(12,1),
(21,2),
(31,3),
(41,4),
(51,5),
(61,6),
(71,3),
(81,3),
(91,3);

insert into DELIVERED (product_id , company_id) values
(1110,1),
(1111,1),
(1112,1),
(2220,2),
(3330,3),
(4440,4),
(4441,4),
(5550,5);




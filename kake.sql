# CREATE kake
CREATE DATABASE IF NOT EXISTS kake;

# USE IT
USE kake;

# Create Auth table
CREATE TABLE IF NOT EXISTS AUTH(
	ID CHAR(10) PRIMARY KEY,
	ACCESS_TOKEN CHAR(64),
	EMAIL_ID VARCHAR(320) NOT NULL,
	PASSWD VARCHAR(15) NOT NULL,
	USERNAME VARCHAR(15) NOT NULL,
	VERIFIED BOOL DEFAULT FALSE
);

# Create Cakes table
CREATE TABLE IF NOT EXISTS CAKES(
	ID INT PRIMARY KEY, 
	PATH VARCHAR(30), 
	NAME VARCHAR(30), 
	PRICE FLOAT,
	QTYPRESENT INT
);

# Create Cart table
# CREATE TABLE IF NOT EXISTS CART(
# 	ID INT PRIMARY KEY,
# 	ITEMS VARCHAR(1000) DEFAULT '[]',
# 	USERID CHAR(10),
# 	CHECKOUT_TOKEN CHAR(10) NOT NULL,
# 	PAID BOOL DEFAULT FALSE,
# 	DATEOFPURCHASE DATE,
# 	DATEOFPAY DATE,
# 	CONSTRAINT fk_accessToken FOREIGN KEY(USERID) REFERENCES AUTH(ID)
# );

# Insert value into cakes
INSERT INTO CAKES VALUES
(1, 'choco.png', 'Chocolate Cake', 678, 50),
(2, 'toasted-marshmallow.png', 'Toasted Marshmallow Cake', 949, 45), 
(3, 'humming-bird.png', 'Hummingbird Cake', 1600, 50),
(4, 'texas-sheet.png', 'Texas Sheet Cake', 699, 45), 
(5, 'white-almond.png', 'White Almond Wedding Cake', 5500, 50), 
(6, 'alfajor.png', 'Alfajor Cake', 1954, 50);

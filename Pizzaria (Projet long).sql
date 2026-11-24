DROP DATABASE pizzaria;
CREATE DATABASE pizzaria;
USE pizzaria;

CREATE TABLE croute(
id INT,
nom VARCHAR(255),
PRIMARY KEY (id)
);

CREATE TABLE sauce(
id INT,
nom VARCHAR(255),
PRIMARY KEY (id)
);

CREATE TABLE garniture(
id INT,
nom VARCHAR(255),
PRIMARY KEY (id)
);

CREATE TABLE pizza (
id INT NOT NULL AUTO_INCREMENT,
croute_id INT,
sauce_id INT NULL,
statut VARCHAR(255) NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY (croute_id) REFERENCES croute(id),
FOREIGN KEY (sauce_id) REFERENCES sauce(id)
);

CREATE TABLE pizza_garniture (
pizza_id INT,
garniture_id INT,
FOREIGN KEY (pizza_id) REFERENCES pizza(id),
FOREIGN KEY (garniture_id) REFERENCES garniture(id)
);

CREATE TABLE clients (
id INT NOT NULL AUTO_INCREMENT,
nom VARCHAR(255),
numero_telephone INT,
adresse_livraison VARCHAR(255),	
pizza_id INT,
PRIMARY KEY (id),
FOREIGN KEY(pizza_id) REFERENCES pizza(id)
);

CREATE TABLE liste (
id INT NOT NULL AUTO_INCREMENT,
croute_id INT,
sauce_id INT NULL,
statut VARCHAR(255) NOT NULL,
PRIMARY KEY(id),
FOREIGN KEY (croute_id) REFERENCES croute(id),
FOREIGN KEY (sauce_id) REFERENCES sauce(id)
);

INSERT INTO croute(id, nom)
VALUES
(1, "Classique"),
(2, "Mince"),
(3, "Épaisse");

INSERT INTO sauce(id, nom)
VALUES
(1, "Tomate"),
(2, "Spaghetti"),
(3, "Alfredo");

INSERT INTO garniture(id, nom)
VALUES
(1, "Pepperoni"),
(2, "Champignons"),
(3, "Oignons"),
(4, "Poivrons"),
(5, "Olives"),
(6, "Anchois"),
(7, "Bacon"),
(8, "Poulet"),
(9, "Maïs"),
(10, "Fromage"),
(11, "Piments forts");

DELIMITER $$
CREATE TRIGGER liste_commandes
AFTER INSERT
ON pizza FOR EACH ROW
BEGIN
	IF New.statut = 'en attente' THEN
	INSERT INTO liste(croute_id, sauce_id, statut)
    VALUES(NEW.croute_id, NEW.sauce_id, NEW.statut); 
    END IF;
END $$
DELIMITER ;





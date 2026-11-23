from flask import Flask, render_template, request
import mysql.connector
import os 
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_port = os.getenv('DB_PORT')

app = Flask(__name__)

db = mysql.connector.connect(
    host=db_host,
    user=db_user,
    passwd=db_password,
    database=db_name,
    port=db_port
)
print(db_host)
print(db_user)
print(db_password)
print(db_name)

@app.route('/')
def index():
    # Curseur de Garniture
    cursorGarniture = db.cursor()
    cursorGarniture.execute("SELECT nom FROM garniture")
    garniture = cursorGarniture.fetchall()
    cursorGarniture.close()
    # Curseur de Croute
    cursorCroute = db.cursor()
    cursorCroute.execute("SELECT nom FROM croute")
    croute = cursorCroute.fetchall()
    cursorCroute.close()
    # Curseur de Sauce
    cursorSauce = db.cursor()
    cursorSauce.execute("SELECT nom FROM sauce")
    sauce = cursorSauce.fetchall()
    cursorSauce.close()
    print("Fonction complète.")
    return render_template('index.html', garniture=garniture, croute=croute, sauce=sauce)

@app.route("/", methods=["POST"])
def validation():
    connexion = mysql.connector.connect(
        host = db_host,
        user = db_user,
        password = db_password,
        database = db_name,
        port = db_port
    )
    # Récupérer les données
    nom = request.form['nom']
    numero_telephone = request.form['numero_tel']
    adresse = request.form['adresse']
    garniture = [
    request.form["Garniture1"],
    request.form["Garniture2"],
    request.form["Garniture3"],
    request.form["Garniture4"] 
    ]
    croute = request.form['Croute']
    sauce = request.form['Sauce']
    print(garniture) # Donnée converti ainsi: [" ", " "," "]
    print(croute) # Donnée bien convertie!
    print(sauce) # Donné bien convertie!
    try:
        cursor = connexion.cursor(dictionary=True)
        crouteID = "SELECT id FROM croute WHERE nom = %(_croute)s"
        parametres1 = {
            '_croute': croute
        }
        cursor.execute(crouteID, parametres1)
        for ligne in cursor:
            croute_ID = ligne['id']
        sauce_ID = ""
        if sauce != "rien":
            sauceID = "SELECT id FROM sauce WHERE nom = %(_sauce)s"
            parametres2 = {
            '_sauce': sauce
            }
            cursor.execute(sauceID, parametres2)
            for ligne in cursor:
                sauce_ID = ligne['id']

        #Si il y a une sauce
        if sauce_ID != "":
            query = "INSERT INTO pizza(croute_id, sauce_id, statut) VALUES(%(_croute)s, %(_sauce)s, 'en attente');"
            parametres3 = {
                '_croute': croute_ID,
                '_sauce': sauce_ID
            }
            print("Avant l'exécution...")
            cursor.execute(query, parametres3)
            connexion.commit()
            print("Pizza enregistré!")
            pizza_select = "SELECT id FROM pizza ORDER BY id DESC LIMIT 1;"
            cursor.execute(pizza_select)
            for ligne in cursor:
                pizza_ID = ligne['id']   
            # si il y a une garniture
            while garniture:
                garniture_choisi = garniture.pop()
                if (garniture_choisi != 'rien'):
                    garniture_id =  "SELECT id FROM garniture WHERE nom = %(_garniture)s"
                    parametres4 = {
                        '_garniture': garniture_choisi
                    }
                    cursor.execute(garniture_id, parametres4)
                    for ligne in cursor:
                        garniture_ID = ligne['id']
                    if garniture_choisi:
                        print("Il y a une garniture!")
                        garniture_entre = "INSERT INTO pizza_garniture(pizza_id, garniture_id) VALUES(%(_pizza_id)s, %(_garniture_id)s)"
                        parametres5 = {
                            '_pizza_id': pizza_ID,
                            '_garniture_id': garniture_ID
                        }
                    cursor.execute(garniture_entre, parametres5)
                    connexion.commit()
        else:
            query = "INSERT INTO pizza(croute_id, statut) VALUES(%(_croute)s, 'en attente');"
            parametres3 = {
                '_croute': croute_ID
            }                
            print("Croute:", croute_ID)     
            # Si il y a une garniture     
            print("Avant l'exécution...")
            cursor.execute(query, parametres3)
            connexion.commit()
            print("Pizza enregistré!")
            pizza_select = "SELECT id FROM pizza ORDER BY id DESC LIMIT 1;"
            cursor.execute(pizza_select)
            for ligne in cursor:
                pizza_ID = ligne['id']
            # si il y a une garniture
            while garniture:
                garniture_choisi = garniture.pop()
                if (garniture_choisi != 'rien'):
                    garniture_id =  "SELECT id FROM garniture WHERE nom = %(_garniture)s"
                    parametres4 = {
                        '_garniture': garniture_choisi
                    }
                    cursor.execute(garniture_id, parametres4)
                    print(garniture_choisi)
                    for ligne in cursor:
                        garniture_ID = ligne['id']
                    if garniture_choisi != "rien":
                        garniture_entre = "INSERT INTO pizza_garniture(pizza_id, garniture_id) VALUES(%(_pizza_id)s, %(_garniture_id)s)"
                        parametres5 = {
                            '_pizza_id': pizza_ID,
                            '_garniture_id': garniture_ID
                        }
                    cursor.execute(garniture_entre, parametres5)
                    connexion.commit()
                    print("Garniture enregistré!")
        print()
        client = "INSERT INTO clients(nom, numero_telephone, adresse_livraison, pizza_id) VALUES(%(_nom)s, %(_num)s, %(_adresse)s, %(_pizza)s);"
        parametres6 = {
            '_nom' : nom,
            '_num' : numero_telephone,
            '_adresse' : adresse,
            '_pizza' : pizza_ID
        }
        cursor.execute(client, parametres6)
        connexion.commit()
        # Plusieurs id de pizza pour un client car il peut avoir plusieurs pizza (Mais plusieurs pizza peuvent être la même à cause du nombre de garnitures)
        # Pour pouvoir sélectionner les garnitures qui se trouve dans la pizza
        # SELECT nom, pizza_id FROM clients JOIN pizza ON pizza.id = clients.pizza_id WHERE garniture_id IS NOT NULL
        print(nom)
        print(numero_telephone)
        # Si il y a une sauce
        pizza_client = "SELECT pizza.id, croute.nom AS croute, sauce.nom AS sauce, statut, GROUP_CONCAT(garniture.nom) AS garnitures FROM pizza JOIN clients ON pizza.id = clients.pizza_id JOIN pizza_garniture ON pizza_garniture.pizza_id = pizza.id LEFT JOIN garniture ON garniture.id = pizza_garniture.garniture_id LEFT JOIN croute ON croute.id = pizza.croute_id LEFT JOIN sauce ON sauce.id = pizza.sauce_id WHERE clients.nom = %(_nom)s AND clients.numero_telephone = %(_num)s GROUP BY pizza.id;"
        parametres7 = {
            '_nom': nom, 
            '_num': numero_telephone
        }
        
        cursor.execute(pizza_client, parametres7)
        pizzas = cursor.fetchall()
        print("Pizza: ", pizzas)
        # Le nom de tout! (Juste pour l'affichage)
        # id de la pizza reste le même
        # La croute et la sauce sont faciles à aller chercher:
        # Comment sélectionner les croutes et sauces qui sont coincé dans pizzas?
        


        return render_template('validation.html', pizza=pizzas)
    except mysql.connector.Error as erreur:
        print(erreur)
        return "Erreur!"
    finally:
        if cursor:
            cursor.close()
        if connexion:
            connexion.close()

@app.route("/livrer")
def liste():
    connexion = mysql.connector.connect(
            host = db_host,
            user = db_user,
            password = db_password,
            database = db_name,
            port = db_port
    )
    try:
        cursor = connexion.cursor(dictionary=True)
        liste_pizza = "SELECT adresse_livraison AS adresse, statut, croute.nom AS croute, sauce.nom AS sauce, GROUP_CONCAT(garniture.nom) AS garnitures FROM clients LEFT JOIN liste ON liste.id = clients.pizza_id LEFT JOIN croute ON croute.id = liste.croute_id LEFT JOIN sauce ON sauce.id = liste.sauce_id LEFT JOIN pizza_garniture ON pizza_garniture.pizza_id = liste.id LEFT JOIN garniture ON garniture.id = pizza_garniture.garniture_id GROUP BY clients.id, adresse_livraison, croute.nom, sauce.nom;"
        cursor.execute(liste_pizza)
        liste_pizza_complete = cursor.fetchall()
    except mysql.connector.Error as erreur:
            print(erreur)
            return "Erreur!"
    finally:
            if cursor:
                cursor.close()
            if connexion:
                connexion.close()
    
    return render_template("livrer.html", liste=liste_pizza_complete)

    

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 10:36:56 2020
@author: thomas
"""
from app import app
from flask import render_template
from flask import request
from flask import redirect
from flask import Markup
from flask import flash
import sqlite3
import json

session = ""
erreur = ""
app.secret_key = 'super secret key'
con = sqlite3.connect('database.db')
print ("Base de données ouverte avec succès")
try:
    con.execute('CREATE TABLE patients (numero TEXT, nom TEXT, prenom TEXT, date_n TEXT, lieu_n TEXT, adresse TEXT, telephone TEXT, mail TEXT, code_p TEXT, identifiant TEXT NOT NULL PRIMARY KEY, password TEXT NOT NULL)')
    con.commit()
except sqlite3.Error as er:
    print('SQLite error: %s' % (' '.join(er.args)))
try:
    con.execute('INSERT INTO patients (numero,nom,prenom,date_n,lieu_n,adresse,telephone,mail,code_p,identifiant,password) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (42, "test", "test", "test", "test", "test", "test", "test", "test", "test", "test"))
    con.commit()
except sqlite3.Error as er:
    print('SQLite error: %s' % (' '.join(er.args)))
try:
    con.execute('CREATE TABLE resultats_patients (identifiant TEXT NOT NULL, resultats TEXT NOT NULL PRIMARY KEY)')
    con.commit()
except sqlite3.Error as er:
    print('SQLite error: %s' % (' '.join(er.args)))
try:
    con.execute('INSERT INTO resultats_patients (identifiant,resultats) VALUES (?,?)', ("test", "../static/test/resultat_1.pdf"))
    con.commit()
    con.execute('INSERT INTO resultats_patients (identifiant,resultats) VALUES (?,?)', ("test", "../static/test/resultat_2.pdf"))
    con.commit()
    con.execute('INSERT INTO resultats_patients (identifiant,resultats) VALUES (?,?)', ("test", "../static/test/resultat_3.pdf"))
    con.commit()
    con.execute('INSERT INTO resultats_patients (identifiant,resultats) VALUES (?,?)', ("test", "../static/test/resultat_4.pdf"))
    con.commit()
    con.execute('INSERT INTO resultats_patients (identifiant,resultats) VALUES (?,?)', ("test", "../static/test/resultat_5.pdf"))
    con.commit()
except sqlite3.Error as er:
    print('SQLite error: %s' % (' '.join(er.args)))
con.close ()

@app.route('/', methods = ["POST", "GET"]) 
def init():
    #user={'surname':request.args.get('surname'),'name': request.args.get('name')}
    global erreur
    global session
    session = ""
    return render_template ('page_login.html', alert = erreur)

@app.route('/page_inscription', methods = ["POST", "GET"])
def page_inscription():
    global erreur
    return render_template('inscription.html', alert = erreur)

@app.route('/inscription', methods = ["POST"])
def inscription():
    global erreur
    numero = request.form.get('numero')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date_n = request.form.get('date_n')
    lieu_n = request.form.get('lieu_n')
    adresse = request.form.get('adresse')
    telephone = request.form.get('telephone')
    mail = request.form.get('mail')
    code_p = request.form.get('code_p')
    identifiant = request.form.get('identifiant')
    password = request.form.get('password')
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            con.execute('INSERT INTO patients (numero,nom,prenom,date_n,lieu_n,adresse,telephone,mail,code_p,identifiant,password) VALUES (?,?,?,?,?,?,?,?,?,?,?)', (numero, nom, prenom, date_n, lieu_n, adresse, telephone, mail, code_p, identifiant, password))
            con.commit()
            records = cur.fetchall()
            mdp = ""
            if (len(records) != 0) :
                resultats = records[0]
                mdp = resultats[0]
                print(mdp)
        con.close()
    except sqlite3.Error as er:
        erreur = "identifiant déjà existant (" + str(er) + ")"
        con.close()
        return redirect('/page_inscription')
    return redirect('/') 


@app.route('/info_user', methods = ["GET","POST"])
def info_user():
    global session
    numero = ""
    nom = ""
    prenom = ""
    date_n = ""
    lieu_n = ""
    adresse = ""
    telephone = ""
    mail = ""
    code_p = ""
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM patients WHERE identifiant = '" + session +"'")
            con.commit()
            records = cur.fetchall()[0]
            numero = records[0]
            nom = records[1]
            prenom = records[2]
            date_n = records[3]
            lieu_n = records[4]
            adresse = records[5]
            telephone = records[6]
            mail = records[7]
            code_p = records[8]      
            con.close()
            print(numero)
    except:
        print("error")    
    return render_template('info_user.html', numero = numero, nom = nom, prenom = prenom, date_n = date_n, lieu_n = lieu_n, adresse = adresse, telephone = telephone, mail = mail, code_p = code_p)  

@app.route('/informations', methods = ["GET","POST"])
def informations(): 
    return render_template('informations.html')


@app.route('/connexion', methods = ["GET","POST"])
def connexion(): 
    global erreur
    global session
    identifiant = request.form.get('identifiant')
    password = request.form.get('password')
    if (identifiant == None):
        identifiant = "test"
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT password FROM patients WHERE identifiant = '" + identifiant + "'")
        con.commit()
        records = cur.fetchall()
        mdp = ""
        if (len(records) != 0) :
            resultats = records[0]
            mdp = resultats[0]
            print(mdp)
    con.close()
    if (mdp == password) :
        erreur = ""
        session = identifiant
        return redirect('/informations')
    else :
        message = Markup("<h1>Voila! Platform is ready to used</h1>")
        flash(message) 
        erreur = "Erreur : identifiant et/ou mot de passe erroné(s)"
        return redirect('/')        


@app.route('/retour', methods = ["POST"])
def retour():
    global erreur
    erreur = ""
    return redirect('/')

@app.route('/modification', methods = ["POST"])
def modification():
    numero = request.form.get('numero')
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    date_n = request.form.get('date_n')
    lieu_n = request.form.get('lieu_n')
    adresse = request.form.get('adresse')
    telephone = request.form.get('telephone')
    mail = request.form.get('mail')
    code_p = request.form.get('code_p')
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("UPDATE patients SET numero = ?, nom = ?, prenom = ?, date_n = ?, lieu_n = ?, adresse = ?, telephone = ?, mail = ?, code_p = ? WHERE identifiant = '" + session +"'", (numero, nom, prenom, date_n, lieu_n, adresse, telephone, mail, code_p))
            con.commit()    
            con.close()
    except:
        print("error")
    return redirect('/info_user')

@app.route('/resultats', methods = ["POST", "GET"])
def resultats():
    global session
    liste = []
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("SELECT resultats FROM resultats_patients WHERE identifiant = '" + session + "'")
            records = cur.fetchall()
            for i in range (len(records)):
                liste.append(records[i][0])
            print(liste)
    except sqlite3.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
    con.close()
    return render_template('resultats.html', pdf=json.dumps(liste), nbfile=len(records))

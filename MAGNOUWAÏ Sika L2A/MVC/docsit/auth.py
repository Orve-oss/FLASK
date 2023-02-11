from flask import Blueprint, render_template, request, flash, redirect, url_for 
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from flask_login import login_user, login_required, logout_user, current_user



auth = Blueprint('auth', __name__)

@auth.route('/connexion', methods=['GET' ,'POST'])
def connexion():
    
    if request.method == 'POST':
       email = request.form.get('email')
       password = request.form.get('password')

       user = User.query.filter_by(email=email).first()
       if user: 
        if check_password_hash(user.password, password):
            flash('Vous êtes connecté!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.Accueil'))
        else:
            flash('Mot de passe incorrect!', category='error')
            return render_template("connexion.html", user=current_user)
            
       else:
        flash('L\'email n\'existe pas', category='error ')
        return render_template("connexion.html", user=current_user)
    else:
        return render_template("connexion.html", user=current_user)


@auth.route('/Deconnexion')
@login_required
def Deconnexion():
    logout_user()
    return redirect(url_for('auth.connexion'))


@auth.route('/Enregistrement', methods=['GET' ,'POST'])
def Enregistrement():
    if request.method == 'POST':
        email= request.form.get('email')
        nom = request.form.get('name')
        prenom = request.form.get('pre_nom')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('L\'email existe déjà!', category='error')
        elif len(email) < 4:
            flash('la taille de l\'email est trop petite. Au moins 4 caractères', category='error')
        elif len(nom) < 2:
            flash('la taille du nom est trop petite. Au moins 2 caractères', category='error')
        elif len(prenom) < 2:
            flash('la taille du prénom est trop petite. Au moins 2 caractères', category='error')
        elif len(password) < 7:
            flash('Au moins 7 caractères pour le mot de passe', category='error')
        else:
            new_user = User(email=email, nom=nom, prenom=prenom, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Vous avez été enregistrer avec succès', category='success')
            
            #ajouter l'utilisateur dans la db
            return redirect(url_for('views.login'))
 
    else:



        return render_template("Enregistrement.html", user=current_user)

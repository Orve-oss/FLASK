from flask import Blueprint, render_template,redirect
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/home')
@login_required 
def Accueil():
    return render_template("Accueil.html", user=current_user)


@views.route('/')
@login_required 
def login():
    return render_template("connexion.html", user=current_user)

@views.route('/login')
@login_required 
def logins():
    return render_template("connexion.html", user=current_user)



    
from flask import render_template, request, url_for, redirect, flash
from application import app, db, login_required
from application.tuotteet.models import Tuote
from application.hyllypaikat.models import Hyllypaikka
from application.tuotteet.forms import PoistoForm
from flask_login import login_required
from application.auth.models import Kayttaja
from application.hyllypaikat.models import Hyllypaikka

@app.route("/", methods=["POST", "GET"])
def index():
    # if == yläpalkin haku layoutissa
    if request.form.get("hakunappi") == "Etsi":

        hakusyote = request.form.get("hakukentta")

        if hakusyote:
            return kasittele_haku(hakusyote, request.form.get("hakutyyppi"))
        else:
            flash('hakukentta tyhjä')
            return render_template("index.html")

    else:
        return render_template("index.html")

@login_required
def kasittele_haku(hakusyote, hakutyyppi):
    
    if hakutyyppi == "tuote":
        tuote = Tuote.query.filter(Tuote.tuotekoodi == int(hakusyote)).first()
        if tuote:
            return render_template("/tuotteet/search.html", tuote=tuote, hyllypaikat=tuote.hyllypaikat, form = PoistoForm())
        else:
            flash('Tuotetta ei löytynyt')
            return render_template("index.html")
    
    elif hakutyyppi == "hyllypaikka":
        hyllypaikka = Hyllypaikka.query.filter(Hyllypaikka.paikkanumero == int(hakusyote)).first()
        if hyllypaikka:
            return redirect(url_for('nayta_hyllypaikka', paikkanumero = hyllypaikka.paikkanumero))
        else:
            flash('Hyllypaikkaa ei löytynyt')
            return render_template("index.html")

    else:
        flash('Et valinnut hakutyyppiä (Tuote tai Hyllypaikka)')
        return render_template("index.html")

@app.route("/tilasto", methods=["GET"])
@login_required
def tilasto_nakyma():

    # 5 työntekijää joilla eniten lokeja viikon aikana
    tyontekijat = Kayttaja.ahkerimmat_tyontekijat()

    # hyllypaikkojen määrä osastoittain ja osaston %-osuus kaikista hyllypaikoista
    osastot = Hyllypaikka.osasto_tilastot()

    return render_template("tilastot/tilasto.html", tyontekijat = tyontekijat, osastot = osastot)
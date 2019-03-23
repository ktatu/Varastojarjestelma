from application import app, db
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.sql.expression import exists
from application.tuotteet.models import Tuote
 
app.secret_key = 'salainen_avain'

@app.route("/tuotteet/new")
def tuotteet_form(tuotekoodi):
    return render_template("tuotteet/new.html", koodi=tuotekoodi)

@app.route("/tuotteet", methods=["POST"])
def tuotteet_create():

    t = Tuote(request.form.get("tuotekoodi"), request.form.get("nimi"),
    request.form.get("maara"), request.form.get("kategoria"), 
    request.form.get("kuvaus"))

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("tuotteet_mainpage"))


@app.route("/tuotteet", methods=["GET"])
def tuotteet_index():
    return render_template("tuotteet/list.html", tuotteet = Tuote.query.all())

@app.route("/tuotteet/main")
def tuotteet_mainpage():
    return render_template("tuotteet/main.html")

@app.route("/tuotteet/main", methods=["POST"])
def tuotteet_search():

    # tuotehaku
    if request.form["nappi"] == "Hae tuotetta":
        koodi = request.form.get("tuotekoodi")

        #workaround-ratkaisu, sama query kahdesti
        tuote = db.session().query(Tuote).filter(Tuote.tuotekoodi==koodi).first()

        if tuote:
            return render_template("tuotteet/search.html", tuote1 = db.session().query(Tuote).filter(Tuote.tuotekoodi==koodi))

        else:
            flash('Tuotetta ' + str(koodi) + ' ei ole varastossa')
            return redirect(url_for('tuotteet_mainpage'))

    # tuotelisäys
    elif request.form["nappi"] == "Lisää uusi tuote":
        koodi = request.form.get("tuotekoodi")

        tuote = db.session().query(Tuote).filter(Tuote.tuotekoodi == koodi).first()

        if tuote:
            flash('Tuote ei ole uusi, tee saldopäivitys')
            return redirect(url_for("tuotteet_mainpage"))
        else:
            return tuotteet_form(koodi)

    # saldopäivitys
    else:
        tuote = db.session().query(Tuote).filter(Tuote.tuotekoodi == request.form.get("tuotekoodi")).first()


        #todo: sijoitetaan entiselle hyllypaikalle jos kapasiteetti sallii. jos ei, niin ohjataan valitsemaan uusi paikka
        # sijoitus uudessa näkymässä commitin jälkeen
        if tuote:

            lisattava = request.form.get("lisays")

            if (int(lisattava) <= 0):
                flash('Virheellinen lisäys: yritit lisätä saldoon ' + lisattava)
                return redirect(url_for("tuotteet_mainpage"))

            koodi = tuote.tuotekoodi
            
            tuote.maara = tuote.maara + int(lisattava)
            db.session().commit()

            flash('Tuotteeseen ' + str(koodi) + ' lisätty ' + lisattava)

        else:
            flash('Tuotetta ' + request.form.get("tuotekoodi") + ' ei ole varastossa')


        return redirect(url_for("tuotteet_mainpage"))



from flask import Flask, render_template, request, url_for, get_flashed_messages, redirect, flash
from startup_setup import Startup, Founder, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///startup.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def showStartups():
    startups = session.query(Startup).all()
    return render_template("index.html", startups=startups)


@app.route('/new', methods=['GET', 'POST'])
def newStartup():
    if request.method == "POST":
        session.add(Startup(name=request.form["name"]))
        session.commit()
        startup = session.query(Startup).filter_by(name=request.form["name"]).one()
        return redirect(url_for("showStartup", startup_id=startup.id))
    return render_template("startups/new.html")


@app.route("/<int:startup_id>/edit", methods=['GET', 'POST'])
def editStartup(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    if request.method == "POST":
        startup.name = request.form["name"]
        session.add(startup)
        session.commit()
        return redirect(url_for("showStartup", startup_id=startup_id))
    return render_template("startups/edit.html", startup=startup)


@app.route("/<int:startup_id>/delete", methods=['GET', 'POST'])
def deleteStartup(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    if request.method == "POST":
        session.delete(startup)
        session.commit()
        return redirect(url_for("showStartups"))
    return render_template("startups/delete.html", startup=startup)


@app.route("/<int:startup_id>/show")
def showStartup(startup_id):
    startup = session.query(Startup).filter_by(id=startup_id).one()
    founders = session.query(Founder).filter_by(startup_id=startup_id).all()
    return render_template("startups/show.html", startup=startup, founders=founders)


@app.route("/<int:startup_id>/founders/new", methods=['POST'])
def addFounder(startup_id):
    session.add(Founder(name=request.form["name"], bio=request.form["bio"], startup_id=startup_id))
    session.commit()
    return redirect(url_for("showStartup", startup_id=startup_id))


@app.route("/<int:startup_id>/founders/<int:founder_id>/delete", methods=['GET', 'POST'])
def deleteFounder(startup_id, founder_id):
    founder = session.query(Founder).filter_by(startup_id=startup_id, id=founder_id).one()
    startup = session.query(Startup).filter_by(id=startup_id).one()
    if request.method == 'POST':
        session.delete(founder)
        session.commit()
        return redirect(url_for("showStartup", startup_id=startup_id))
    return render_template("founders/delete.html", founder=founder, startup=startup)


@app.route("/<int:startup_id>/founders/<int:founder_id>/edit", methods=['GET', 'POST'])
def editFounder(startup_id, founder_id):
    founder = session.query(Founder).filter_by(startup_id=startup_id, id=founder_id).one()
    startup = session.query(Startup).filter_by(id=startup_id).one()
    if request.method == 'POST':
        founder.name = request.form["name"]
        founder.bio = request.form["bio"]
        session.add(founder)
        session.commit()
        return redirect(url_for("showStartup", startup_id=startup_id))
    return render_template("founders/edit.html", founder=founder, startup= startup)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000')

from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
import os
from werkzeug.security import check_password_hash
from helpers import apology, login_required
from forms import aanpassen_eten_form, aanpassen_mo_form


app = Flask(__name__)
app.secret_key = os.urandom(24)


# database verbinding
def get_db_connection():
  conn = sqlite3.connect('database.db')
  conn.row_factory = sqlite3.Row
  return conn


# rows als dictionary ophalen
def get_items(sql, params=()):
  conn = get_db_connection()
  cursor = conn.cursor()
 
  cursor.execute(sql, params)
  rows = cursor.fetchall()


  cursor.close()
  conn.close()
  return [dict(row) for row in rows]


# row als dictionary ophalen
def get_one_item(sql, params=()):
  conn = get_db_connection()
  cursor = conn.cursor()
 
  cursor.execute(sql, params)
  row = cursor.fetchone()


  cursor.close()
  conn.close()
  return dict(row) if row else None


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/zoek", methods=["POST"])
def zoek():
  gezocht = request.form.get("gezocht")


  resultaten_eten = get_items("SELECT * FROM eten WHERE naam LIKE ?", (f"%{gezocht}%",))


  resultaten_mo = get_items("SELECT * FROM mo WHERE naam LIKE ?", (f"%{gezocht}%",))


  return render_template("zoek.html",
      zoekresultaten_eten = resultaten_eten,
      zoekresultaten_mo = resultaten_mo,
      zoekterm = gezocht
  )


@app.route("/producten")
def producten():
   info_eten = get_items("SELECT * FROM eten order by naam")
   return render_template("producten.html", eten=info_eten)


@app.route("/eten/<int:id>")
def detail_eten(id):
  info_eten = get_one_item("SELECT * FROM eten WHERE id = ?", (id,))
  if not info_eten:
      return apology(f"Product met id {id} niet gevonden", 404)
 
  sql = """
  SELECT mo.*
  FROM mo
  JOIN mo_met_eten ON mo.id = mo_met_eten.mo_id
  WHERE mo_met_eten.eten_id = ?
  """
  info_mo = get_items(sql, (id,))


  return render_template("product_info.html",
                         eten = info_eten,
                         mo = info_mo)


@app.route("/mo")
def mo():
   info_mo = get_items("SELECT * FROM mo order by naam")
   return render_template("mo.html", mo=info_mo)


@app.route("/mo/<int:id>")
def detail_mo(id):
   info_mo = get_one_item("SELECT * FROM mo WHERE id = ?", (id,))
   if not info_mo:
      return apology(f"Micro-organisme met id {id} niet gevonden", 404)


   sql = """
   SELECT eten.*
   FROM eten
   JOIN mo_met_eten ON eten.id = mo_met_eten.eten_id
   WHERE mo_met_eten.mo_id = ?
   """
   info_eten = get_items(sql, (id,))


   return render_template("mo_info.html",
                         eten = info_eten,
                         mo = info_mo)


@app.template_filter("risk_color")
def risk_color(level):
   mapping = {
       "hoog": "bg-danger",
       "middel": "bg-warning text-dark",
       "laag": "bg-success"
   }
   return mapping.get(level.lower(), "bg-secondary")


@app.route("/inlog", methods=["GET", "POST"])
def login():
  """Log user in"""

  # Forget any user_id
  session.clear()

  if request.method == "POST":

      # Check of gebruikersnaam is ingevuld
      if not request.form.get("username"):
          return apology("must provide username", 403)

      # Check of wachtwoord is ingevuld
      elif not request.form.get("password"):
          return apology("must provide password", 403)




      conn = get_db_connection()
      cursor = conn.cursor()
      # Query database voor de gebruiker
      cursor.execute(
          "SELECT * FROM inlog WHERE gebruikersnaam = ?",
          (request.form.get("username"),)
      )
      rows = cursor.fetchall()




      # Controleer of gebruiker bestaat en wachtwoord correct is
      if len(rows) != 1 or not check_password_hash(
          rows[0]["wachtwoord"], request.form.get("password")
      ):
          return apology("invalid username and/or password", 403)




      # Onthoud ingelogde gebruiker
      session["user_id"] = rows[0]["id"]
      conn.close()


      # Redirect naar info toevoegen pagina
      return redirect("aanpassen")




  else:
      # GET: laat login-formulier zien
      return render_template("inlog.html")






@app.route('/aanpassen', methods=['GET', 'POST'])
@login_required
def aanpassen():
  eten_form = aanpassen_eten_form(prefix='eten')
  mo_form = aanpassen_mo_form(prefix='mo')




  if eten_form.validate_on_submit() and eten_form.submit.data:
      conn = get_db_connection()
      cursor = conn.cursor()
      try:
          cursor.execute("""INSERT INTO eten (naam, categorie) VALUES (?, ?)""", (eten_form.naam.data, eten_form.categorie.data))
          conn.commit()
          conn.close()
          return redirect(url_for('producten'))
      except sqlite3.IntegrityError:
          conn.close()
          return apology('Deze naam bestaat al!', 403)




  if mo_form.validate_on_submit() and mo_form.submit.data:
      conn = get_db_connection()
      cursor = conn.cursor()
      try:
          cursor.execute("""
              INSERT INTO mo (naam, herkenning, risiconiveau, actie, symptomen, beschrijving)
              VALUES (?, ?, ?, ?, ?, ?)
          """, (mo_form.naam.data, mo_form.herkenning.data, mo_form.risiconiveau.data, mo_form.actie.data, mo_form.symptomen.data, mo_form.beschrijving.data))
          conn.commit()
          conn.close()
          return redirect(url_for('mo'))
      except sqlite3.IntegrityError:
          conn.close()
          return apology('Deze naam bestaat al!', 403)
  return render_template('aanpassen.html', eten_form=eten_form, mo_form=mo_form)


@app.route("/logout")
def logout():
 """Log user out"""








 # Forget any user_id
 session.clear()








 # Redirect user to login form
 return redirect("/")




if __name__ == "__main__":
  app.run(debug=True)










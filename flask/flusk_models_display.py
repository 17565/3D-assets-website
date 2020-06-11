from flask import Flask, g, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "static/3dmodel.db"

#access database
def get_db():
    db = getattr(g,'database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#closes connetion
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.close()

#displays data
@app.route("/")
def home():
    cursor = get_db().cursor() 
    sql = "SELECT * FROM models"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("test_index.html" , results=results)

#uploads 3D models
@app.route('/upload/')
def upload():
    return

#runs app
if __name__ == "__main__":
    app.run(debug=True)
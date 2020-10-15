from flask import Flask, g, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "3dmodel.db"

#access database
def get_db():
    db = getattr(g,'database', None)
    if db is None:
        db = g.database = sqlite3.connect(DATABASE)
    return db

#closes connetion
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.close()

#displays home page
@app.route("/")
def home():
    return render_template("home_page.html")

#displays data
@app.route("/data")
def data():
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM models"
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template("model_page.html" , results=results)

#dispaly model on indivigual page
@app.route("/model/<int:id>")
def model(id):
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * frOM models WHERE id = ?"
    cursor.execute(sql,(id,))
    result = cursor.fetchone()
    return render_template("1_model.html" , result=result)

#uploads 3D models
@app.route('/upload/')
def upload():
    return

#displays feedback page
@app.route("/feedback")
def feedback():
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM comments"
    cursor.execute(sql)
    comments = cursor.fetchall()
    conn = get_db()
    cursor = conn.cursor()
    sql = "SELECT * FROM models"
    cursor.execute(sql)
    models = cursor.fetchall()
    return render_template("comments_and_feedback_page.html", comments=comments, models=models)

#adds item to database
@app.route("/add", methods=["POST"])
def add():
    if request.method == "POST":
        conn = get_db()
        cursor = conn.cursor()
        comment_1 = request.form["comment"]
        id = request.form["model"]
        sql = "INSERT INTO comments(comment, related_model) VALUES (?,?)"
        cursor.execute(sql,( comment_1, id))
        conn.commit()
    return redirect("/feedback")

#delete items from database
@app.route("/delete",methods=["POST"])
def delete():
    if request.method =="POST":
        conn = get_db()
        cursor = conn.cursor()
        id = int(request.form["comment"])
        sql = "DELETE FROM comments WHERE id = ?"
        cursor.execute(sql,(id,))
        conn.commit()
    return redirect("/feedback")

#runs app
if __name__ == "__main__":
    app.run(debug=True)
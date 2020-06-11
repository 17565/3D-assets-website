from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return ("hello, world!")
#    return render_template("index.html",data = "ball_web_test.x3d")

if __name__ == "__main__":
    app.run(debug=True)
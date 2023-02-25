from flask import Flask, render_template, url_for, flash, redirect, Response
app = Flask(__name__)
app.secret_key = "akanksha"

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
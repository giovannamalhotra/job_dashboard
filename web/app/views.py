from app import app
from flask import render_template

#@app.route('/')
@app.route('/index')
#@app.route('/email')

def index():
  #return "Hello, World!"
  user = { 'nickname': 'Giovanna' } #fake user
  mylist = [1,2,3,4]
  #return render_template("index.html", title = 'Home', user = user, mylist = mylist)
  return render_template("index.html")

def email():
  return render_template("base.html") 

from flask import Flask, render_template
from .helpers import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/installUpdate/<int:updateno>',methods = ["POST"])
def install_update(updateno):
    if request.method == 'POST':
        # get the update number and pass to the handler
        install_update(updateno)
    else:
        return "Invalid request"

@app.route('/removeUpdate/<int:updateno>',methods = ["POST"])
def remove_update(updateno):
    if request.method == 'POST':
        # get the update number and pass to the handler
        update_number = ""
        remove_update(updateno)
    else:
        return "Invalid request"


if __name__ == '__main__':
   app.run()

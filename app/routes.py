from flask import render_template, request, redirect, url_for
from app import app, models, testcase

@app.route('/')
def index():
    testcases = testcase.TestCase.get_test_cases()
    return render_template('main.html', testcases=testcases)


@app.route('/testcases')
def test_cases():
    testcases = testcase.TestCase.get_test_cases()
    return render_template('/testcases/list.html', testcases=testcases)


@app.route('/testcases/new', methods=['GET', 'POST'])
def new_test_case():
    if request.method == 'GET':
        return render_template('/testcases/new.html')
    elif request.method == 'POST':
        testcase.TestCase.add_test_case(request)
        return redirect(url_for('test_cases'))

@app.route('/installUpdate/<int:updateno>', methods = ["POST"])
def install_update(updateno):
    if request.method == 'POST':
        # get the update number and pass to the handler
        install_update(updateno)
    else:
        return "Invalid request"

@app.route('/removeUpdate/<int:updateno>', methods = ["POST"])
def remove_update(updateno):
    if request.method == 'POST':
        # get the update number and pass to the handler
        update_number = ""
        remove_update(updateno)
    else:
        return "Invalid request"
from flask import render_template, request, redirect, url_for
from app import app, models, testcase

@app.route('/')
def index():
    testcases = testcase.TestCase.get_testcases()
    return render_template('main.html', testcases=testcases)


@app.route('/testcases')
def testcases():
    testcases = testcase.TestCase.get_testcases()
    return render_template('/testcases/list.html', testcases=testcases)


@app.route('/testcases/new', methods=['GET', 'POST'])
def new_testcase():
    if request.method == 'GET':
        return render_template('/testcases/new.html')
    elif request.method == 'POST':
        testcase.TestCase.add_testcase(request)
        return redirect(url_for('index'))


@app.route('/testcases/delete/<int:tcid>')
def delete_testcase(tcid):
    testcase.TestCase.delete_testcase(tcid)
    return redirect(url_for('testcases'))


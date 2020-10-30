from flask import render_template, request, redirect, url_for
from app import app, models, testcase

tc = testcase.TestCase()

@app.route('/')
def index():
    activerun = tc.active
    queued = tc.get_queue()
    testruns = tc.get_runs()
    testcases = tc.get_testcases()

    return render_template('main.html', active=activerun,
                            queued=queued,
                            testcases=testcases,
                            testruns=testruns)


@app.route('/testcases')
def testcases():
    testcases = tc.get_testcases()
    return render_template('/testcases/list.html', testcases=testcases)


@app.route('/testcases/new', methods=['GET', 'POST'])
def new_testcase():
    if request.method == 'GET':
        return render_template('/testcases/new.html')
    elif request.method == 'POST':
        tc.add_testcase(request)
        return redirect(url_for('index'))


@app.route('/testcases/delete/<int:tcid>')
def delete_testcase(tcid):
    tc.delete_testcase(tcid)
    return redirect(url_for('testcases'))


@app.route('/testcases/run', methods=['GET', 'POST'])
def run_testcase():
    if request.method == 'GET':
        return redirect(url_for('index'))
    elif request.method == 'POST':
        tc.run_testcase(request)
        return redirect(url_for('index'))
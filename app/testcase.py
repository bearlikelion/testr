import json
import os

from flask import flash
from sqlalchemy.sql.expression import cast
from app import config, cs, db, machine, models, log

class TestCase:
    def add_testcase(self, request):
        testcase = models.TestCase(
            number = request.form['number'],
            name = request.form['name'],
            inputs = request.form['inputs']
        )

        db.session.add(testcase)
        db.session.commit()
        log.info("Added Test Case %s" % request.form['number'])
        flash('Test Case %s added' % request.form['number'], 'success')


    def get_testcase(self, tcnumber):
        return models.TestCase.query.filter_by(number=tcnumber).scalar()


    def get_testcases(self):
        return models.TestCase.query.all()


    def delete_testcase(self, tcid):
        models.TestCase.query.filter_by(id=tcid).delete()
        db.session.commit()
        log.info("Deleted Test Case %s" % tcid)
        flash('Deleted Test case %s' % tcid, 'success')


    def generate_tc_json(self, testrun, email, tcnumbers):
        testcase = {}
        testcase['commcell'] = {
            "webconsoleHostname": config['cshostname'],
            "commcellUsername": config['username'],
            "commcellPassword": config['password']
        }

        testcase['email'] = {
            "receiver": email
        }

        testcase['testCasesInfo'] = {
            "UpdateQA": 'false',
            "ParallelExecution": 'false',
        }

        testcase['testCasesInfo']["testCases"] = {}

        for tcnum in tcnumbers:
            _testCase = self.get_testcase(tcnum)
            testcase['testCasesInfo']["testCases"][_testCase.number] = json.loads(_testCase.inputs)

        jsonpath = "." + os.sep + 'tmp' + os.sep + 'testrun-' + str(testrun.id) + '.json'
        with open(jsonpath, 'a+') as outfile:
            json.dump(testcase, outfile, indent=2, separators=(',', ':'))
            log.info("Generated JSON File: %s" % jsonpath)
            return jsonpath


    def run_testcase(self, request):
        email = request.form['email']
        testcases = request.form.getlist('testcase')
        testrun = models.TestRun()
        db.session.add(testrun)
        db.session.commit()
        log.info("Created new test run %s" % testrun.id)
        jsonFile = self.generate_tc_json(testrun, email, testcases)

        # TODO: Threaded pyton CVAutomation.py --inputJSON json

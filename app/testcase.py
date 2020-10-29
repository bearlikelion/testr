import json, os, threading, subprocess

from re import search
from flask import flash
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
            "receiver": email,
            "subject": 'Testr [' + cs.commserv_hostname + ':'
                        + str(cs.commserv_version) + ']: Test Run ' + str(testrun.id)
        }

        testcase['testCasesInfo'] = {
            "UpdateQA": 'false',
            "ParallelExecution": 'false',
        }

        testcase['testCasesInfo']["testCases"] = {}

        for tcnum in tcnumbers:
            _testCase = self.get_testcase(tcnum)
            testcase['testCasesInfo']["testCases"][_testCase.number] = json.loads(_testCase.inputs)

        path = os.path.abspath(os.getcwd())
        jsonpath = path + os.sep + 'tmp' + os.sep + 'testrun-' + str(testrun.id) + '.json'
        with open(jsonpath, 'a+') as outfile:
            json.dump(testcase, outfile, indent=2, separators=(',', ':'))
            log.info("Generated JSON File: %s" % jsonpath)
            return jsonpath


    def execute_testcase(self, testrun, jsonFile):
        install_dir = cs.commserv_client.install_directory
        cvautomation = install_dir + os.sep + 'Automation' + os.sep + 'CVAutomation.py'
        automation_log_file = cs.commserv_client.log_directory + os.sep + 'Automation' + os.sep + 'Automation.log'

        log.info('Executing Test Run %s' % testrun.id)
        subprocess.call(['python', cvautomation, '--inputJSON', jsonFile], shell=True)

        automation_log = machine.read_file(automation_log_file)
        with open(automation_log_file) as f:
            for line in f:
                pass
            last_line = line

        pid = last_line.split('  ')[0]
        pid_log = search(pid, automation_log)

        if "[FAILED]." in pid_log.string:
            testrun.result = -1
            db.session.commit()
            log.error('Test Run Failed')
        elif "[PASSED]." in pid_log.string:
            testrun.result = 1
            db.session.commit()
            log.info('Test Run Passed')

        log.info('Test Run %s Finished' % testrun.id)


    def run_testcase(self, request):
        email = request.form['email']
        testcases = request.form.getlist('testcase')
        testrun = models.TestRun()
        db.session.add(testrun)
        db.session.commit()
        log.info("Created new test run %s" % testrun.id)
        jsonFile = self.generate_tc_json(testrun, email, testcases)

        # TODO: Threaded pyton CVAutomation.py --inputJSON json
        tcrun = threading.Thread(target=self.execute_testcase, args=(testrun, jsonFile))
        tcrun.start()
        flash('Started Test Run %s' % testrun.id, 'success')

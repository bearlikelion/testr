from flask import flash
from app import cs, db, models, log

class TestCase:
    def add_testcase(request):
        testcase = models.TestCase(
            number = request.form['number'],
            name = request.form['name'],
            inputs = request.form['inputs']
        )

        db.session.add(testcase)
        db.session.commit()
        log.info("Added Test Case %s" % request.form['number'])
        flash('Test Case %s added' % request.form['number'], 'success')

    def get_testcases():
        return models.TestCase.query.all()

    def delete_testcase(tcid):
        models.TestCase.query.filter_by(id=tcid).delete()
        db.session.commit()
        log.info("Deleted Test Case %s" % tcid)
        flash('Deleted Test case %s' % tcid, 'success')
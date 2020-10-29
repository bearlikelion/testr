from flask import flash
from app import cs, db, models

class TestCase:
    def add_test_case(request):
        testcase = models.TestCase(
            number = request.form['number'],
            name = request.form['name'],
            inputs = request.form['inputs']
        )

        db.session.add(testcase)
        db.session.commit()
        flash('Test Case %s added' % request.form['number'], 'success')

    def get_test_cases():
        return models.TestCase.query.all()
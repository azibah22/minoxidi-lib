from flask import Flask, render_template_string, request, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'
csrf = CSRFProtect(app)

class TestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/test-csrf', methods=['GET', 'POST'])
def test_csrf():
    form = TestForm()
    if form.validate_on_submit():
        flash(f'Hello, {form.name.data}!')
    elif request.method == 'POST':
        flash('CSRF failed or name missing!')
    return render_template_string('''
        <!doctype html>
        <title>CSRF Test</title>
        <h2>CSRF Test Form</h2>
        <form method="post">
            {{ form.hidden_tag() }}
            {{ form.name.label }} {{ form.name() }}<br><br>
            {{ form.submit() }}
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
            {% for message in messages %}
              <li>{{ message }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
    ''', form=form)

if __name__ == '__main__':
    app.run(debug=True) 
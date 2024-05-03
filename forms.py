from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField 
from wtforms.validators import DataRequired, Length


class TodoForm(FlaskForm):
	title = StringField('Type an item:', validators=[DataRequired()])
	submit = SubmitField('Add item')





class UpdateTodoForm(FlaskForm):
	title = StringField('Type an item:', validators=[DataRequired()])
	submit = SubmitField('Update Item')
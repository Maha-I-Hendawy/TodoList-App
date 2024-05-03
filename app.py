from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from forms import TodoForm, UpdateTodoForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '43d07b3e76ab6240e940ee6c8ea12321'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todolist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
app.app_context().push()

ma = Marshmallow(app)


class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.Text, nullable=False)


	def __repr__(self):
		return f"Todo('{self.title}')"




class TodoSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Todo




todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)



db.create_all()



@app.route('/', methods=['GET', 'POST'])
def index():
	form = TodoForm()
	if form.validate_on_submit():
		new_todo = Todo(title=form.title.data)
		db.session.add(new_todo)
		db.session.commit()
		return redirect(request.url)
	elif request.method == 'GET':
		todos = Todo.query.all()
	return render_template('index.html',form=form, todos=todos)
	
@app.route('/todo/<int:todo_id>')
def one_todo(todo_id):
	todo = Todo.query.get_or_404(todo_id)

	return render_template('todo.html', todo=todo)



@app.route('/todo/<int:todo_id>/update', methods=['GET', 'POST'])
def update_todo(todo_id):
	todo = Todo.query.get_or_404(todo_id)
	form = UpdateTodoForm()
	if form.validate_on_submit():
		todo.title = form.title.data
		db.session.commit()
		return redirect(url_for('index'))

	elif request.method == 'GET':
		form.title.data = todo.title

	return render_template('update_todo.html', form=form)

@app.route('/todo/<int:todo_id>/delete', methods=['GET', 'POST'])
def delete_todo(todo_id):
	todo = Todo.query.get_or_404(todo_id)
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for('index'))



if __name__ == '__main__':
	app.run(debug=True)
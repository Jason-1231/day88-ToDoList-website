from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)


class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250), nullable=True)
    date_added = db.Column(db.DateTime(120), nullable=True, default=datetime.datetime.now().date())

    def __repr__(self):
        return f"<Task {self.id}>"


class Task:
    def __init__(self):
        self.date = datetime.datetime.now().date()
        self.task_name = None


db.create_all()


@app.route("/")
def home():
    all_todos = Todos.query.all()
    return render_template('index.html', todos=all_todos)


@app.route("/addtask", methods=["POST"])
def add_task():
    new_todo = Todos(description=request.form.get('add_task'))
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/delete/<task_id>", methods=["DELETE", "POST"])
def delete_task(task_id):
    task_to_delete = Todos.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)

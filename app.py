from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Todo.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres:grespost@localhost:5432/Todo"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return f"{self.srno} - {self.title}"

@app.route('/',methods = ['GET','POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title = title,desc = desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html",allTodo = allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return f"This is products page"

@app.route('/update/<int:srno>',methods = ['GET','POST'])
def update(srno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        record = Todo.query.filter_by(srno=srno).first()
        record.title = title
        record.desc = desc
        db.session.commit()
        return redirect('/')
    
    record = Todo.query.filter_by(srno=srno).first()
    return render_template('update.html',record = record)

@app.route('/delete/<int:srno>')
def delete(srno):
    record = Todo.query.filter_by(srno=srno).first()
    db.session.delete(record)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
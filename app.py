from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.Title}"


@app.route('/', methods = ["GET", "POST"])
def hello_world():
    if request.method == "POST":
        Title = request.form["Title"]
        desc = request.form["desc"]
        todo=Todo(Title = Title, desc=desc)
        db.session.add(todo)
        db.session.commit()
   
    alltodo = Todo.query.all()

    return render_template("index.html", alltodo=alltodo)

@app.route('/products')
def producs():
    alltodo = Todo.query.all()
    print(alltodo)
    return 'This is a products end point!'

@app.route('/update/<int:sno>', methods = ["GET", "POST"])
def update(sno):
    if request.method == "POST":
        Title = request.form["Title"]
        desc = request.form["desc"]
        todo = Todo.query.filter_by(sno=sno).first()
        todo.Title=Title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo=todo )

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

  

if __name__ == "__main__":
    app.run(debug=True, port=8000)  #debug=True : To see error in browser itself
     
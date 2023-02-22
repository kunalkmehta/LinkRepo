from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///link_list.db"
db = SQLAlchemy()
db.init_app(app)

class link_list(db.Model):
    link_id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(100), nullable = True)
    title = db.Column(db.String(200), nullable = True)
    link = db.Column(db.String(500), nullable = True)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.title} - {self.link}"
    
with app.app_context():
    db.create_all()

@app.route("/", methods = ['GET', 'POST'])
def hello_world():

    if request.method == 'POST':
        category = title = request.form['category']
        title = request.form['title']
        link = request.form['link']
        rec_list = link_list (category = category, title = title, link = link)
        db.session.add(rec_list)
        db.session.commit()

    all_links = link_list.query.all()
    #print(all_links)
    return render_template('index.html', all_links = all_links)

    #return "<p>Hello, World!</p>"

@app.route("/about")
def about():
    return "<p>This is About me page</p>"

@app.route("/show")
def show_all():
    all_links = link_list.query.all()
    print(all_links)

    return "<p>Hello, Show!</p>"

@app.route("/update/<int:link_id>", methods = ['GET', 'POST'])
def update(link_id):
    if request.method == 'POST':
        link_select = db.get_or_404(link_list, link_id)
        link_select.category = title = request.form['category']
        link_select.title = request.form['title']
        link_select.link = request.form['link']
        db.session.commit()
        return redirect("/")
    link_select = db.get_or_404(link_list, link_id)
    return render_template('update.html', link_select = link_select)


@app.route("/delete/<int:link_id>")
def delete(link_id):
    link_select = db.get_or_404(link_list, link_id)
    db.session.delete(link_select)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run(debug = True)

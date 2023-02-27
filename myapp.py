from flask import Flask, render_template, request, redirect, jsonify
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

@app.route("/getinfo/title/<string:s>")
def getTitle(s):

    filter_list = link_list.query.filter_by(title=s).all()
    #filter_list = db.session.query(link_list).filter_by(title='Prime').all()
    if len (filter_list) == 0:
        return "<p>No value exist</p>"
    else: 
        for i in range(len(filter_list)):
            title = filter_list[i].title
            category = filter_list[i].category
            link = filter_list[i].link

            result = {
                'Title': title,
                'Category': category,
                'Link': link
            }

    #return jsonify (filter_list)
    #return render_template('test.html', filter_list = filter_list)
    return jsonify(result)

@app.route("/getinfo/category/<string:s>")
def getCategory(s):
    result_list = []
    filter_list = link_list.query.filter_by(category=s).all()
    #filter_list = db.session.query(link_list).filter_by(title='Prime').all()
    if len (filter_list) == 0:
        return "<p>No value exist</p>"
    else: 
        for i in range(len(filter_list)):
            title = filter_list[i].title
            category = filter_list[i].category
            link = filter_list[i].link

            result = {
                'Title': title,
                'Category': category,
                'Link': link
            }
            result_list.append(result)
    #return jsonify (filter_list)
    #return render_template('test.html', filter_list = filter_list)
    return jsonify(result_list)



@app.route("/show")
def show_all():
    all_links = link_list.query.all()
    print(all_links)

    return "<p>Hello, Show!</p>"

@app.route("/update/<int:link_id>", methods = ['GET', 'POST'])
def update(link_id):
    if request.method == 'POST':
        link_select = db.get_or_404(link_list, link_id)
        link_select.category = request.form['category']
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

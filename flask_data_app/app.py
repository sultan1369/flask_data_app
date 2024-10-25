from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Data {self.name}>'

@app.route('/')
def index():
    data_list = Data.query.all()
    return render_template('index.html', data_list=data_list)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        new_data = Data(name=name)
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    data = Data.query.get_or_404(id)
    if request.method == 'POST':
        data.name = request.form['name']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', data=data)

@app.route('/delete/<int:id>')
def delete(id):
    data = Data.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():  # Use application context here
        db.create_all()  # Create database and tables
    app.run(debug=True)

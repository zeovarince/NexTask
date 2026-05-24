from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Konfigurasi Database SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nextask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Database untuk Kanban
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='todo') # Status: todo, inprogress, done

# Generate database otomatis
with app.app_context():
    db.create_all()

# READ: Halaman Dashboard Board
@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

# CREATE: Pindah halaman form tambah task
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        status = request.form['status']
        
        new_task = Task(title=title, description=description, status=status)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('tambah_task.html')

# UPDATE: Pindah halaman form edit detail
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    task = Task.query.get_or_404(id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.status = request.form['status']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', task=task)

# UPDATE CEPAT: Geser task antar kolom Kanban
@app.route('/move/<int:id>/<string:new_status>')
def move_status(id, new_status):
    task = Task.query.get_or_404(id)
    if new_status in ['todo', 'inprogress', 'done']:
        task.status = new_status
        db.session.commit()
    return redirect(url_for('index'))

# DELETE: Hapus task
@app.route('/hapus/<int:id>')
def hapus(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
from Demos.win32ts_logoff_disconnected import username
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3 as sq
app =Flask(__name__)
app.secret_key = "supersecret"
def init_db():
    conn=sq.connect('todo.db')
    cur=conn.cursor()
    cur.execute('''
    create table if not exists tasks
    (
    id integer primary key autoincrement,
    task text not null,
    status text not null,
    time_added timestamp default current_timestamp,
    time_updated timestamp ,
    time_done timestamp,
    priority text default 'medium'
    )
    ''')
    try:
        cur.execute('''
    alter table tasks add column user_id integer references user(id)
    ''')
    except sq.OperationalError:
        pass
    cur.execute('''
        create table if not exists users
        (
        id integer primary key autoincrement,
        username text unique not null,
        password text not null
        )
        ''')
    conn.commit()
    conn.close()

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        conn=sq.connect('todo.db')
        cur=conn.cursor()
        try:
            cur.execute('''
            insert into users (username, password) values(?,?)''',(username,generate_password_hash(password)))
            flash("Account created", "success")
        except:
            flash("Account already exists.", "danger")
        conn.commit()
        conn.close()
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        conn=sq.connect('todo.db')
        cur=conn.cursor()
        cur.execute('''select * from users where username=(?)''',(username,))
        user=cur.fetchone()
        conn.close()
        if user and check_password_hash(user[2],password):
            session['username']=username
            session['user_id']=user[0]
            flash("Welcome, " + username, "success")
            return redirect(url_for('index'))
        else :
            flash("Incorrect username or password", "danger")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    sort = request.args.get('sort','time')
    query = request.args.get('q','').lower()
    status_filter = request.args.get('status','All').lower()
    conn=sq.connect("todo.db")
    cur=conn.cursor()
    que= 'select * from tasks where user_id= '+str(session['user_id'])+' '
    if status_filter == 'pending':
        que+="and status='pending' "
    elif status_filter == 'done':
        que+="and status='Done' "
    if query :
        que+="and lower(task) like ? "
    if sort == 'time':
        que+='order by time_added asc '
    else:
        que+="order by case priority when 'High' then 1 when 'Medium' then 2 when 'Low' then 3 end"
    if query:
        cur.execute(que,('%' + query + '%',))
    else :
        cur.execute(que)
    tasks=cur.fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks,sort_by=sort,status_filter=status_filter,username=session['username'])
@app.route('/add',methods=['POST'])
def add():
    if 'username' not in session:
        return redirect(url_for('login'))
    task=request.form['task']
    priority=request.form['priority']
    conn=sq.connect("todo.db")
    cur=conn.cursor()
    cur.execute(''' insert into tasks (task,status,priority,user_id) values (?,?,?,?)''',(task,"pending",priority,session['user_id']))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn=sq.connect('todo.db')
    cur=conn.cursor()
    cur.execute('''delete from tasks where id=?''',(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/done/<int:id>',methods=['POST'])
def done(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn=sq.connect('todo.db')
    cur = conn.cursor()
    cur.execute('''update tasks set status='Done',time_done=CURRENT_TIMESTAMP where id=?''', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/edit/<int:id>',methods=['POST'])
def edit(id):
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sq.connect('todo.db')
    cur = conn.cursor()
    text=request.form['task']
    cur.execute('''update tasks set task=?,time_updated=CURRENT_TIMESTAMP where id=?''', (text,id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/api/register',methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = sq.connect('todo.db')
    cur = conn.cursor()
    try:
        cur.execute('''
                insert into users (username, password) values(?,?)''', (username, generate_password_hash(password)))
        return jsonify({"message":"Account created"})
    except:
        return jsonify({"message":"Account already exists"})
    finally:
        conn.commit()
        conn.close()
@app.route('/api/tasks',methods=['GET'])
def api_tasks():
    if 'username' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    conn=sq.connect('todo.db')
    cur=conn.cursor()
    cur.execute("select * from tasks where user_id=?", (session['user_id'],))
    tasks = cur.fetchall()
    conn.close()
    return jsonify(tasks)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
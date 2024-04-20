from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'my_secret_key_123' 

def connect_to_db():
    conn = psycopg2.connect(
        dbname="my_database",
        user="postgres",
        password="your_password",
        host="db",
        port="5432"
    )
    return conn

@app.route('/')
def index():
    return render_template('index.html', username=session.get('username'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Users WHERE username = %s", (username,))
        user = cur.fetchone()
        
        if user:
            cur.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
            user_with_password = cur.fetchone()
            if user_with_password:
                cur.close()
                conn.close()
                session['username'] = username
                return redirect(url_for('index', username=username))
            else:
                cur.close()
                conn.close()
                return render_template('incorrect_password.html')
        else:
            cur.close()
            conn.close()
            return render_template('user_not_found.html')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/web-development')
def web_development():
    return render_template('web-development.html')

@app.route('/mobile-apps')
def mobile_apps():
    return render_template('mobile-apps.html')

@app.route('/artificial-intelligence')
def artificial_intelligence():
    return render_template('artificial-intelligence.html')

@app.route('/internet-of-things')
def internet_of_things():
    return render_template('internet-of-things.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0')

from flask import Flask, request, render_template_string, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'vulnerable_secret_key'  # Clave secreta expuesta

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return "<h1>PyVulnApp - Flask Vulnerable App</h1>"

# Endpoint vulnerable a SQL Injection
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        result = conn.execute(query).fetchone()
        conn.close()
        
        if result:
            session['user'] = username
            return "<h2>Login exitoso</h2>"
        else:
            return "<h2>Credenciales incorrectas</h2>"
    
    return '''
        <form method="post">
            Usuario: <input type="text" name="username"><br>
            Contraseña: <input type="password" name="password"><br>
            <input type="submit" value="Iniciar sesión">
        </form>
    '''

# Endpoint vulnerable a XSS
@app.route('/comment', methods=['GET', 'POST'])
def comment():
    if request.method == 'POST':
        comment = request.form['comment']
        return render_template_string("""
            <h2>Tu comentario:</h2>
            <p>{{ comment }}</p>
            <a href='/comment'>Volver</a>
        """, comment=comment)  # No hay escape de HTML -> XSS
    
    return '''
        <form method="post">
            Comentario: <input type="text" name="comment"><br>
            <input type="submit" value="Publicar">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
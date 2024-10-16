class printer:
    def __init__(self):
        self.a = 1

    def sql_injection(self):
        print('''
        from flask import Flask, request, render_template_string
        import sqlite3
        
        app = Flask(__name__)
        
        # Use a persistent database file
        DATABASE = 'users.db'
        
        
        def get_db_connection():
            conn = sqlite3.connect(DATABASE)
            conn.row_factory = sqlite3.Row
            return conn
        
        
        # Initialize the database with some data (only run once)
        def init_db():
            conn = get_db_connection()
            conn.execute("""CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                username TEXT NOT NULL,
                                password TEXT NOT NULL)""")
            conn.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
            conn.execute("INSERT INTO users (username, password) VALUES ('user', 'userpass')")
            conn.commit()
            conn.close()
        
        
        # Initialize the database on app startup
        init_db()
        
        """
        # Vulnerable login function
        def check_login(username, password):
            conn = get_db_connection()
            query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
            result = conn.execute(query).fetchone()
            conn.close()
            return result
        """
        def check_login(username, password):
            conn = get_db_connection()
            # Use parameterized query to prevent SQL injection
            query = "SELECT * FROM users WHERE username=? AND password=?"
            result = conn.execute(query, (username, password)).fetchone()
            conn.close()
            return result
        
        # Route for the home page (login page)
        @app.route('/', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
        
                # Check login
                user = check_login(username, password)
        
                if user:
                    return f"<div class='alert alert-success'>Welcome, {username}!</div>"
                else:
                    return "<div class='alert alert-danger'>Login failed. Invalid username or password.</div>"
        
            return render_template_string("""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
                    <title>Login</title>
                    <style>
                        body {
                            background-color: #f8f9fa;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                        }
                        .login-container {
                            background-color: white;
                            padding: 30px;
                            border-radius: 8px;
                            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        }
                        .login-container h2 {
                            margin-bottom: 20px;
                            font-weight: bold;
                            color: #343a40;
                        }
                    </style>
                </head>
                <body>
                    <div class="login-container">
                        <h2>Login</h2>
                        <form method="post">
                            <div class="mb-3">
                                <label for="username" class="form-label">Username</label>
                                <input type="text" class="form-control" id="username" name="username" required>
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control" id="password" name="password" required>
                            </div>
                            <button type="submit" class="btn btn-primary w-100">Login</button>
                        </form>
                    </div>
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
                </body>
                </html>
            """)
        
        
        if __name__ == '__main__':
            app.run(debug=True)
        ''')

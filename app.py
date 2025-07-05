from flask import Flask, render_template, request, jsonify, session, redirect
import os
from datetime import datetime
import json
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from dream_analyzer import DreamAnalyzer

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Initialize the dream analyzer
analyzer = DreamAnalyzer()

# Database setup
def init_db():
    conn = sqlite3.connect('dream_journal.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Dreams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS dreams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            date_recorded TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            emotions TEXT,
            themes TEXT,
            analysis TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('dashboard.html')
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        password_hash = generate_password_hash(password)
        
        try:
            conn = sqlite3.connect('dream_journal.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                         (username, password_hash))
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Registration successful'})
        except sqlite3.IntegrityError:
            return jsonify({'error': 'Username already exists'}), 400
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('dream_journal.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            return jsonify({'success': True, 'redirect': '/'})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/add_dream', methods=['GET', 'POST'])
def add_dream():
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        if not title or not content:
            return jsonify({'error': 'Title and content required'}), 400
        
        # Analyze the dream
        analysis_result = analyzer.analyze_dream(content)
        
        # Save to database
        conn = sqlite3.connect('dream_journal.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dreams (user_id, title, content, emotions, themes, analysis)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (session['user_id'], title, content, 
              json.dumps(analysis_result['emotions']),
              json.dumps(analysis_result['themes']),
              json.dumps(analysis_result)))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'analysis': analysis_result})
    
    return render_template('add_dream.html')

@app.route('/dreams')
def view_dreams():
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = sqlite3.connect('dream_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, title, content, date_recorded, emotions, themes, analysis
        FROM dreams WHERE user_id = ? ORDER BY date_recorded DESC
    ''', (session['user_id'],))
    dreams = cursor.fetchall()
    conn.close()
    
    # Parse JSON fields
    dreams_data = []
    for dream in dreams:
        dreams_data.append({
            'id': dream[0],
            'title': dream[1],
            'content': dream[2],
            'date_recorded': dream[3],
            'emotions': json.loads(dream[4]) if dream[4] else [],
            'themes': json.loads(dream[5]) if dream[5] else [],
            'analysis': json.loads(dream[6]) if dream[6] else {}
        })
    
    return render_template('dreams.html', dreams=dreams_data)

@app.route('/insights')
def insights():
    if 'user_id' not in session:
        return redirect('/login')
    
    conn = sqlite3.connect('dream_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT emotions, themes, analysis, date_recorded
        FROM dreams WHERE user_id = ? ORDER BY date_recorded DESC
    ''', (session['user_id'],))
    dreams = cursor.fetchall()
    conn.close()
    
    # Generate insights
    insights_data = analyzer.generate_insights(dreams)
    
    return render_template('insights.html', insights=insights_data)

@app.route('/api/dream/<int:dream_id>')
def get_dream(dream_id):
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = sqlite3.connect('dream_journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT title, content, emotions, themes, analysis, date_recorded
        FROM dreams WHERE id = ? AND user_id = ?
    ''', (dream_id, session['user_id']))
    dream = cursor.fetchone()
    conn.close()
    
    if not dream:
        return jsonify({'error': 'Dream not found'}), 404
    
    return jsonify({
        'title': dream[0],
        'content': dream[1],
        'emotions': json.loads(dream[2]) if dream[2] else [],
        'themes': json.loads(dream[3]) if dream[3] else [],
        'analysis': json.loads(dream[4]) if dream[4] else {},
        'date_recorded': dream[5]
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)

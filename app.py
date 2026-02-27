import sqlite3
import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template, g

app = Flask(__name__)
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'bookmarks.db')


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_db(exc):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT    NOT NULL,
                url        TEXT    NOT NULL,
                created_at TEXT    NOT NULL,
                updated_at TEXT    NOT NULL
            )
        ''')
        conn.commit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/bookmarks', methods=['GET', 'POST'])
def bookmarks():
    db = get_db()

    if request.method == 'GET':
        rows = db.execute('SELECT * FROM bookmarks ORDER BY id DESC').fetchall()
        return jsonify([dict(r) for r in rows])

    data  = request.get_json(silent=True) or {}
    title = (data.get('title') or '').strip()
    url   = (data.get('url')   or '').strip()

    if not title or not url:
        return jsonify({'error': 'Title and URL are required.'}), 400

    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    cur = db.execute(
        'INSERT INTO bookmarks (title, url, created_at, updated_at) VALUES (?, ?, ?, ?)',
        (title, url, now, now)
    )
    db.commit()
    row = db.execute('SELECT * FROM bookmarks WHERE id = ?', (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201


@app.route('/api/bookmarks/<int:bookmark_id>', methods=['GET', 'PUT', 'DELETE'])
def bookmark_detail(bookmark_id):
    db  = get_db()
    row = db.execute('SELECT * FROM bookmarks WHERE id = ?', (bookmark_id,)).fetchone()

    if row is None:
        return jsonify({'error': 'Bookmark not found.'}), 404

    if request.method == 'GET':
        return jsonify(dict(row))

    if request.method == 'PUT':
        data  = request.get_json(silent=True) or {}
        title = (data.get('title') or '').strip()
        url   = (data.get('url')   or '').strip()

        if not title or not url:
            return jsonify({'error': 'Title and URL are required.'}), 400

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        db.execute(
            'UPDATE bookmarks SET title = ?, url = ?, updated_at = ? WHERE id = ?',
            (title, url, now, bookmark_id)
        )
        db.commit()
        updated = db.execute('SELECT * FROM bookmarks WHERE id = ?', (bookmark_id,)).fetchone()
        return jsonify(dict(updated))

    db.execute('DELETE FROM bookmarks WHERE id = ?', (bookmark_id,))
    db.commit()
    return jsonify({'message': 'Bookmark deleted successfully.'})


if __name__ == '__main__':
    init_db()
    app.run(debug=True)

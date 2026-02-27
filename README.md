# Smart-Bookmark-CRUD-Application

A full-stack **CRUD Bookmark Manager** built with **Python (Flask)** on the backend and plain HTML/CSS/JavaScript on the frontend. Bookmarks are stored in a local **SQLite** database.

## Features

| Operation | Endpoint | Description |
|-----------|----------|-------------|
| Create    | `POST /api/bookmarks`        | Add a new bookmark |
| Read      | `GET /api/bookmarks`         | List all bookmarks |
| Read one  | `GET /api/bookmarks/<id>`    | Get a single bookmark |
| Update    | `PUT /api/bookmarks/<id>`    | Edit title / URL |
| Delete    | `DELETE /api/bookmarks/<id>` | Remove a bookmark |

- Live favicon thumbnails per domain
- Client-side search / filter
- Toast notifications for all actions
- Keyboard shortcuts: **Enter** to submit, **Esc** to cancel edit

## Tech Stack

| Layer    | Technology |
|----------|-----------|
| Language | Python 3.10+ |
| Backend  | Flask 3.x |
| Database | SQLite (via Flask-SQLAlchemy) |
| Frontend | HTML5 / CSS3 / Vanilla JavaScript |

---

## Setup & Run Locally

### 1 — Clone the repository

```bash
git clone <your-repo-url>
cd bookmark-manager
```

### 2 — Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### 4 — Run the application

```bash
python app.py
```

The app will start at **http://127.0.0.1:5000**


## Deploying to Render (free)

1. Push this repo to GitHub.
2. Go to [render.com](https://render.com) → **New Web Service**.
3. Connect your GitHub repo.
4. Set:
   - **Build command:** `pip install -r requirements.txt`
   - **Start command:** `gunicorn app:app`
5. Add `gunicorn` to `requirements.txt`.
6. Click **Deploy** — Render provides a free live URL.


## Project Structure

```
bookmark-manager/
├── app.py               # Flask application + REST API
├── requirements.txt     # Python dependencies
├── bookmarks.db         # SQLite database (auto-created on first run)
├── README.md
└── templates/
    └── index.html       # Single-page frontend
```


## API Reference

### `GET /api/bookmarks`
Returns all bookmarks sorted by newest first.

**Response 200**
```json
[
  {
    "id": 1,
    "title": "GitHub",
    "url": "https://github.com",
    "created_at": "2025-01-01 10:00:00",
    "updated_at": "2025-01-01 10:00:00"
  }
]
```

### `POST /api/bookmarks`
**Body**
```json
{ "title": "GitHub", "url": "https://github.com" }
```
**Response 201** — the created bookmark object.

### `PUT /api/bookmarks/<id>`
**Body**
```json
{ "title": "New Title", "url": "https://new-url.com" }
```
**Response 200** — the updated bookmark object.

### `DELETE /api/bookmarks/<id>`
**Response 200**
```json
{ "message": "Bookmark deleted successfully." }
```

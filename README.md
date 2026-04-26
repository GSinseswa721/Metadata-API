# Metadata API — DRE Asset Metadata API

A REST API for managing Digital Realm Entertainment's creative assets, built with Django REST Framework.

## Stack
- Python 3 / Django 6
- Django REST Framework
- SQLite (dev)

## Requirements
- Python 3.11+
- pip

## Setup & Install

```bash
# Clone the repo
git clone https://github.com/GSinseswa721/Metadata-API.git
cd Metadata-API

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt

# Run migrations
python3 manage.py migrate
```

## Run

```bash
python3 manage.py runserver
```

API is available at: `http://127.0.0.1:8000/api/`

## Test

```bash
python3 manage.py test assets
```

Expected output:
```
Ran 7 tests in 0.Xs
OK
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/assets/` | List all assets |
| POST | `/api/assets/` | Create a new asset |
| GET | `/api/assets/?search=X` | Search assets by title or description |
| GET | `/api/assets/?status=draft` | Filter by status |
| GET | `/api/assets/?asset_type=image` | Filter by type |
| GET | `/api/assets/{id}/` | Get a single asset |
| PATCH | `/api/assets/{id}/` | Update an asset |
| DELETE | `/api/assets/{id}/` | Delete an asset |
| GET | `/api/assets/{id}/history/` | View full audit/version history |
| GET | `/api/assets/{id}/suggest-tags/` | Get quality tag suggestions |
| GET | `/api/tags/` | List all tags |
| POST | `/api/tags/` | Create a tag |

## Assumptions
- File URLs are stored as references, not actual file uploads
- ChangeLog entries are immutable — created automatically on every save
- SQLite is sufficient for this assessment scope

## What I Would Improve With More Time
- Add user authentication (JWT)
- Switch to PostgreSQL for production
- Add pagination to list endpoints
- Add created_by field to track which user made each change

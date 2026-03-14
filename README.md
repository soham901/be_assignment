# Backend Assignment

## Setup
```bash
uv run manage.py migrate
uv run manage.py loaddata core/fixtures/articles.json
uv run manage.py runserver
```

## Test

use [articles.http](articles.http) to test the API

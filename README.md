A basic notes API, built using FastAPI + SQLAlchemy & PostgreSQL. 

## To run with Docker
### Requirements: Docker, Docker Compose

### Steps
1. Build the project by running:
``` bash
docker compose build
```

2. PostgreSQL connection details 
``` bash
Host: db
Port: 5432
User: postgres
Password: postgres
Database: simplenotes
```

3. Start the service by running:
```bash
docker compose up
```

To view available routes' documentation, navigate to localhost:8000/docs once the app is running


## To run locally
### Requirements: Python, Pip, PostgreSQL, PGAdmin

1. To install the necessary python libraries, run:

``` bash
pip install -r requirements.txt
```

2. Set up a PostgreSQL database and add the database url to the .env file

3. Start the service, by running:
``` bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
To view available routes' documentation, navigate to localhost:8000/docs once the app is running
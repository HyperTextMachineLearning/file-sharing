# file-sharing

## Pre-requisites

>Note: Windows is not supported to run & test this application.

- A UNIX-based system having a cron-job like utility; 
- Docker (strongly recommended for Postgres)
- Python 3.8+

There are basically _THREE_ components in the applications:
- `PostgreSQL` container hosting the database
- `FastAPI` application
- A `cron-job` that handles auto-deleting files

---

## Setup

---

### Setting up `postgres`

Run the following in your terminal

```bash
$ docker pull postgres:alpine

$ docker run --name fastapi-postgres -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres:alpine

$ docker exec -it fastapi-postgres bash
```

You'll now enter the Alpine container having postgres

To enter into postgres run:

```bash
$ psql -U postgres
```

Now Postgres has started as default user `postgres`

Now create database & user for the `FastAPI` application & configure it for use using:

```
postgres=# CREATE DATABASE file_sharing;
postgres=# CREATE USER myuser WITH ENCRYPTED PASSWORD 'password';
postgres=# ALTER DATABASE file_sharing OWNER TO myuser;
postgres=# \c file_sharing;
postgres=# psql -h localhost -p 5432 postgres
```

Now leave the container running.

---

### Setting up our FastAPI app

After cloning this project, navigate to the cloned directory.

Create a virtual environment using `venv` module of python with and acitvate it:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

Now install all the dependencies using:

```bash
$ pip install -r requirements.txt
```

Start the application using:

```bash
$ cd src/
$ uvicorn main:app --reload
```

---

### Setting up the cron-job

Open your terminal and enter:

```bash
$ crontab -e
```

Select your desired editor if not selected.

Then go to the bottom of the file to add the following line:

```crontab
2 0 * * * cd /Absolute/Path-to/cloned-project-directory && /Absolute/Path-to/cloned-project-directory/venv/bin/python3 /Absolute/Path-to/cloned-project-directory/src/auto-delete.py >> /Path-to/Log/Errors/errors.txt
```

Replace `/Absolute/Path-to/cloned-project-directory` with, well, obviously to the absolute directory where you've cloned the project.

Basically this cronjob will run everyday at `12.02 AM`

---

### Running & Testing

The project now will be running at: `http:localhost:8000`

Using **POSTMAN** or `http:localhost:8000/docs` it can be tested

---

### A few important things to consider if using POSTMAN

- `"/login"` & `"/upload"` routes take input data using `form-data` in the `BODY` of request instead of raw JSON.
- First Register then Login to get a Token
- Go to `Authorization` tab under a request
- In the visible Drop-down select token type as `Bearer`.
- Now pass the previously obtained token in the textbox on the right to make authenticated requests.
- Please note the token expires after 30 minutes so you will need to login again after 30 minutes.

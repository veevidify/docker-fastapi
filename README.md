# Contents
- [Contents](#contents)
- [1. Prerequisites and installation:](#1-prerequisites-and-installation)
  - [a. Workflow](#a-workflow)
  - [b. URLs:](#b-urls)
- [2. Backend local dev env](#2-backend-local-dev-env)
  - [a. General workflow](#a-general-workflow)
  - [b. Structures](#b-structures)
  - [c. Docker Compose Override](#c-docker-compose-override)
  - [d. REPL](#d-repl)
  - [e. Backend tests](#e-backend-tests)
    - [Test running stack](#test-running-stack)
    - [Local tests](#local-tests)
    - [Test Coverage](#test-coverage)
  - [f. Development with Jupyter Notebooks](#f-development-with-jupyter-notebooks)
    - [Environment](#environment)
    - [Packages](#packages)
  - [g. Migrations](#g-migrations)
  - [h. Working with db](#h-working-with-db)
  - [i. Working with queue](#i-working-with-queue)
  - [k. Working with websocket](#k-working-with-websocket)
- [3. Development domain name](#3-development-domain-name)
  - [a. Development in `localhost` with a custom domain](#a-development-in-localhost-with-a-custom-domain)
  - [b. Development with a custom IP](#b-development-with-a-custom-ip)
  - [c. Change the development "domain" name](#c-change-the-development-domain-name)
- [4. Frontend development](#4-frontend-development)
  - [a. Start development](#a-start-development)
  - [b. WebSocket and CORS gotcha](#b-websocket-and-cors-gotcha)
  - [c. (Optional) Removing frontend](#c-optional-removing-frontend)
- [5. Deployment](#5-deployment)
  - [a. Traefik network](#a-traefik-network)
  - [b. Persisting Docker named volumes](#b-persisting-docker-named-volumes)
    - [Adding services with volumes](#adding-services-with-volumes)
    - [docker-auto-labels](#docker-auto-labels)
    - [(Optionally) adding labels manually](#optionally-adding-labels-manually)
  - [c. Deploy to a Docker Swarm mode cluster](#c-deploy-to-a-docker-swarm-mode-cluster)
    - [Procedure](#procedure)
    - [Deployment Technical Details](#deployment-technical-details)
  - [d. Continuous Integration / Continuous Delivery](#d-continuous-integration--continuous-delivery)
- [6. Docker Compose files and env vars](#6-docker-compose-files-and-env-vars)
  - [The .env file](#the-env-file)
- [7. URLs](#7-urls)
  - [a. Production URLs](#a-production-urls)
  - [b. Staging URLs](#b-staging-urls)
  - [c. Development URLs](#c-development-urls)
  - [d. Development with Docker Toolbox URLs](#d-development-with-docker-toolbox-urls)
  - [e. Development with a custom IP URLs](#e-development-with-a-custom-ip-urls)
  - [f. Development in localhost with a custom domain URLs](#f-development-in-localhost-with-a-custom-domain-urls)
- [8. Project generation and updating, or re-generating](#8-project-generation-and-updating-or-re-generating)
  - [a. cookiecutter](#a-cookiecutter)
  - [b. Input options generating project template](#b-input-options-generating-project-template)

---
_**Disclaimer**: This file is a summarised version of `README.md`_

---

# 1. Prerequisites and installation:
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.
* Node.js (with `npm`) for Frontend.

## a. Workflow
Start the stack with Docker Compose:

```bash
docker-compose up -d
```

## b. URLs:
- Frontend: http://localhost
- Backend API: http://localhost/api/
- Swagger UI: http://localhost/docs
- Alternative doc (ReDoc): http://localhost/redoc
- PGAdmin (for Postgres): http://localhost:5050
- Flower (for Celery tasks): http://localhost:5555
- Traefik dashboard, for proxy info: http://localhost:8090

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```

---

# 2. Backend local dev env

## a. General workflow

- Install [Poetry](https://python-poetry.org/).
- Dependencies:
```console
$ cd `backend/app/`
```
- Make sure `poetry.toml` has the right config (not modified):
```console
$ cat poetry.toml
```
Output:
```toml
[virtualenvs]
create = true
# uncomment in-project to create .venv within the proj (not recommended)
# in-project = true
```
- Start a shell session (venv):
```console
$ poetry shell
```
- Get packages
```console
$ poetry install
```
- In your IDE, point python interpreter and environment to the one `poetry` created, e.g. `./backend/app/.venv/bin/python3.8` (if in-project is uncommented in `poetry.toml`), otherwise `~/.cache/pypoetry/virtualenvs/app-[random_string]-py3.8/bin/python3.8`

- If new packages added to `pyproject.toml`, run update to resolve dependencies and create new lockfile:
```console
$ poetry update
```

_**Note**: It's important to note that poetry commands should be invoked from the host, within backend/app folder, instead of from within docker container service, in order to avoid conflicts._

_**Note**: Poetry virtual envs do not affect docker environment bootstrapped by `docker-compose`. It's purely for IDE and intellisense._

## b. Structures
- SQLAlchemy models: `./backend/app/app/models/`
- Pydantic schemas: `./backend/app/app/schemas/`
- API endpoints: `./backend/app/app/api/`
- CRUD utils: `./backend/app/app/crud/`.
- Celery worker's tasks in `./backend/app/app/worker.py`.
- Additional packages for worker: `./backend/app/celeryworker.dockerfile`.

## c. Docker Compose Override
- Overrides only take effect for local dev env, to achieve this, modify `docker-compose.override.yml`.
- E.g., volume mount, allowing changes to be reflected, without having to rebuild Docker image (development only)
- For prod, build the Docker image, preferably in CI.
- Command override `/start-reload.sh` in-place of `/start.sh` starts a single server process (instead of multi-threaded, which is suitable for prod). Often the container exits, you have to re-issue command:

```console
$ docker-compose up -d
```

- Commented out `command` override. Uncomment it and comment the default one. This makes backend container run a process that does "nothing", but keeps the container alive, allows `exec` into running container, e.g. running python REPL, start-reload, start Jupyter nb, etc.

- To achieve this:

```console
$ docker-compose up -d
```

and then:

```console
$ docker-compose exec backend bash
```

Output:

```console
root@7f2607af31c3:/app#
```

Which allows executing scripts such as:
```console
root@7f2607af31c3:/app# bash /start-reload.sh
```

- This keeps the container alive instead of exiting.

## d. REPL

- `ipython` is installed as REPL, to use, cd into backend folder and invoke it:
```console
cd backend/app
ipython
```
- In here you can import backend's modules and test snippets/functions:
```
 $  ipython
Python 3.8.0 (default, Feb 25 2021, 22:10:10)
Type 'copyright', 'credits' or 'license' for more information
IPython 7.28.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from fastapi import FastAPI

In [2]: from .app.models.item import Item
```

## e. Backend tests
- To test the backend run:

```console
$ DOMAIN=backend sh ./scripts/test.sh
```

- `./scripts/test.sh` generates a testing `docker-stack.yml` file, which starts the stack and test it.
- The tests run with Pytest: `./backend/app/app/tests/`.
- Gitlab CI is included which runs tests.

### Test running stack
- If stack is up, use:

```bash
docker-compose exec backend /app/tests-start.sh
```

### Local tests
- Start the stack:

```Bash
DOMAIN=backend sh ./scripts/test-local.sh
```
- `./backend/app` will be mounted as "host volume" inside the docker container (set in the file `docker-compose.dev.volumes.yml`).
- Rerun the test on live code:

```Bash
docker-compose exec backend /app/tests-start.sh
```

- `/app/tests-start.sh` simply calls `pytest`. Extra args to `pytest` will be forwarded, e.g., stopping on first error:
```bash
docker-compose exec backend bash /app/tests-start.sh -x
```

### Test Coverage
- Enable HTML report, `pytest` fashion, by passing `--cov-report=html`:
```Bash
DOMAIN=backend sh ./scripts/test-local.sh --cov-report=html
```
- For live stack:
```bash
docker-compose exec backend bash /app/tests-start.sh --cov-report=html
```

## f. Development with Jupyter Notebooks
### Environment
- `docker-compose.override.yml` file sends variable `env` = `dev` to the build process of the Docker image (local development), while `Dockerfile` has steps to install and configure Jupyter within the container.
- `exec` into running container:
```bash
docker-compose exec backend bash
```
- Use environment variable `$JUPYTER` to run a Jupyter Notebook with everything configured. Can visit from host's web browser.

- Sample output:

```console
root@73e0ec1f1ae6:/app# $JUPYTER
[I 12:02:09.975 NotebookApp] Writing notebook server cookie secret to /root/.local/share/jupyter/runtime/notebook_cookie_secret
[I 12:02:10.317 NotebookApp] Serving notebooks from local directory: /app
[I 12:02:10.317 NotebookApp] The Jupyter Notebook is running at:
[I 12:02:10.317 NotebookApp] http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
[I 12:02:10.317 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[W 12:02:10.317 NotebookApp] No web browser found: could not locate runnable browser.
[C 12:02:10.317 NotebookApp]

    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://(73e0ec1f1ae6 or 127.0.0.1):8888/?token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

- Replace the "host" to be `localhost` (or relevant domain):
```
http://localhost:8888/token=f20939a41524d021fbfc62b31be8ea4dd9232913476f4397
```

### Packages
- Since Jyputer notebooks run within the container, changes to the packages/dependencies warrant a re-build and restart of the container/service. After using `poetry add` to install new package, in the host, within `backend/app` folder, run:
```console
$ docker-compose build backend
```
Then
```console
$ docker-compose up -d backend
```
- And continue with notebooks development.

## g. Migrations
- Run migrations using `alembic` commands inside the container, migration code will be in your app directory, with volume mounting.
- `exec` into backend:
```console
$ docker-compose exec backend bash
```
- For every new model in `./backend/app/app/models/`, import it in `./backend/app/app/db/base.py`, which will be used by Alembic.
- After modifying the model, inside the container, create a revision:
```console
$ alembic revision --autogenerate -m "Add column last_name to User model"
```
Output:
```console
root@54b8181cdcfb:/app# alembic revision --autogenerate -m "Add column last_name to User model and dbschema"
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.ddl.postgresql] Detected sequence named 'user_id_seq' as owned by integer column 'user(id)', assuming SERIAL and omitting
INFO  [alembic.ddl.postgresql] Detected sequence named 'item_id_seq' as owned by integer column 'item(id)', assuming SERIAL and omitting
INFO  [alembic.autogenerate.compare] Detected added column 'user.last_name'
INFO  [alembic.autogenerate.compare] Detected NOT NULL on column 'user.email'
INFO  [alembic.autogenerate.compare] Detected NOT NULL on column 'user.hashed_password'
  Generating /app/alembic/versions/14ca970985f2_add_column_last_name_to_user_model_and_.py
  ...  done

```
- Double-check new file generated under `backend/app/alembic/versions`
- Run the migration to apply changes to database:

```console
$ alembic upgrade head
```
Output
```console
root@54b8181cdcfb:/app# alembic upgrade head
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade d4867f3a4c0a -> 14ca970985f2, Add column last_name to User model and dbschema
```
- Don't forget to commit.

**Note**: If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```

## h. Working with db
- You can browse the db via psql inside the db container:
```console
$ docker-compose exec db psql --user=postgres app
```
- Then some psql commands or sql queries:
```console
psql (12.8 (Debian 12.8-1.pgdg110+1))
Type "help" for help.

app-# \dt
```
Output:
```console
app-# \dt
              List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+----------
 public | alembic_version | table | postgres
 public | item            | table | postgres
 public | user            | table | postgres
(3 rows)
```
```console
app=# select * from public.user;
```
Output:
```console
app=# select * from public.user;
 id | full_name |         email         |                       hashed_password
             | is_active | is_superuser | last_name
----+-----------+-----------------------+-------------------------------------------------
-------------+-----------+--------------+-----------
  1 |           | admin@fastapi-app.com | $2b$12$JA82XxbBWmnmHK2.71y/sOQ4172GvOO/mulsCuFT7
wca.dZiLurhW | t         | t            |
(1 row)

```
**Note**: This is simply a hash for "123456" for development purposes.

## i. Working with queue
- `celery` handler and tasks are defined in `app/worker.py` for the moment. It might make sense to split it into 2 files: one only containing the celery handler and configs, the other with all the declared tasks to be invoked by controller.
- Queue using `celery` is configured with `redis` pub/sub and backend for persistence. To inspect the queue, cli into `redis` container (service `queue`, as declared in `docker-compose.yml`):
```console
$ docker-compose exec queue redis-cli
```
- To view task's results, get the specific task using `GET` (simple key - string value mapping):
```
127.0.0.1:6379> KEYS **
 1) "_kombu.binding.celery.pidbox"
 2) "celery-task-meta-c4f0990d-8d13-4848-8f5f-39be4e07c5ad"
 3) "celery-task-meta-04db80d2-9994-4058-8d41-8875c50534dd"
 4) "celery-task-meta-5a9d9666-9049-4a78-b02a-b514236d5265"
 5) "celery-task-meta-01e16094-76b3-418f-a80a-9f6a2b76c400"
 6) "celery-task-meta-456c7a24-297a-4e0e-bef5-34cb6b3643e4"
 7) "_kombu.binding.celery"
 8) "celery"
 9) "_kombu.binding.main-queue"
10) "_kombu.binding.celeryev"

127.0.0.1:6379> GET celery-task-meta-c4f0990d-8d13-4848-8f5f-39be4e07c5ad
"{\"status\": \"SUCCESS\", \"result\": \"test task return test fr vue again\", \"traceback\": null, \"children\": [], \"date_done\": \"2021-11-01T09:14:34.166946\", \"task_id\": \"c4f0990d-8d13-4848-8f5f-39be4e07c5ad\"}"
```
- To inspect queued (but not picked up by `celery`) tasks, use list retrieval for `celery` key:
```console
127.0.0.1:6379> LRANGE celery 1 10
```

## k. Working with websocket
- Websocket support is already built into FastAPI core. Logging from websocket requests is also standard, just like other (HTTP) API routes.
- For authorization, since native browser WebSocket does not support any standard authorization headers, we make use of cookies. Upon logging in, the backend will respond with a `set-cookie` response header, directing the browser to persist this token:
```py
# api.api_v1.endpoints.login
    response.set_cookie(key="token", value=access_token, path="/", expires=access_token_expires)
```
- Then this `token` cookie will automatically be attached to the WS request from frontend.
- Read further below in 4. Frontend > WebSocket and CORS gotcha.

# 3. Development domain name

## a. Development in `localhost` with a custom domain
- With hostname/CORS/cookies issues, you can use `localhost.tiangolo.com`, it is set up to point to `localhost` (to the IP `127.0.0.1`) and all subdomains.
- `localhost.tiangolo.com` was configured to be allowed. Otherwise, add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.
- To configure it in your stack, follow **Change the development "domain"** below, using domain `localhost.tiangolo.com`.
- You should be able to open: http://localhost.tiangolo.com, it will be server by your stack in `localhost`.

## b. Development with a custom IP
- If you are running Docker in an IP address different than `127.0.0.1` (`localhost`) and `192.168.99.100` (the default of Docker Toolbox), you will need to use a fake local domain (`dev.fastapi-app.com`) and make your computer think that the domain is is served by the custom IP (e.g. `192.168.99.150`).
- `dev.fastapi-app.com` was configured to be allowed. If you want a custom one, add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.
- Open `/etc/hosts`, added line might look like:
```
192.168.99.100    dev.fastapi-app.com
```
- To configure it in your stack, follow the section **Change the development "domain"** below, using domain `dev.fastapi-app.com`.

- You should be able to open: http://dev.fastapi-app.com, it will be server by your stack in `localhost`.

## c. Change the development "domain" name

If you need to use your local stack with a different domain than `localhost`, you need to make sure the domain you use points to the IP where your stack is set up. See the different ways to achieve that in the sections above (i.e. using Docker Toolbox with `local.dockertoolbox.tiangolo.com`, using `localhost.tiangolo.com` or using `dev.fastapi-app.com`).

To simplify your Docker Compose setup, for example, so that the API docs (Swagger UI) knows where is your API, you should let it know you are using that domain for development. You will need to edit 1 line in 2 files.

* Open the file located at `./.env`. It would have a line like:

```
DOMAIN=localhost
```

* Change it to the domain you are going to use, e.g.:

```
DOMAIN=localhost.tiangolo.com
```

That variable will be used by the Docker Compose files.

* Now open the file located at `./frontend/.env`. It would have a line like:

```
VUE_APP_DOMAIN_DEV=localhost
```

* Change that line to the domain you are going to use, e.g.:

```
VUE_APP_DOMAIN_DEV=localhost.tiangolo.com
```

That variable will make your frontend communicate with that domain when interacting with your backend API, when the other variable `VUE_APP_ENV` is set to `development`.

After changing the two lines, you can re-start your stack with:

```bash
docker-compose up -d
```

and check all the corresponding available URLs in the section at the end.

---

# 4. Frontend development
## a. Start development
- Enter the `frontend` directory:
```bash
cd frontend
npm install
npm run serve
```
- Then browse to http://localhost:8080
- It's recommended to work with frontend in host env for live-reload, fast npm tools, etc..
- You can build the frontend image and start it, to test in a production-like environment.
- Check `package.json`.
- Can point local frontend to staging env. To achieve this,modify `./frontend/.env`, change:

```
VUE_APP_ENV=development
# VUE_APP_ENV=staging
```
to:
```
# VUE_APP_ENV=development
VUE_APP_ENV=staging
```

## b. WebSocket and CORS gotcha
- If you went with the default development environment, with Vue at `localhost:8080` and FastAPI at `localhost`, you will run into CORS issues with `set-cookie`.
- Specifically, `set-cookie` directs the browser to set one at `localhost:8080`, then afterwards, WebSocket connection is calling `localhost`, for which the browser will not provide the `token` for.
- The work around for development is obtain a valid token, e.g. via Swagger, then manually set it in browser for `localhost`, or launch the Vue app at `localhost` (online via docker service) and login normally, which will make browser persist a `token` for `localhost` instead of `localhost:8080` via `set-cookie` response header, which makes other requests to api/ws at `localhost` from Vue include this `token` cookie.

## c. (Optional) Removing frontend
If you wish to remove in favour of other frontends:
- Remove the `./frontend` directory.
- In the `docker-compose.yml` file, remove the whole service / section `frontend`.
- In the `docker-compose.override.yml` file, remove the whole service / section `frontend`.
- You have a frontend-less (api-only) app.
- You can also remove the `FRONTEND` environment variables from:
  * `.env`
  * `.gitlab-ci.yml`
  * `./scripts/*.sh`

---

# 5. Deployment

_**Note**: Consult the [official docs for Deployment](https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes) first._

You can deploy the stack to a Docker Swarm mode cluster with a main Traefik proxy, set up using the ideas from <a href="https://dockerswarm.rocks" target="_blank">DockerSwarm.rocks</a>, to get automatic HTTPS certificates, etc.

And you can use CI (continuous integration) systems to do it automatically.

But you have to configure a couple things first.

## a. Traefik network

This stack expects the public Traefik network to be named `traefik-public`, just as in the tutorials in <a href="https://dockerswarm.rocks" class="external-link" target="_blank">DockerSwarm.rocks</a>.

If you need to use a different Traefik public network name, update it in the `docker-compose.yml` files, in the section:

```YAML
networks:
  traefik-public:
    external: true
```

Change `traefik-public` to the name of the used Traefik network. And then update it in the file `.env`:

```bash
TRAEFIK_PUBLIC_NETWORK=traefik-public
```

## b. Persisting Docker named volumes

- Make sure each service (Docker container) that uses a volume is always deployed to the same Docker "node" in the cluster to preserve the data. Otherwise, if deployed to a different node, the volume would be re-created in that new node before starting the service, as if starting from scratch and lose all the previous data.
- Especially important for a service running a database, saving files in backend service.
- To achieve this, put constraints in the services that use data volumes (like databases), making them be deployed to a Docker node with a specific label.
- You need to have that label assigned to only one of your nodes.

### Adding services with volumes

- For each service that uses a volume (databases, services with persisted files, etc) assign a label constraint in `docker-compose.yml`.
- To make sure labels are unique per volume, per stack (for example, that they are not the same for `prod` and `staging`), prefix them with the name of the stack, then use the same name of the volume.
- Then, have those constraints in `docker-compose.yml` for the services that need to be fixed with each volume.
- To use different environments, like `prod` and `staging`, pass the name of the stack as an environment variable. Like:

```bash
STACK_NAME=staging-fastapi-app sh ./scripts/deploy.sh
```

- To use and expand that environment variable inside the `docker-compose.yml`, add the constraints to the services:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.${STACK_NAME?Variable not set}.app-db-data == true
```

- The `${STACK_NAME?Variable not set}`, used by script `./scripts/deploy.sh`, would convert `docker-compose.yml`, and saved to a file `docker-stack.yml` containing:

```yaml
version: '3'
services:
  db:
    volumes:
      - 'app-db-data:/var/lib/postgresql/data/pgdata'
    deploy:
      placement:
        constraints:
          - node.labels.fastapi-template-app.app-db-data == true
```

**Note**:
- `${STACK_NAME?Variable not set}` uses the environment variable `STACK_NAME`. If not set, show an error `Variable not set`".
- More volumes added means the corresponding constraints to the services that use that named volume need to be added/set.
- Then create those labels in some nodes in your Docker Swarm mode cluster. `docker-auto-labels` can do this automatically.

### docker-auto-labels

- [`docker-auto-labels`](https://github.com/tiangolo/docker-auto-labels) can automatically read the placement constraint labels in your Docker stack (Docker Compose file), and assign them to a random Docker node in your Swarm mode cluster if those labels don't exist yet.

- To achieve this, install `docker-auto-labels`:

```bash
pip install docker-auto-labels
```

- Then run it, passing `docker-stack.yml` as a parameter:

```bash
docker-auto-labels docker-stack.yml
```

- You can run that command every time you deploy, right before deploying, as it doesn't modify anything if the required labels already exist.

### (Optionally) adding labels manually
Without using `docker-auto-labels`, you can manually assign the constraint labels to specific nodes in your Docker Swarm mode cluster:

* First, SSH into your Docker Swarm mode cluster.

* Then check the available nodes, and chose a node from the list. For example, `dog.example.com`:

```console
$ docker node ls


// you would see an output like:

ID                            HOSTNAME               STATUS              AVAILABILITY        MANAGER STATUS
nfa3d4df2df34as2fd34230rm *   dog.example.com        Ready               Active              Reachable
2c2sd2342asdfasd42342304e     cat.example.com        Ready               Active              Leader
c4sdf2342asdfasd4234234ii     snake.example.com      Ready               Active              Reachable
```

* Add the label to that node. Use as label the name of the stack you are deploying followed by a dot (`.`) followed by the named volume, and as value, just `true`, e.g.:

```bash
docker node update --label-add fastapi-template-app.app-db-data=true dog.example.com
```

* Then, do the same for each stack version you have. For example, for staging:

```bash
docker node update --label-add staging-fastapi-app.app-db-data=true cat.example.com
```

## c. Deploy to a Docker Swarm mode cluster
### Procedure
There are 3 steps:

1. **Build** your app images
2. Optionally, **push** your custom images to a Docker Registry
3. **Deploy** your stack

---

Here are the steps in detail:

1. **Build your app images**

* Set these environment variables, right before the next command:
  * `TAG=prod`
  * `FRONTEND_ENV=production`
* Use the provided `scripts/build.sh` file with those environment variables:

```bash
TAG=prod FRONTEND_ENV=production bash ./scripts/build.sh
```

2. **Optionally, push your images to a Docker Registry**

**Note**: if the deployment Docker Swarm mode "cluster" has more than one server, you will have to push the images to a registry or build the images in each server, so that when each of the servers in your cluster tries to start the containers it can get the Docker images for them, pulling them from a Docker Registry or because it has them already built locally.

If you are using a registry and pushing your images, you can omit running the previous script and instead using this one, in a single shot.

* Set these environment variables:
  * `TAG=prod`
  * `FRONTEND_ENV=production`
* Use the provided `scripts/build-push.sh` file with those environment variables:

```bash
TAG=prod FRONTEND_ENV=production bash ./scripts/build-push.sh
```

3. **Deploy your stack**

* Set these environment variables:
  * `DOMAIN=fastapi-app.com`
  * `TRAEFIK_TAG=fastapi-app.com`
  * `STACK_NAME=fastapi-template-app`
  * `TAG=prod`
* Use the provided `scripts/deploy.sh` file with those environment variables:

```bash
DOMAIN=fastapi-app.com \
TRAEFIK_TAG=fastapi-app.com \
STACK_NAME=fastapi-template-app \
TAG=prod \
bash ./scripts/deploy.sh
```

---

- If you change your mind and, for example, want to deploy everything to a different domain, you only have to change the `DOMAIN` environment variable in the previous commands.

- If you wanted to add a different version / environment of your stack, like "`preproduction`", you would only have to set `TAG=preproduction` in your command and update these other environment variables accordingly. And it would all work, that way you could have different environments and deployments of the same app in the same cluster.

### Deployment Technical Details

- Building and pushing is done with the `docker-compose.yml` file, using the `docker-compose` command. The file `docker-compose.yml` uses the file `.env` with default environment variables. The scripts set some additional environment variables as well.
- Deployment requires using `docker stack` instead of `docker-swarm`, and it can't read environment variables or `.env` files. Because of that, the `deploy.sh` script generates a file `docker-stack.yml` with configs read from `docker-compose.yml`, then injecting the environment variables in it. This `docker-stack.yml` is then used to deploy the stack.
- Alternatively, you can do the process manually using those same scripts (e.g. different CI). The general structure looks like this:

```bash
# Use the environment variables passed to this script, as TAG and FRONTEND_ENV
# And re-create those variables as environment variables for the next command
TAG=${TAG?Variable not set} \
# Set the environment variable FRONTEND_ENV to the same value passed to this script with
# a default value of "production" if nothing else was passed
FRONTEND_ENV=${FRONTEND_ENV-production?Variable not set} \
# The actual comand that does the work: docker-compose
docker-compose \
# Pass the file that should be used, setting explicitly docker-compose.yml avoids the
# default of also using docker-compose.override.yml
-f docker-compose.yml \
# Use the docker-compose sub command named "config", it just uses the docker-compose.yml
# file passed to it and prints their combined contents
# Put those contents in a file "docker-stack.yml", with ">"
config > docker-stack.yml

# The previous only generated a docker-stack.yml file,
# but didn't do anything with it yet

# docker-auto-labels makes sure the labels used for constraints exist in the cluster
docker-auto-labels docker-stack.yml

# Now this command uses that same file to deploy it
docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"
```

## d. Continuous Integration / Continuous Delivery

- `.gitlab-ci.yml` is included and can automatically deploy. You may need to update it according to your GitLab configurations.

- For other CI / CD providers, base your deployment from `.gitlab-ci.yml`, since all script steps are performed in reusable `bash` scripts.

GitLab CI is configured assuming 2 environments following GitLab flow:

* `prod` (production) from the `production` branch.
* `stag` (staging) from the `master` branch.

- If you require more environments, e.g. client-approved/QA `preprod` branch, copy the configurations in `.gitlab-ci.yml` for `stag`, rename the corresponding variables.
- The Docker Compose file and environment variables are configured to support as many environments as you need, so that you only need to modify `.gitlab-ci.yml`.

---

# 6. Docker Compose files and env vars

- Main `docker-compose.yml` file contains all configurations for the whole stack.
- `docker-compose.override.yml` gives overrides for development, e.g. volume mount source code. It is used automatically by `docker-compose`, applying overrides on top of `docker-compose.yml` (merging `yaml`).
- These Docker Compose files use the `.env` file, containing configurations to be injected as environment variables in the containers.
- They also use some additional configurations taken from environment variables set in the scripts before calling the `docker-compose` command.
- This design pattern support "stages" workflow, like development, building, testing, and deployment, allowing the deployment to different environments.
- Extending is simple, e.g. to have another deployment environment, say `preprod`, just change environment variables, while keep using the same Docker Compose files.

## The .env file

- `.env` file is the one that contains all your configurations, generated keys and passwords, etc.
- If git-ignored, add each environment variable to CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.

---

# 7. URLs

These are the URLs that will be used and generated by the project.

## a. Production URLs
- Production URLs, from the branch `production`.
- Frontend: https://fastapi-app.com
- Backend: https://fastapi-app.com/api/
- Automatic Interactive Docs (Swagger UI): https://fastapi-app.com/docs
- Automatic Alternative Docs (ReDoc): https://fastapi-app.com/redoc
- PGAdmin: https://pgadmin.fastapi-app.com
- Flower: https://flower.fastapi-app.com

## b. Staging URLs
- Staging URLs, from the branch `master`.
- Frontend: https://staging.fastapi-app.com
- Backend: https://staging.fastapi-app.com/api/
- Automatic Interactive Docs (Swagger UI): https://staging.fastapi-app.com/docs
- Automatic Alternative Docs (ReDoc): https://staging.fastapi-app.com/redoc
- PGAdmin: https://pgadmin.staging.fastapi-app.com
- Flower: https://flower.staging.fastapi-app.com

## c. Development URLs
- Development URLs, for local development.
- Frontend: http://localhost
- Backend: http://localhost/api/
- Automatic Interactive Docs (Swagger UI): https://localhost/docs
- Automatic Alternative Docs (ReDoc): https://localhost/redoc
- PGAdmin: http://localhost:5050
- Flower: http://localhost:5555
- Traefik UI: http://localhost:8090

## d. Development with Docker Toolbox URLs
- Development URLs, for local development.
- Frontend: http://local.dockertoolbox.tiangolo.com
- Backend: http://local.dockertoolbox.tiangolo.com/api/
- Automatic Interactive Docs (Swagger UI): https://local.dockertoolbox.tiangolo.com/docs
- Automatic Alternative Docs (ReDoc): https://local.dockertoolbox.tiangolo.com/redoc
- PGAdmin: http://local.dockertoolbox.tiangolo.com:5050
- Flower: http://local.dockertoolbox.tiangolo.com:5555
- Traefik UI: http://local.dockertoolbox.tiangolo.com:8090

## e. Development with a custom IP URLs
- Development URLs, for local development.
- Frontend: http://dev.fastapi-app.com
- Backend: http://dev.fastapi-app.com/api/
- Automatic Interactive Docs (Swagger UI): https://dev.fastapi-app.com/docs
- Automatic Alternative Docs (ReDoc): https://dev.fastapi-app.com/redoc
- PGAdmin: http://dev.fastapi-app.com:5050
- Flower: http://dev.fastapi-app.com:5555
- Traefik UI: http://dev.fastapi-app.com:8090

## f. Development in localhost with a custom domain URLs
- Development URLs, for local development.
- Frontend: http://localhost.tiangolo.com
- Backend: http://localhost.tiangolo.com/api/
- Automatic Interactive Docs (Swagger UI): https://localhost.tiangolo.com/docs
- Automatic Alternative Docs (ReDoc): https://localhost.tiangolo.com/redoc
- PGAdmin: http://localhost.tiangolo.com:5050
- Flower: http://localhost.tiangolo.com:5555
- Traefik UI: http://localhost.tiangolo.com:8090

---

# 8. Project generation and updating, or re-generating
## a. cookiecutter

This project was generated using https://github.com/tiangolo/full-stack-fastapi-postgresql with:

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql
```

## b. Input options generating project template

The input variables, with their default values (some auto generated) are:
-    `project_name`: The name of the project
-    `project_slug`: The development friendly name of the project. By default, based on the project name
-    `domain_main`: The domain in where to deploy the project for production (from the branch production), used by the load balancer, backend, etc. By default, based on the project slug.
-    `domain_staging`: The domain in where to deploy while staging (before production) (from the branch master). By default, based on the main domain.
-    `docker_swarm_stack_name_main`: The name of the stack while deploying to Docker in Swarm mode for production. By default, based on the domain.
-    `docker_swarm_stack_name_staging`: The name of the stack while deploying to Docker in Swarm mode for staging. By default, based on the domain.
-    `secret_key`: Backend server secret key. Use the method above to generate it.
-    `first_superuser`: The first superuser generated, with it you will be able to create more users, etc. By default, based on the domain.
-    `first_superuser_password`: First superuser password. Use the method above to generate it.
-    `backend_cors_origins`: Origins (domains, more or less) that are enabled for CORS (Cross Origin Resource Sharing). This allows a frontend in one domain (e.g. https://dashboard.example.com) to communicate with this backend, that could be living in another domain (e.g. https://api.example.com). It can also be used to allow your local frontend (with a custom hosts domain mapping, as described in the project's README.md) that could be living in http://dev.example.com:8080 to communicate with the backend at https://stag.example.com. Notice the http vs https and the dev. prefix for local development vs the "staging" stag. prefix. By default, it includes origins for production, staging and development, with ports commonly used during local development by several popular frontend frameworks (Vue with :8080, React, Angular).
-    `smtp_port`: Port to use to send emails via SMTP. By default 587.
-    `smtp_host`: Host to use to send emails, it would be given by your email provider, like Mailgun, Sparkpost, etc.
-    `smtp_user`: The user to use in the SMTP connection. The value will be given by your email provider.
-    `smtp_password`: The password to be used in the SMTP connection. The value will be given by the email provider.
-    `smtp_emails_from_email`: The email account to use as the sender in the notification emails, it would be something like info@your-custom-domain.com.
-    `postgres_password`: Postgres database password. Use the method above to generate it. (You could easily modify it to use MySQL, MariaDB, etc).
-    `pgadmin_default_user`: PGAdmin default user, to log-in to the PGAdmin interface.
-    `pgadmin_default_user_password`: PGAdmin default user password. Generate it with the method above.
-    `traefik_constraint_tag`: The tag to be used by the internal Traefik load balancer (for example, to divide requests between backend and frontend) for production. Used to separate this stack from any other stack you might have. This should identify each stack in each environment (production, staging, etc).
-    `traefik_constraint_tag_staging`: The Traefik tag to be used while on staging.
-    `traefik_public_constraint_tag`: The tag that should be used by stack services that should communicate with the public.
-    `flower_auth`: Basic HTTP authentication for flower, in the formuser:password. By default: "admin:changethis".
-    `sentry_dsn`: Key URL (DSN) of Sentry, for live error reporting. You can use the open source version or a free account. E.g.: https://1234abcd:5678ef@sentry.example.com/30.
-    `docker_image_prefix`: Prefix to use for Docker image names. If you are using GitLab Docker registry it would be based on your code repository. E.g.: git.example.com/development-team/my-awesome-project/.
-    `docker_image_backend`: Docker image name for the backend. By default, it will be based on your Docker image prefix, e.g.: git.example.com/development-team/my-awesome-project/backend. And depending on your environment, a different tag will be appended ( prod, stag, branch ). So, the final image names used will be like: git.example.com/development-team/my-awesome-project/backend:prod.
-    `docker_image_celeryworker`: Docker image for the celery worker. By default, based on your Docker image prefix.
-    `docker_image_frontend`: Docker image for the frontend. By default, based on your Docker image prefix.

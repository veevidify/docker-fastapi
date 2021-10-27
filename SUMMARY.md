# Contents
- [Contents](#contents)
- [1. Prerequisites and installation:](#1-prerequisites-and-installation)
    - [Workflow](#workflow)
    - [URLs:](#urls)
- [2. Backend local dev env](#2-backend-local-dev-env)
    - [General workflow](#general-workflow)
    - [Structures](#structures)
    - [Docker Compose Override](#docker-compose-override)
    - [Backend tests](#backend-tests)
      - [Test running stack](#test-running-stack)
      - [Local tests](#local-tests)
      - [Test Coverage](#test-coverage)
    - [Development with Jupyter Notebooks](#development-with-jupyter-notebooks)
    - [Migrations](#migrations)
    - [Development in `localhost` with a custom domain](#development-in-localhost-with-a-custom-domain)
    - [Development with a custom IP](#development-with-a-custom-ip)
    - [Change the development "domain"](#change-the-development-domain)
- [3. Frontend development](#3-frontend-development)
    - [Removing frontend](#removing-frontend)
- [4. Deployment](#4-deployment)
    - [Traefik network](#traefik-network)
    - [Persisting Docker named volumes](#persisting-docker-named-volumes)
      - [Adding services with volumes](#adding-services-with-volumes)
      - [`docker-auto-labels`](#docker-auto-labels)
      - [(Optionally) adding labels manually](#optionally-adding-labels-manually)
    - [Deploy to a Docker Swarm mode cluster](#deploy-to-a-docker-swarm-mode-cluster)
      - [Deployment Technical Details](#deployment-technical-details)
    - [Continuous Integration / Continuous Delivery](#continuous-integration--continuous-delivery)
- [5. Docker Compose files and env vars](#5-docker-compose-files-and-env-vars)
    - [The .env file](#the-env-file)
- [6. URLs](#6-urls)
    - [Production URLs](#production-urls)
    - [Staging URLs](#staging-urls)
    - [Development URLs](#development-urls)
    - [Development with Docker Toolbox URLs](#development-with-docker-toolbox-urls)
    - [Development with a custom IP URLs](#development-with-a-custom-ip-urls)
    - [Development in localhost with a custom domain URLs](#development-in-localhost-with-a-custom-domain-urls)
- [7. Project generation and updating, or re-generating](#7-project-generation-and-updating-or-re-generating)

---

# 1. Prerequisites and installation:
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Poetry](https://python-poetry.org/) for Python package and environment management.
* Node.js (with `npm`) for Frontend.

### Workflow
Start the stack with Docker Compose:

```bash
docker-compose up -d
```

### URLs:
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

### General workflow

- Install [Poetry](https://python-poetry.org/).
- Dependencies:
```console
$ cd `backend/app/`
```

```console
$ poetry install
```

Start a shell session (venv):

```console
$ poetry shell
```
### Structures
- SQLAlchemy models: `./backend/app/app/models/`
- Pydantic schemas: `./backend/app/app/schemas/`
- API endpoints: `./backend/app/app/api/`
- CRUD utils: `./backend/app/app/crud/`.
- Celery worker's tasks in `./backend/app/app/worker.py`.
- Additional packages for worker: `./backend/app/celeryworker.dockerfile`.

### Docker Compose Override
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

### Backend tests
- To test the backend run:

```console
$ DOMAIN=backend sh ./scripts/test.sh
```

- `./scripts/test.sh` generates a testing `docker-stack.yml` file, which starts the stack and test it.
- The tests run with Pytest: `./backend/app/app/tests/`.
- Gitlab CI is included which runs tests.

#### Test running stack
- If stack is up, use:

```bash
docker-compose exec backend /app/tests-start.sh
```

#### Local tests
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

#### Test Coverage
- Enable HTML report, `pytest` fashion, by passing `--cov-report=html`:
```Bash
DOMAIN=backend sh ./scripts/test-local.sh --cov-report=html
```
- For live stack:
```bash
docker-compose exec backend bash /app/tests-start.sh --cov-report=html
```

### Development with Jupyter Notebooks

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

### Migrations
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
- Run the migration to apply changes to database:

```console
$ alembic upgrade head
```
- Don't forget to commit.

- If you don't want to use migrations at all, uncomment the line in the file at `./backend/app/app/db/init_db.py` with:

```python
Base.metadata.create_all(bind=engine)
```

and comment the line in the file `prestart.sh` that contains:

```console
$ alembic upgrade head
```

### Development in `localhost` with a custom domain
- With hostname/CORS/cookies issues, you can use `localhost.tiangolo.com`, it is set up to point to `localhost` (to the IP `127.0.0.1`) and all subdomains.
- `localhost.tiangolo.com` was configured to be allowed. Otherwise, add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.
- To configure it in your stack, follow **Change the development "domain"** below, using domain `localhost.tiangolo.com`.
- You should be able to open: http://localhost.tiangolo.com, it will be server by your stack in `localhost`.

### Development with a custom IP
- If you are running Docker in an IP address different than `127.0.0.1` (`localhost`) and `192.168.99.100` (the default of Docker Toolbox), you will need to use a fake local domain (`dev.fastapi-app.com`) and make your computer think that the domain is is served by the custom IP (e.g. `192.168.99.150`).
- `dev.fastapi-app.com` was configured to be allowed. If you want a custom one, add it to the list in the variable `BACKEND_CORS_ORIGINS` in the `.env` file.
- Open `/etc/hosts`, added line might look like:
```
192.168.99.100    dev.fastapi-app.com
```
- To configure it in your stack, follow the section **Change the development "domain"** below, using domain `dev.fastapi-app.com`.

- You should be able to open: http://dev.fastapi-app.com, it will be server by your stack in `localhost`.

### Change the development "domain"

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

# 3. Frontend development
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

### Removing frontend
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

# 4. Deployment

You can deploy the stack to a Docker Swarm mode cluster with a main Traefik proxy, set up using the ideas from <a href="https://dockerswarm.rocks" target="_blank">DockerSwarm.rocks</a>, to get automatic HTTPS certificates, etc.

And you can use CI (continuous integration) systems to do it automatically.

But you have to configure a couple things first.

### Traefik network

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

### Persisting Docker named volumes

You need to make sure that each service (Docker container) that uses a volume is always deployed to the same Docker "node" in the cluster, that way it will preserve the data. Otherwise, it could be deployed to a different node each time, and each time the volume would be created in that new node before starting the service. As a result, it would look like your service was starting from scratch every time, losing all the previous data.

That's specially important for a service running a database. But the same problem would apply if you were saving files in your main backend service (for example, if those files were uploaded by your users, or if they were created by your system).

To solve that, you can put constraints in the services that use one or more data volumes (like databases) to make them be deployed to a Docker node with a specific label. And of course, you need to have that label assigned to one (only one) of your nodes.

#### Adding services with volumes

For each service that uses a volume (databases, services with uploaded files, etc) you should have a label constraint in your `docker-compose.yml` file.

To make sure that your labels are unique per volume per stack (for example, that they are not the same for `prod` and `stag`) you should prefix them with the name of your stack and then use the same name of the volume.

Then you need to have those constraints in your `docker-compose.yml` file for the services that need to be fixed with each volume.

To be able to use different environments, like `prod` and `stag`, you should pass the name of the stack as an environment variable. Like:

```bash
STACK_NAME=staging-fastapi-app sh ./scripts/deploy.sh
```

To use and expand that environment variable inside the `docker-compose.yml` files you can add the constraints to the services like:

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

note the `${STACK_NAME?Variable not set}`. In the script `./scripts/deploy.sh`, the `docker-compose.yml` would be converted, and saved to a file `docker-stack.yml` containing:

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

**Note**: The `${STACK_NAME?Variable not set}` means "use the environment variable `STACK_NAME`, but if it is not set, show an error `Variable not set`".

If you add more volumes to your stack, you need to make sure you add the corresponding constraints to the services that use that named volume.

Then you have to create those labels in some nodes in your Docker Swarm mode cluster. You can use `docker-auto-labels` to do it automatically.

#### `docker-auto-labels`

You can use [`docker-auto-labels`](https://github.com/tiangolo/docker-auto-labels) to automatically read the placement constraint labels in your Docker stack (Docker Compose file) and assign them to a random Docker node in your Swarm mode cluster if those labels don't exist yet.

To do that, you can install `docker-auto-labels`:

```bash
pip install docker-auto-labels
```

And then run it passing your `docker-stack.yml` file as a parameter:

```bash
docker-auto-labels docker-stack.yml
```

You can run that command every time you deploy, right before deploying, as it doesn't modify anything if the required labels already exist.

#### (Optionally) adding labels manually

If you don't want to use `docker-auto-labels` or for any reason you want to manually assign the constraint labels to specific nodes in your Docker Swarm mode cluster, you can do the following:

* First, connect via SSH to your Docker Swarm mode cluster.

* Then check the available nodes with:

```console
$ docker node ls


// you would see an output like:

ID                            HOSTNAME               STATUS              AVAILABILITY        MANAGER STATUS
nfa3d4df2df34as2fd34230rm *   dog.example.com        Ready               Active              Reachable
2c2sd2342asdfasd42342304e     cat.example.com        Ready               Active              Leader
c4sdf2342asdfasd4234234ii     snake.example.com      Ready               Active              Reachable
```

then chose a node from the list. For example, `dog.example.com`.

* Add the label to that node. Use as label the name of the stack you are deploying followed by a dot (`.`) followed by the named volume, and as value, just `true`, e.g.:

```bash
docker node update --label-add fastapi-template-app.app-db-data=true dog.example.com
```

* Then you need to do the same for each stack version you have. For example, for staging you could do:

```bash
docker node update --label-add staging-fastapi-app.app-db-data=true cat.example.com
```

### Deploy to a Docker Swarm mode cluster

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

If you change your mind and, for example, want to deploy everything to a different domain, you only have to change the `DOMAIN` environment variable in the previous commands. If you wanted to add a different version / environment of your stack, like "`preproduction`", you would only have to set `TAG=preproduction` in your command and update these other environment variables accordingly. And it would all work, that way you could have different environments and deployments of the same app in the same cluster.

#### Deployment Technical Details

Building and pushing is done with the `docker-compose.yml` file, using the `docker-compose` command. The file `docker-compose.yml` uses the file `.env` with default environment variables. And the scripts set some additional environment variables as well.

The deployment requires using `docker stack` instead of `docker-swarm`, and it can't read environment variables or `.env` files. Because of that, the `deploy.sh` script generates a file `docker-stack.yml` with the configurations from `docker-compose.yml` and injecting the environment variables in it. And then uses it to deploy the stack.

You can do the process by hand based on those same scripts if you wanted. The general structure is like this:

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

### Continuous Integration / Continuous Delivery

If you use GitLab CI, the included `.gitlab-ci.yml` can automatically deploy it. You may need to update it according to your GitLab configurations.

If you use any other CI / CD provider, you can base your deployment from that `.gitlab-ci.yml` file, as all the actual script steps are performed in `bash` scripts that you can easily re-use.

GitLab CI is configured assuming 2 environments following GitLab flow:

* `prod` (production) from the `production` branch.
* `stag` (staging) from the `master` branch.

If you need to add more environments, for example, you could imagine using a client-approved `preprod` branch, you can just copy the configurations in `.gitlab-ci.yml` for `stag` and rename the corresponding variables. The Docker Compose file and environment variables are configured to support as many environments as you need, so that you only need to modify `.gitlab-ci.yml` (or whichever CI system configuration you are using).

---

# 5. Docker Compose files and env vars

There is a main `docker-compose.yml` file with all the configurations that apply to the whole stack, it is used automatically by `docker-compose`.

And there's also a `docker-compose.override.yml` with overrides for development, for example to mount the source code as a volume. It is used automatically by `docker-compose` to apply overrides on top of `docker-compose.yml`.

These Docker Compose files use the `.env` file containing configurations to be injected as environment variables in the containers.

They also use some additional configurations taken from environment variables set in the scripts before calling the `docker-compose` command.

It is all designed to support several "stages", like development, building, testing, and deployment. Also, allowing the deployment to different environments like staging and production (and you can add more environments very easily).

They are designed to have the minimum repetition of code and configurations, so that if you need to change something, you have to change it in the minimum amount of places. That's why files use environment variables that get auto-expanded. That way, if for example, you want to use a different domain, you can call the `docker-compose` command with a different `DOMAIN` environment variable instead of having to change the domain in several places inside the Docker Compose files.

Also, if you want to have another deployment environment, say `preprod`, you just have to change environment variables, but you can keep using the same Docker Compose files.

### The .env file

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

Depending on your workflow, you could want to exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.

One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.

---

# 6. URLs

These are the URLs that will be used and generated by the project.

### Production URLs
- Production URLs, from the branch `production`.
- Frontend: https://fastapi-app.com
- Backend: https://fastapi-app.com/api/
- Automatic Interactive Docs (Swagger UI): https://fastapi-app.com/docs
- Automatic Alternative Docs (ReDoc): https://fastapi-app.com/redoc
- PGAdmin: https://pgadmin.fastapi-app.com
- Flower: https://flower.fastapi-app.com

### Staging URLs
- Staging URLs, from the branch `master`.
- Frontend: https://staging.fastapi-app.com
- Backend: https://staging.fastapi-app.com/api/
- Automatic Interactive Docs (Swagger UI): https://staging.fastapi-app.com/docs
- Automatic Alternative Docs (ReDoc): https://staging.fastapi-app.com/redoc
- PGAdmin: https://pgadmin.staging.fastapi-app.com
- Flower: https://flower.staging.fastapi-app.com

### Development URLs
- Development URLs, for local development.
- Frontend: http://localhost
- Backend: http://localhost/api/
- Automatic Interactive Docs (Swagger UI): https://localhost/docs
- Automatic Alternative Docs (ReDoc): https://localhost/redoc
- PGAdmin: http://localhost:5050
- Flower: http://localhost:5555
- Traefik UI: http://localhost:8090

### Development with Docker Toolbox URLs
- Development URLs, for local development.
- Frontend: http://local.dockertoolbox.tiangolo.com
- Backend: http://local.dockertoolbox.tiangolo.com/api/
- Automatic Interactive Docs (Swagger UI): https://local.dockertoolbox.tiangolo.com/docs
- Automatic Alternative Docs (ReDoc): https://local.dockertoolbox.tiangolo.com/redoc
- PGAdmin: http://local.dockertoolbox.tiangolo.com:5050
- Flower: http://local.dockertoolbox.tiangolo.com:5555
- Traefik UI: http://local.dockertoolbox.tiangolo.com:8090

### Development with a custom IP URLs
- Development URLs, for local development.
- Frontend: http://dev.fastapi-app.com
- Backend: http://dev.fastapi-app.com/api/
- Automatic Interactive Docs (Swagger UI): https://dev.fastapi-app.com/docs
- Automatic Alternative Docs (ReDoc): https://dev.fastapi-app.com/redoc
- PGAdmin: http://dev.fastapi-app.com:5050
- Flower: http://dev.fastapi-app.com:5555
- Traefik UI: http://dev.fastapi-app.com:8090

### Development in localhost with a custom domain URLs
- Development URLs, for local development.
- Frontend: http://localhost.tiangolo.com
- Backend: http://localhost.tiangolo.com/api/
- Automatic Interactive Docs (Swagger UI): https://localhost.tiangolo.com/docs
- Automatic Alternative Docs (ReDoc): https://localhost.tiangolo.com/redoc
- PGAdmin: http://localhost.tiangolo.com:5050
- Flower: http://localhost.tiangolo.com:5555
- Traefik UI: http://localhost.tiangolo.com:8090

---

# 7. Project generation and updating, or re-generating

This project was generated using https://github.com/tiangolo/full-stack-fastapi-postgresql with:

```bash
pip install cookiecutter
cookiecutter https://github.com/tiangolo/full-stack-fastapi-postgresql
```

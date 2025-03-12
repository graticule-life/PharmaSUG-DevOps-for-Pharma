# PharmaSUG 2025 Sample
Template repository for papermill pipelines.

This repo contains the basic structure for papermill pipelines. The main execution file is `source/papermill.ipynb` which executes Python and R notebooks from `source/notebooks`.


<br>

### Local Set up

1. Create a virtual environment: `python3 -m venv venv`
2. Activate virtual environment: `source venv/bin/activate`
3. Install Python dependencies: `make install`


#### Updating R dependencies

1. Update the package you want to update
    ```r
    renv::update(packages = c("dplyr", "ggplot2"))
    renv::snapshot()
    ```
2. Commit your `renv.lock` file and push your changes

Note that renv will look for necessary packages based on the `Rmd` files in the `source/notebooks` directory. Any `Rmd` files that are not in `source/notebooks` will be ignored by renv via `.renvignore`. To modify what is ignored, edit the `.renvignore` file.

#### Updating Python dependencies

1. Add the package to `pyproject.toml`
2. Run `make install` to install packages from the public PyPI repository
3. Commit your `pyproject.toml` file and push your changes

<br>

### Developer Guide
* Notebooks should be defined in the `source/notebooks` directory
* Helper functions should be defined in `source/notebooks/helpers`
* Default parameter values can be defined or updated in a centralized configuration file: `config.py`
* If adding or updating R dependencies, update `renv.lock` e.g. using `renv::snapshot()`

<br>

### CI / CD
#### Continuous Integration (CI)
Occurs when a PR has been opened or updated

Action:
  * Creates new snowflake schema
    * The PR # is embedded in the snowflake schema
  * Builds new docker image with requirements defined in pyproject.toml and renv.lock
  * Runs the papermill pipeline
  * Writes new tables to snowflake
  * Copies tables to AWS S3 with parquet files along with the Dockerfile and notebooks that were used

<br>

#### Continuous Deployment (CD)
Occurs when a PR has been closed

Action:
  * Renames the snowflake schema by replacing the PR # with the git commit hash (see above in CI)
  * Sets snowflake tables to read only


<br>

---



## Local Docker build and run

Set git commit hash
```bash
export GIT_COMMIT=$(git rev-parse HEAD)
```

Build docker image:
```bash
docker compose build base-image
```

Run in interactive mode:
```bash
docker compose run local-interactive
```

Run papermill notebook:
```bash
docker compose run local-notebook
```


<br>

# Chotot_DA

Note: My Linux distro is Fedora 40

## Using Selenium to crawl data about pet dogs in Ho Chi Minh City, then export to the csv file

Code in file `Crawl_Dog.ipynb`

## SQLite as database engine to store data
Code in insert_data.py to create Processed table in pets_database and insert samples to it.

## Install and set up Apache Superset

1. **Install Dependencies:**
   - `sudo dnf update -y`
   - `sudo dnf install -y @development-tools`
   - `sudo dnf install -y libffi-devel zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils`
2. **Install pyenv:**
   - `curl https://pyenv.run | bash`
3. **Configure Shell:**
   - `echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc`
   - `echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc`
   - `echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init --path)"\nfi' >> ~/.bashrc`
   - `echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc`
4. **Restart Shell:**
   - `exec "$SHELL"`
5. **Install Python 3.9.7 because Apache Superset is compatible with Python ver ~=3.9**
   - `pyenv install 3.9.7`
6. **Make directory for project and set python version**
   - `mkdir superset_project && cd superset_project`
   - `pyenv local 3.9.7`
7. **Create the virtual env and activate it:**
   - `python3.9 -m venv superset_venv`
   - `source superset_venv/bin/activate`

Now I can install apache superset:
- `pip install apache-superset`

Set the Flask app env variable:
- `export FLASK_APP=superset`

Run database upgrade and finish installing by following cmds:
- `superset db upgrade`
- `superset fab create-admin`

### Load some data to play with

- `superset load_examples`

### Create default roles and permissions

- `superset init`

### To start a development web server on port 8088, use -p to bind to another port

- `superset run -p 8088 --with-threads --reload --debugger`

For the case if encounter warning like this: \
------------------WARNING----------------------- \
A Default SECRET_KEY was detected, please use superset_config.py to override it. Use a strong complex alphanumeric string and use a tool to help you generate a sufficiently random sequence, ex: openssl rand -base64 42

**Solution** is:

1. Create `superset_config.py` and place it in project dir, not any subdirs
2. Use `openssl rand -base64 42` to generate a secure secret key and assign it in file config above
   - `SECRET_KEY = 'YOUR_SECURE_SECRET_KEY'`
3. Set Python path env variable for superset to know where to look for config file
   - `export PYTHONPATH=$(pwd)`
   - `export SUPERSET_CONFIG_PATH=$(pwd)/superset_config.py`
4. To prevent from setting up env variables again next time, we create a file named `set_env_vars.sh` in project dir, then add these lines to it
   ```bash
   #!/bin/bash
   export FLASK_APP=superset
   export PYTHONPATH=$(pwd)
   export SUPERSET_CONFIG_PATH=$(pwd)/superset_config.py
   export SECRET_KEY='YOUR_SECURE_SECRET_KEY'

Then run this to make a script executable
- `chmod +x set_env_vars.sh` 
  
and update env variables with
- `source /path/to/your/project/set_env_vars.sh`
## Connect SQLite to Apache Superset for exploring and visualizing
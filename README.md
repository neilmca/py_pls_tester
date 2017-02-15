For running locally
1. Create a python virtual environment 
	virtualenv env
2. Activate the environment
    env\scripts\activate
3. Install packages into this environment
    pip install -r requirements.txt

When Deploying
- Remove file server/lib/flask/ext/setuptools/script (dev).tmpl otherwise get deploy failure


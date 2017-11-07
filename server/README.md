# Python API Server w/ Flask

This example sets up a basic Python API server with Flask. It uses
`Flask-OAuthLib` to authenticate the consumer on it's first request via
`identitypreview.ses.nsw.gov.au`. It then proxies a request to
`https://apipreviewbeacon.ses.nsw.gov.au/Api/v1/Users` which presents the JSON
blob that contains the user's record in Beacon.

## Setup

1. Pre-requisites

First, install a modern Python and virtualenv. On macOS:
```sh
brew install python3
pip install virtualenv
```

2. Clone repo

3. Install
```sh
cd ses-auth-shell/server
virtualenv venv
venv/bin/pip install Flask
venv/bin/pip install Flask-OAuthLib
```

4. Run

```sh
venv/bin/python3 app.py
```

5. Access API with browser
http://localhost:5000/

# License
MIT

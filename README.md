# ADI Website ([https://adicu.com][adi])

[![Build Status](https://travis-ci.org/adicu/adi-website.svg)](https://travis-ci.org/adicu/adi-website)

[ADI][adi] is the tech club at [Columbia][columbia].  The ADI website is built on [Eventum][eventum], a content management system for an event-driven blog that syncs with Google Calendar.

## Stack
- Built in [Flask][flask]
- [Flask-Mongoengine][flask-mongoengine] and [Mongoengine][mongoengine] are used to interface with [MongoDB][mongodb]  
- Authentication is done with [Google+ server-side flow][google-plus-server-side-flow]
- Forms and validation are done through [Flask-WTForms][flask-wtforms] and [WTForms][wtforms]
- CSS is generated from [SCSS][scss] and managed with [Flask-Assets][flask-assets]
- Configurations are managed using [Consul][consul].
- Development is done using [Vagrant][vagrant].
- Deployment is done using [Docker][docker].

## First-Time Setup

Eventum can be run locally on your machine, or in a virtual environment, using [Vagrant][vagrant].  Default to use Vagrant, unless you have some reason to run Eventum locally.

#### Using Vagrant 

1.  Generate secrets files:
    - **ADI:** Download the [ADI website secrets][adi-website-secrets] from GitHub. Unzip the folder, and copy its **contents** into the `config` directory.  

        > If the link gives a 404 error, ask someone within the ADI GitHub organization for access
    
    - **non-ADI:** Copy `config/setup_consul_no_secrets.sh` to `config/setup_consul_dev.sh`, and fill in the four parameters that are set to empty strings.  Then, either setup Google Auth yourself, or [disable it](#disabling-google-auth).

2. Install [Virtual box](https://www.virtualbox.org/wiki/Downloads).

3. Once Vagrant is installed, install [Vagrant][vagrant-install].

#### Without Vagrant

Eventum runs natively on Linux and OSX.  To get it up an running, follow these steps:

1.  Generate secrets files:
    - **ADI:** Download the [ADI website secrets][adi-website-secrets] from GitHub. Unzip the folder, and copy its **contents** into the `config` directory.  

        > If the link gives a 404 error, ask someone within the ADI GitHub organization for access
    
    - **non-ADI:** Copy `config/setup_consul_no_secrets.sh` to `config/setup_consul_dev.sh`, and fill in the four parameters that are set to empty strings.  Then, either setup Google Auth yourself, or [disable it](#disabling-google-auth).
    
2.  Install [MongoDB][mongodb] ([Ubuntu Linux][mongodb-linux], [OSX][mongodb-osx]).

    > On OSX, you may have to run `mkdir /data /data/db` before you can run `mongod` without errors.

3.  Install [VirtualEnv][virtualenv]:
    ```bash
    sudo pip install virtualenv
    ```

4.  Install [Consul][consul-install].

5.  Install SASS gem `gem install sass`
    
    > Otherwise, you will see an intermittent `OSError` 

## Developing

#### Using Vagrant

```bash
vagrant up                      # Wait for installation
vagrant ssh                     # Enter your virtual machine
cd /vagrant                     # Enter your project directory
./config/setup_consul_dev.sh    # Populate Consul with values
python run.py                   # Run the application
```

Finally, go to `localhost:5000` in your web browser.

#### Without Vagrant

```bash
./develop.sh                    # MongoDB, Consul, and Pip
source bin/activate             # Enter the virtual environment
./config/setup_consul_dev.sh    # Populate Consul with values
python run.py                   # Run the application
```

Finally, go to `localhost:5000` in your web browser.

#### Disabling Google Auth

It is possible to run Eventum without logging in using Google+ or authenticating with Google Calendar.  To do so, edit `config/setup_consul_dev.sh` and change the line:

```bash
consul_set GOOGLE_AUTH_ENABLED 'FALSE'
```

to:

```bash
consul_set GOOGLE_AUTH_ENABLED 'TRUE'
```

Then, re-run the consul configurations:

```bash
./config/setup_consul_dev.sh    # Populate Consul with values
```

## Documentation

Eventum uses [Sphinx](http://sphinx-doc.org/) to compile documentation to an HTML website.  This documentation is generated from the source code.

First, enter your development environment.  See "Developing" for more.  Then, generate the docs:

```bash
cd docs
make html                       # Generate docs in /docs/_build/html
cd _build/html
python -m SimpleHTTPServer .    # Host the docs on localhost:8000
```


## Testing

Tests live in the `test` directory, and can be run via `nosetests`.  We also use `flake8` for linting `.py` files.

First, enter your development environment.  See "Developing" for more.  Then, run the tests:

```bash
flake8 app config test script   # Run the flake8 linter on our python files
nosetests --with-progressive    # Run test scripts
```

## Organization / Structure

```bash
.
├── .travis.yml      # Configurations for Travis-CI continuous integration
├── app              # All code related to the running of the app
│   ├── forms        # Flask-WTForms models, used for generating forms in 
│   │                #     HTML and validating input
│   ├── lib          # Misc helpers, tasks, and modular libraries
│   ├── models       # Mongoengine Models
│   ├── routes       # All Flask routes, using Blueprints
│   ├── static       # Static files.  Note: All files in here are public
│   │   ├── css      # CSS
│   │   │   ├── lib  # CSS libraries
│   │   │   └── gen  # CSS generated from SCSS
│   │   ├── img      # Images
│   │   ├── js       # JavaScript files
│   │   └── scss     # Stylesheets
│   ├── templates    # HTML templates
│   └── __init__.py  # All app-wide setup.  Called by `run.py`
├── authorize.py     # Used for authorizing the app with Google Calendar
├── config           # Configuration files
├── data             # Backup data
├── deploy.sh        # Run on our deployment server to deploy a new version
├── develop.sh       # Used for non-Vagrant local Development
├── Dockerfile       # Holds Docker configurations
├── docs             # Eventum documentation, generated using Sphinx
├── log              # Log Files
├── manage.py        # Various scripts. Run `python manage.py` to view usage
├── run.py           # Runs the app!
├── script           # Scripts run by `manage.py` outside of the app
├── test             # Unit tests
└── Vagrantfile      # Configurations for Vagrant
```

[adi]: https://adicu.com
[adi-website-secrets]: https://github.com/adicu/secrets/raw/master/adi-website/config.zip
[columbia]: http://www.columbia.edu
[consul]: https://www.consul.io
[consul-install]: https://www.consul.io/intro/getting-started/install.html
[docker]: http://www.docker.com/
[eventum]: https://github.com/danrschlosser/eventum
[flask]: http://flask.pocoo.org/
[flask-assets]: http://flask-assets.readthedocs.org/en/latest/
[flask-mongoengine]: http://flask-mongoengine.readthedocs.org/en/latest/
[flask-wtforms]: https://flask-wtf.readthedocs.org/en/latest/
[google-developer-console]: https://console.developers.google.com/project/apps~adicu-com/apiui/credential
[google-plus-server-side-flow]: https://developers.google.com/+/web/signin/server-side-flow
[mongodb]: https://www.mongodb.org/
[mongodb-linux]: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-ubuntu/
[mongodb-osx]: http://docs.mongodb.org/manual/tutorial/install-mongodb-on-os-x/#install-mongodb-with-homebrew
[mongoengine]: http://docs.mongoengine.org/
[scss]: http://sass-lang.com/
[virtualenv]: http://virtualenv.readthedocs.org/en/latest/
[wtforms]: http://wtforms.readthedocs.org/en/latest/
[vagrant]: https://www.vagrantup.com
[vagrant-install]: https://www.vagrantup.com/downloads.html

# ADI Website ([https://adicu.com][adi])

[![Build Status](https://travis-ci.org/adicu/adi-website.svg)](https://travis-ci.org/adicu/adi-website)

[ADI][adi] is the tech club at [Columbia][columbia].  The ADI website is built on [Eventum][eventum], a content management system for an event-driven blog that syncs with Google Calendar.

![](https://static.schlosser.io/ss/adi/website.png)

## First-Time Setup

The ADI website runs natively on Linux and OSX.  To get it up an running, follow these steps:

1.  Generate secrets files:
    Download the [ADI website secrets][adi-website-secrets] from GitHub. Unzip the folder, and copy its **contents** into the `config` directory.  

    > If the link gives a 404 error, ask someone within the ADI GitHub organization for access
    
2.  Install [MongoDB][mongodb] ([Ubuntu Linux][mongodb-linux], [OSX][mongodb-osx]).

    > On OSX, you may have to run `mkdir /data /data/db` before you can run `mongod` without errors.

3.  Install [VirtualEnv][virtualenv]:
    ```bash
    sudo pip install virtualenv
    ```

4.  Install SASS gem `gem install sass`
    
    > Otherwise, you will see an intermittent `OSError` 

## Developing

```bash
./develop.sh                  # Setup MongoDB, Virtualenv, and Pip
source bin/activate           # Enter the virtual environment
source config/secrets.dev     # Set your enviornment variables to "development"
python run.py                 # Run the application
```

Finally, go to `localhost:5000` in your web browser.

#### Disabling Google Auth

It is possible to run Eventum without logging in using Google+ or authenticating with Google Calendar.  To do so, edit `config/secrets.dev` and change the line:

```bash
export EVENTUM_GOOGLE_AUTH_ENABLED='TRUE'
```

to:

```bash
export EVENTUM_GOOGLE_AUTH_ENABLED='FALSE'
```

Then, reset the environment variables:

```bash
source config/secrets.dev     # Set your enviornment variables to "development"
```

#### Developing with [Eventum][eventum]

Eventum is the content management system (CMS) that we use to create and edit events, blog posts, user accounts, and more. Eventum is a python package that lives at a different GitHub repository.  If you want to make changes to our admin interface (anything at under `/admin`), you will have to work on both repositories at the same time.  Here's how:

1. Clone both repositories from the same folder. You will now have an `adi-website` folder and an `eventum` folder next to each other.

2. Open two terminal windows:

    **Terminal window 1**

    ```bash
    cd adi-website
    ./develop.sh                  # Setup MongoDB, Virtualenv, and Pip
    source bin/activate           # Enter the virtual environment
    source config/secrets.dev     # Set your enviornment variables
    cd ../eventum
    python setup.py develop       # Use this local version of Eventum.
    ```

    This last command will run once and exit. But if it runs without errors, ADI Website will use the local version of the `eventum` package.  If you make changes in the `/eventum` folder, they will be reflected live.

    **Terminal window 2**

    ```bash
    cd adi-website
    source bin/activate           # Enter the virtual environment
    python run.py                 # Run the ADI Website.
    ```

## Deployment

_Note: In order to deploy the ADI website, you must have SSH access to our DigitalOcean server (instructions below)._

First, add our DigitalOcean server as a Git remote:

```bash
git remote add deploy adi-website:~/adi-website.git
```

Then, you should be able to deploy using Git:

```bash
git push deploy master
```

#### Getting SSH Access

1. You need SSH keys. [Check for existing keys](https://help.github.com/articles/checking-for-existing-ssh-keys/) and if you don't have an `~/.ssh/id_rsa` file and a `~/.ssh/id_rsa.pub` file, [create them](https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/#generating-a-new-ssh-key).

2. Next, create or edit `~/.ssh/config`.  Add the following lines:

    ```
    Host adi-website
      HostName 162.243.116.41
      User root
      IdentityFile ~/.ssh/id_rsa
    ```

    This creates an ssh alias called `adi-website`, that allows us to easily log into this server.

3. Next, send your public key (`~/.ssh/id_rsa.pub`) to someone who has access to the server.

    > Protip, you can type `cat ~/.ssh/id_rsa.pub | pbcopy` to copy it to your clipboard.

4. On the server, they should append your public key to the `~/.ssh/authorized_keys` file.

5. Then you should be done!  To test it out, try logging in:

    ```
    ssh adi-website
    ```
    
    You shouldn't need any password or any additional steps.

#### How our deployment works:

Here's a short intro into what happens when you type `git push deploy master`.

1. The lastest changes are pushed to our DigitalOcean server, into a git repo located at `~/adi-website.git`.
2. Once that git repo receives the changes, it runs a script we wrote, called `~/adi-website.git/hooks/post-receive`.  This script copies the latest changes into the folder where the live code is (`/srv/adi-website/www/`).
3. Then, that script changes directory to the root of our project, and runs `./deploy.sh`, which kills the live docker container, and builds a new one with the new code.

## Testing

#### _Warning: Our tests need some love, and may be broken..._

Tests live in the `test` directory, and can be run via `nosetests`.  We also use `flake8` for linting `.py` files.

First, enter your development environment.  See "Developing" for more.  Then, run the tests:

```bash
flake8 app config test script   # Run the flake8 linter on our python files
nosetests --with-progressive    # Run test scripts
```

## About ADI Website

#### Tech Stack
- Built in [Flask][flask], using [Eventum][eventum] as a CMS.
- [Flask-Mongoengine][flask-mongoengine] and [Mongoengine][mongoengine] are used to interface with [MongoDB][mongodb]  
- Authentication is done with [Google+ server-side flow][google-plus-server-side-flow]
- Forms and validation are done through [Flask-WTForms][flask-wtforms] and [WTForms][wtforms]
- CSS is generated from [SCSS][scss] and managed with [Flask-Assets][flask-assets]
- Deployment is done using [Docker][docker].

#### Organization / Structure

```bash
.
├── .travis.yml      # Configurations for Travis-CI continuous integration
├── app              # All code related to the running of the app
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
├── config           # Configuration files
├── data             # Backup data
├── deploy.sh        # Run by our deployment server to deploy a new version
├── develop.sh       # Used for non-Vagrant local Development
├── Dockerfile       # Holds Docker configurations
├── manage.py        # Various scripts. Run `python manage.py` to view usage
├── run.py           # Runs the app!
├── script           # Scripts run by `manage.py` outside of the app
└── test             # Unit tests
```

[adi]: https://adicu.com
[adi-website-secrets]: https://github.com/adicu/secrets/raw/master/adi-website/config.zip
[columbia]: http://www.columbia.edu
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

Digital Helsinki CMS
====================

[![Build status](https://travis-ci.org/City-of-Helsinki/digihel.svg?branch=master)](https://travis-ci.org/City-of-Helsinki/digihel)
[![codecov](https://codecov.io/gh/City-of-Helsinki/digihel/branch/master/graph/badge.svg)](https://codecov.io/gh/City-of-Helsinki/digihel)
[![Requirements](https://requires.io/github/City-of-Helsinki/digihel/requirements.svg?branch=master)](https://requires.io/github/City-of-Helsinki/digihel/requirements/?branch=master)
[![Stories in Ready](https://badge.waffle.io/City-of-Helsinki/digihel.svg?label=ready&title=Ready)](http://waffle.io/City-of-Helsinki/digihel)


This [Wagtail](https://wagtail.io/)-based CMS powers the [Digital Helsinki](http://digi.hel.fi) website.

Installation
------------

Set the DEBUG environment variable to 1

```
export DEBUG=1
```

Install required Python packages

```
(sudo) pip install -r requirements.txt
```

Create the database

```
sudo -u postgres createuser digihel
sudo -u postgres createdb -O digihel digihel
```

Install node dependencies

```
npm install
```

Install bower components

```
./manage.py bower install
```

If you have acquired a database dump, install it this way:

```
tar xvjf digihel-backup.tar.bz2
pg_restore -d digihel digihel.sql
echo "delete from wagtailimages_rendition;" | ./manage.py dbshell
```

Requirements
------------

This project uses two files for requirements. The workflow is as follows.

`requirements.txt` is not edited manually, but is generated
with `pip-compile`.

`requirements.txt` always contains fully tested, pinned versions
of the requirements. `requirements.in` contains the primary, unpinned
requirements of the project without their dependencies.

In production, deployments should always use `requirements.txt`
and the versions pinned therein. In development, new virtualenvs
and development environments should also be initialised using
`requirements.txt`. `pip-sync` will synchronize the active
virtualenv to match exactly the packages in `requirements.txt`.

In development and testing, to update to the latest versions
of requirements, use the command `pip-compile`. You can
use [requires.io](https://requires.io) to monitor the
pinned versions for updates.

To remove a dependency, remove it from `requirements.in`,
run `pip-compile` and then `pip-sync`. If everything works
as expected, commit the changes.

Configuration
-------------

These settings are recognized in the Django settings.

You can acquire the Twitter keys from the Twitter developer portal (https://apps.twitter.com).

* `TWITTER_CONSUMER_KEY`: "Consumer Key (API Key)"
* `TWITTER_CONSUMER_SECRET`: "Consumer Secret (API Secret)"
* `TWITTER_ACCESS_TOKEN`: A personal (read-only) access token
* `TWITTER_ACCESS_TOKEN_SECRET`: The secret for the personal (read-only) access token

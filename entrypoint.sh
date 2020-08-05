#!/usr/bin/env bash

set -e
set -x

export DEBIAN_FRONTEND=noninteractive

ROOT=/imager
ENV=$ROOT/env
PY=$ENV/bin/python
PROJ=$ROOT/imager
MANAGE=$PROJ/manage.py

if [ ! -d "$ENV/bin" ] ; then
    mkdir -p $ROOT
    chmod -R a+rwx $ROOT
    pip install virtualenv
    virtualenv -p python3.8 $ENV
    $ENV/bin/pip install -U pip setuptools
fi

cd $PROJ

$ENV/bin/pip install -r requirements.txt
$PY $MANAGE migrate
$PY $MANAGE collectstatic --noinput
$ENV/bin/daphne -b 0.0.0.0 -p 8000 imager.asgi:application

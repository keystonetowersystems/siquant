#!/usr/bin/env bash

BASEDIR=$(dirname "$0")

rm -r ${BASEDIR}/../dist/
rm -r ${BASEDIR}/../build/
rm -r ${BASEDIR}/../*.egg-info/
rm -r ${BASEDIR}/../.eggs/
rm -r ${BASEDIR}/../.tox/
rm -r ${BASEDIR}/../.pytest_cache/

rm ${BASEDIR}/../.coverage

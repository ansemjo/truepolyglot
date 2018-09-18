#!/bin/bash
rsync -av --progress ./ -e ssh dragon:/var/www/html/truepolyglot/

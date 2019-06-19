#!/bin/bash
python3 ../manage.py collectstatic
ls ../static/resdig/js/
echo 'compileing...'
java -jar compiler.jar --js ../static/resdig/js/*.js   --js_output_file core.js
rm ../static/resdig/js/*
cp core.js ../static/resdig/js/
rm core.js
echo 'done!'
./fullstart

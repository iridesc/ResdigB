#!/bin/bash
pwd
echo del core.js...
ls ../resdig/static/resdig/js
echo 'cp all js to here...'
cp ../resdig/static/resdig/js/*js ../Encrypthon
echo 'compileing...'
java -jar compiler.jar --js **.js   --js_output_file core.js

echo 'done!'

#!/bin/bash

cd /home/jovyan/work

export GIT_COMMITTER_NAME=anonymous
export GIT_COMMITTER_EMAIL=anon@localhost

git clone https://github.com/hfst/compmorph-course.git
cd /home/jovyan
cp -r /home/jovyan/work/compmorph-course/* /home/jovyan/

python3 -m pip install graphviz
python3 -m pip install hfst-dev

rm -fR src
rm -fR work
rm -fR doc

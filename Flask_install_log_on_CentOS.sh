ls
pwd
mkdir downloads
ls
cd downloads/
wget http://pypi.python.org/packages/source/F/Flask/Flask-0.9.tar.gz
ls
tar -zxv -f Flask-0.9.tar.gz
ls
cd Flask-0.9
ls
cd ..
ls
wget https://bootstrap.pypa.io/ez_setup.py -O - | python
ls
cd Flask-0.9
ls
python setup.py install
ls
cd ..
ls
cd code/

if [[ $TRAVIS_OS_NAME == 'osx' ]]; then
    brew update;
    brew install freetype;
    brew install python3;
    brew tap Homebrew/python
    pip3 install -U pip wheel;
    pip3 install --only-binary=numpy numpy;
    pip3 install -r requirements.txt;
else
    pip3 install -U pip wheel;
    pip3 install --only-binary=numpy numpy;
    pip3 install --only-binary=matplotlib matplotlib;
    brew link matplotlib --force
    pip3 install -r requirements.txt;
fi

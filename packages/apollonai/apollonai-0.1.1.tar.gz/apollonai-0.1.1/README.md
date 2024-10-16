# ApollonAI


Setup Library
```bash
python setup.py sdist bdist_wheel
```

Locally install
```bash 
pip install .
```

Install twine into the virtual env

```bash
pip install twine
```

Upload to pip package manager
```bash
twine upload dist/*
```
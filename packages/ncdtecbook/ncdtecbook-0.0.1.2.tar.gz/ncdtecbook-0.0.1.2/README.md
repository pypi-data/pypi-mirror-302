# ncd-tec-book



[ncd-teck-book](https://suhelhammoud.github.io/ncd-tec-book)


### Example Package

### build using hatchling
```bash
python -m build
# or
hatchling build
```

### publish using twine
```bash
python -m build
twine upload dist/*
```

### publish to testpypi
```bash
python -m build
twine upload --repository testpypi dist/*
```

### installing pypi library from testpypi
```
pip install -i https://test.pypi.org/simple/ ncdtecbook
```


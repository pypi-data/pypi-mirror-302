# vnpy_chart

enhanced chart for vnpy

## tips

If you encounter issues while installing [ta-lib](https://github.com/TA-Lib/ta-lib-python), try:

```sh
pip install numpy==1.26.4 importlib_metadata
pip install --extra-index-url https://pypi.vnpy.com TA_Lib==0.4.24
```

## dev

### run test

```sh
pip install .
python -m unittest discover -s tests
```

### publish

build

```sh
pip install --upgrade build

python -m build
```

upload to testpypi

```sh
pip install --upgrade twine

python -m twine upload --repository testpypi dist/*
```

upload to pypi

```sh
python -m twine upload dist/*
```

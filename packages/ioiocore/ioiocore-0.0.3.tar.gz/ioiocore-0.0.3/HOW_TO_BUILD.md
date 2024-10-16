# Buld instructions
## Prerequisites
- Visual Studio Code<br>
&nbsp;&nbsp;&nbsp; - Python (Microsoft) v2024.16.1 Extension<br>
&nbsp;&nbsp;&nbsp; - Python Debugger (Microsoft) v2024.10.00<br>
&nbsp;&nbsp;&nbsp; - Pylance (Microsoft) v2024.10.01 Extension<br>
&nbsp;&nbsp;&nbsp; - Markdown Preview Github Styling (Matt Bierner) v2.1.0 Extension<br>
- Python >= 3.11<br>
&nbsp;&nbsp;&nbsp; - pip (must be accessible from commandline)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Note**: ensure that the pip package is installed ```python -m ensurepip --upgrade```<br>
&nbsp;&nbsp;&nbsp; - pipreqs (must be accessible from commandline)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Note**: ensure that the pipreqs package is installed ```pip install pipreqs```<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Note**: ensure that the twine package is installed ```pip install twine```<br>
&nbsp;&nbsp;&nbsp; - build (must be accessible from commandline)<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Note**: ensure that the build package is installed ```pip install build```<br>
&nbsp;&nbsp;&nbsp; - setuptools<br>
&nbsp;&nbsp;&nbsp; - numpy (for tests only)<br>

## Create requirements file

Create or update requirements.txt<br>
```pipreqs ./ioiocore --force```

## Build
Update version number:<br>
```./ioiocore/___version__.py```

build wheel:<br>
```python -m build```<br>
distributables are built to the ```./dist``` folder

### Upload to pypi
Upload to pypi using the following command: <br>
```python -m twine upload --repository pypi dist/*```

API token: pypi-AgEIcHlwaS5vcmcCJDcxN2FhNmYzLTM1MzQtNGUyMS04MDI2LTI5NzQ4MTk3MDAyYQACKlszLCJmYWZmN2JkMC1lNTBlLTRkOTUtYmY5NC01MTFjNTQzNGY1YzMiXQAABiACrvmxaUzjvzTBqZtlzwe6dzMId1Kp-7_l7vrMO69mYA

## Installation
### Manual installation
Copy ```.whl``` file from  ```./dist``` folder and install from command line: <br>
```pip install ./dist/ioiocore-0.0.2-py3-none-any.whl```

### Installation using PyPi
Package can be downloaded, installed and updated via pypi if uploaded ([Upload to pypi](#upload-to-pypi)).<br>
```pip install ioiocore```<br>
```pip install ioiocore --upgrade```

### Uninstall
```pip uninstall ioiocore```

## Run tests
Go to project base folder and execute:<br>
```python ./test/run_all.py```
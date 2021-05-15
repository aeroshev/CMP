# CMP
This's compiler MATLAB to python

# Install from PYPI
Before install depencies
```shell
pip install ply==3.11
```
After install package
```shell
pip install pycmp
```
Homepage on PYPI - https://pypi.org/project/pycmp/0.1.0/

# Install CMP
Base require `Python 3.9` or newer

```shell
git clone https://github.com/aeroshev/CMP.git | cd cmp
pip install .
```

### Get help by package
```shell
$ pycmp -h
usage: pycmp [-h] (-p PATH | -s STRING | -S) [-of OUTPUT_FILE] [-v] [-P PORT] [-H HOST]

Compiler MATLAB code to Python scripts

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  path to file
  -s STRING, --string STRING
                        input data from console
  -S, --server          Run async TCP server
  -of OUTPUT_FILE, --output-file OUTPUT_FILE
                        path to output file
  -v, --version         show program's version number and exit
  -P PORT, --port PORT  Port of server
  -H HOST, --host HOST  Hostname of server
```

### Run TCP Server
```shell
pycmp -S [-H/--host host] [-P/--port port]
```

# Install TCP client
Client is available by name `tcmp`
```shell
pip install cmp/helpers/server 
```

### Get help
```shell
$ tcmp -h
usage: tcmp [-h] (-d DATA | -f FILE) [-p PORT] [-a ADDRESS]

TCP client for server MATLAB compiler

optional arguments:
  -h, --help            show this help message and exit
  -d DATA, --data DATA  input data for compiler from console
  -f FILE, --file FILE  input data for compiler from file
  -p PORT, --port PORT  Port of connection server
  -a ADDRESS, --address ADDRESS
                        Address of connection server

```

### Run TCP Client
```shell
tcmp --data 'a = [1; 2; 3];'
```

## Check tests
```shell
pipenv shell
pipenv install --dev
cd tests
pytest
```

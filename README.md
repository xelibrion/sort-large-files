# sort-large-files

## How to run

First, it is required to install the project into virtual environment:

```
pip install -e .
```


Once you've done that, there will be two commands available, for generating a file with random strings and for sorting it.

To generate a file, run:

```
sort-large-files generate 2000000 120
```

To sort the generated file, run:

```
sort-large-files sort --sort-max-memory-mb 2 --merge-max-files 50
```

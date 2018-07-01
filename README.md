# Unoccupied

Find an unoccupied name from basename & occupied names.



## Usage

### Basic Usage

Use `basename` and `occupied` container (an iterable) to find a unoccupied name:

```python3
from unoccupied import unoccupied

basename = 'foo'



unoccupied(basename, [])  # 'foo' not be occupied
# >>> 'foo'

unoccupied(basename, ['foo'])  # 'foo' already be occupied
# >>> 'foo-1'

unoccupied(basename, ['foo', 'foo-1'])  # 'foo' & 'foo-1' already be occupied
# >>> 'foo-2'
```



### Name Finder

Name finder offer an algorithm to find (or generate) an unoccupied name.

Let's try to change the default name finder:

```python3
from unoccupied import unoccupied
from unoccupied import NumberNameFinder  # A built-in name finder generator

# test data
basename = 'foo'
occupied = ['foo', 'bar', 'foo-1']



unoccupied(basename, occupied)  # use defualt name finder
# >>> 'foo-2'

name_finder = NumberNameFinder(template='{basename}-{num:02}')  # <- look here
unoccupied(basename, occupied, name_finder)
# >>> 'foo-01'
```

Another case: Assume we need to find an unoccupied filename, but, we don't want the base filename `foo.txt` become `foo.txt-1`. The `foo-1.txt` is much suitable name. Try the built-in `FileNameFinder()`.

```python3
from unoccupied import unoccupied
from unoccupied import FileNameFinder  # here

# test data
basename = 'pic.jpg'
occupied = ['pic.jpg', 'pic-1.jpg', 'foo']  # may use os.listdir() in real case



unoccupied(basename, occupied, FileNameFinder())  # <- look here
# >>> 'pic-2.jpg'

name_finder = FileNameFinder(template='{base}.{num:02}', start=0)
unoccupied(basename, occupied, name_finder)
# >>> 'pic.00.jpg'
```



#### Build a Name Finder

A `name_finder` is just a callable accept 2 arguments: (`basename`, `occupied`), so feel free to build your own. e.g.:

```python3
import string
from unoccupied import unoccupied

def alphabet_name_finder(basename, occupied):
    for char in string.ascii_lowercase:
        testing_name = '{}-{}'.format(basename, char)
        if testing_name not in occupied:
            return testing_name

unoccupied('foo', ['foo'], alphabet_name_finder)
# >>> 'foo-a'
```



## Reference

### unoccupied(basename, occupied, name_finder=NumberNameFinder(), nobase=False)

Find a unoccupied name.

- `basename`: (str) the wanted basename.
- `occupied`: (str of iterable) the names already be occupied.

`name_finder` is a callable with 2 arguments (`basename`, `occupied`). This function only be called when `basename` cannot use directly, and it should return `None` or `str`. Return `None` mean cannot find any unoccupied name and cause `unoccupied()` raise `UnoccupiedNameNotFound` exception.

> Hint: Before call the `name_finder`, `occupied` will be convert to `frozenset` data type internally. If and only if you try to build a name_finder by yourself, you may need to know that.

`nobase` is a boolean value. It request do not use `basename` as return directly, no matter `basename` already in `occupied` or not.



### NumberNameFinder(template='{basename}-{num}', start=1)

Generate a `name_finder` to find an unoccupied name with `basename` and an increasing number.

The `template` argument is a python `str.format()` template. This template can include 2 keyword params. `{basename}` represent the original `basename`. `{num}` represent an increasing number.

`start` argument can define what `{num}` starts from.



### FileNameFinder(template='{base}-{num}', start=1)

Generate a `name_finder` to find an unoccupied name with processed filename and an increasing number.

The `template` argument is a python `str.format()` template. This template can include 2 keyword params. `{base}` represent the filename without extension. `{num}` represent an increasing number. Hint: the filename extension will be appended automatically.

`start` argument can define what `{num}` starts from.



## Test

```sh
./setup.py test  # or pytest
```


## Install

```sh
pip install unoccupied
```

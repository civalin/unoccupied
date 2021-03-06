# Unoccupied

[![Build Status](https://travis-ci.org/visig9/unoccupied.svg?branch=master)](https://travis-ci.org/visig9/unoccupied)

Find an unoccupied name by `basename` & `occupied names`.

If you tired to write a bunch of code to deal `unnamed note 02`, `pic-03.jpg`, `archive.part4.zip` naming problem. It's for you.



## Features

- Based on basename: find an unoccupied name as close as user wanted, not randomly.
- Isolated: pure functional API, no related any outer environment like filesystem or DB.
- Stable: consider edge situations and already be tested.
- Flexible: library user can choice / overwrite naming algorithm easily.



## Usage

### Basic Usage

Use `basename` and `occupied` container (an iterable) to find a unoccupied name:

```python
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

```python
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

```python
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

A `name_finder` is just a callable accept 2 arguments: (`basename`, `norm_occupied`), so feel free to build your own. e.g.:

```python
import string
from unoccupied import unoccupied

def alphabet_name_finder(basename, norm_occupied):
    for char in string.ascii_lowercase:
        testing_name = '{}-{}'.format(basename, char)
        if testing_name not in norm_occupied:
            return testing_name

unoccupied('foo', ['foo'], alphabet_name_finder)
# >>> 'foo-a'
```

Or, using `BaseNameFinder` class to build a `name_finder`:

```python
import string
from unoccupied import unoccupied
from unoccupied import BaseNameFinder


class AlphabetNameFinder(BaseNameFinder):
    """Basic alphabet name finder."""
    def ids_generator(self):
        return string.ascii_lowercase

alphabet_name_finder = AlphabetNameFinder()

unoccupied('foo', ['foo'], alphabet_name_finder)
# >>> 'foo-a'


class AlphabetNameFinder2(BaseNameFinder):
    """Configurable alphabet name finder."""
    def __init__(self, template):       # here is a configurable option.
        self.template = template

    def ids_generator(self):
        return string.ascii_lowercase

    def formatter(self, basename, id):  # change formatting algorithm
        return self.template.format(basename=basename, id=id)

alphabet_name_finder2 = AlphabetNameFinder2(template='{basename}.{id}')

unoccupied('foo', ['foo'], alphabet_name_finder2)
# >>> 'foo.a'
```

As you see. `BaseNameFinder` packed some tedious work like for-loop & infinite loop checking. And good for offer some configurable options for further usage.



## Reference

### function unoccupied(basename, occupied, name_finder=NumberNameFinder(), skipbase=False)

Find a unoccupied name.

- `basename`: (str) the wanted basename.
- `occupied`: (str of iterable) the names already be occupied.

`name_finder` is a callable with 2 arguments (`basename`, `norm_occupied`). This function only be called when `basename` cannot use directly, and it should return `None` or string. Return `None` mean it can't find any unoccupied name and cause `unoccupied()` raise `UnoccupiedNameNotFound` exception.

> Hint: `occupied` will be convert to `frozenset` data type (we call it `norm_occupied`) and inject to `name_finder`. If and only if you try to build a `name_finder` by yourself, you may need to know that.

`skipbase` is a boolean value. If `True`, `basename` will never return directly, no matter the `basename` already in `occupied` or not. So user can generate a consistent name series like `pic-01`, `pic-02` and without `pic`.



### class BaseNameFinder()

This is the base class of built-in NameFinder class. It has 2 method which can (but not necessary) be overwrited:



#### method ids_generator(self) -> Iterable

This method will create a series of `id` and push into `self.formatter()`.



#### method formatter(self, basename, id) -> str

This method can assemble `basename` and `id` then return a string by any algorithm.



### class NumberNameFinder(template='{basename}-{num}', start=1)

Generate a `name_finder` to find an unoccupied name with `basename` and an increasing number.

The `template` argument is a python `str.format()` template. This template can include 2 keyword params. `{basename}` represent the original `basename`. `{num}` represent an increasing number.

`start` argument can define what `{num}` starts from.



### class FileNameFinder(template='{base}-{num}', start=1)

Generate a `name_finder` to find an unoccupied name with processed filename and an increasing number.

The `template` argument is a python `str.format()` template. This template can include 2 keyword params. `{base}` represent the filename without extension. `{num}` represent an increasing number. Hint: the filename extension will be appended automatically.

`start` argument can define what `{num}` starts from.



## Test

```sh
pip install -r test_requirements.txt
pytest
```


## Install

```sh
pip install unoccupied
```

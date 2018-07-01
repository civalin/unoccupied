# Unoccupied

Generate unoccupied name(s) from basename & occupied name list.



## Usage

Use `basename` and `occupied` container (a iterable) to find a unoccupied
name:

```python3
from unoccupied import unoccupied

basename = 'foo'

unoccupied(basename, [])
# >>> 'foo'

unoccupied(basename, ['foo'])  # 'foo' already be occupied
# >>> 'foo-1'

unoccupied(basename, ['foo', 'foo-1'])  # 'foo' & 'foo-1' already be occupied
# >>> 'foo-2'
```

Nice hmm? Now try to change the default `name_finder`:

```python3
from unoccupied import unoccupied
from unoccupied import NumberNameFinder

basename = 'foo'
occupied = ['foo', 'bar', 'foo-1']

unoccupied(basename, occupied)
# >>> 'foo-2'

name_finder = NumberNameFinder(template='{basename}-{num:02}')
unoccupied(basename, occupied, name_finder)
# >>> 'foo-01'
```

Another example: Assume we need a unoccupied filename.

```python3
from unoccupied import unoccupied
from unoccupied import FileNameFinder

basename = 'pic.jpg'
occupied = ['pic.jpg', 'pic-1.jpg', 'foo']  # may use os.listdir() in real case

unoccupied(basename, occupied, FileNameFinder())
# >>> 'pic-2.jpg'

name_finder = FileNameFinder(template='{base}.{num:02}', start=0)
unoccupied(basename, occupied, name_finder)
# >>> 'pic.00.jpg'
```

A `name_finder` is just a callable accept 2 arguments: (`basename`, `occupied`),
so feel free to build your own. e.g.,

```python3
import string

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

Get a unoccupied name.

- `basename`: (str) the wanted basename.
- `occupied`: (str of iterable) the names already be occupied.

`name_finder` is a callable with 2 arguments (`basename`, `occupied`). This function only be called when `basename` cannot use directly, and it should return `None` or `str`. Return `None` mean cannot find any unoccupied name and cause `unoccupied()` raise `UnoccupiedNameNotFound` exception.

`nobase` is a boolean value. It request do not use `basename` as return directly, no matter `basename` already in `occupied` or not.



### NumberNameFinder(template='{basename}-{num}', start=1)

Find a new name by `basename` and a increasing number.

The `template` is a python `str.format()` template. This template can include 2 keyword params: `{basename}` & `{num}` which represent `basename` & increasing number.

`start` argument can define what `{num}` starts from.



### FileNameFinder(template='{base}-{num}', start=1)

Find a new name by Auto processed filename extension and a increasing number.

The `template` is a python `str.format()` template. This template can include 2 keyword params: `{base}` & `{num}` which represent a filename without extension & increasing number.

`start` argument can define what `{num}` starts from.

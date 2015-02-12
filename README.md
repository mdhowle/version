# Version
A Python 3 class that parses version numbers to allow for comparison.

## Attributes
**version**  &mdash; The version data as given.  Set this value to parse the version given.

**parsed_version** (read-only) &mdash;  A tuple of the version elements parsed (e.g., ```'1.0.0a'``` returns ```(1, 0, 0, 'a')```).

**delimiters** &mdash; A set of values to be used as boundaries; defaults to {'.'}.


# Examples
```python
>>> from version import Version
>>> v = Version('1.0.0a')
>>> v.parsed_version
(1, 0, 0, 'a')
>>> v.version
'1.0.0.a'  # the original input
>>> version_2 = float(2.0)
>>> v2 = Version(version_2)
>>> v2.parsed_version
(2, 0)
>>> v2 > v
True
```


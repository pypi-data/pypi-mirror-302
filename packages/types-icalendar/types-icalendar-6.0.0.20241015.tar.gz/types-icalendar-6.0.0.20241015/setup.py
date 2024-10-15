from setuptools import setup

name = "types-icalendar"
description = "Typing stubs for icalendar"
long_description = '''
## Typing stubs for icalendar

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`icalendar`](https://github.com/collective/icalendar) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`icalendar`.

This version of `types-icalendar` aims to provide accurate annotations
for `icalendar==6.0.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/icalendar. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`a871efd90ca2734b3341dde98cffab66f3e08cee`](https://github.com/python/typeshed/commit/a871efd90ca2734b3341dde98cffab66f3e08cee) and was tested
with mypy 1.11.2, pyright 1.1.383, and
pytype 2024.10.11.
'''.lstrip()

setup(name=name,
      version="6.0.0.20241015",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/icalendar.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-python-dateutil', 'backports.zoneinfo; python_version < "3.9"'],
      packages=['icalendar-stubs'],
      package_data={'icalendar-stubs': ['__init__.pyi', 'cal.pyi', 'caselessdict.pyi', 'parser.pyi', 'parser_tools.pyi', 'prop.pyi', 'timezone/__init__.pyi', 'timezone/provider.pyi', 'timezone/pytz.pyi', 'timezone/tzp.pyi', 'timezone/windows_to_olson.pyi', 'timezone/zoneinfo.pyi', 'tools.pyi', 'version.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)

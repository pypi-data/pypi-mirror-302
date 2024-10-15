__version__ = '0.0.0.dev63'
__revision__ = '6de2b8280b36325b4e4b319adfe01b6a284bbdcc'


#


class ProjectBase:
    name: str | None = None
    authors = [{'name': 'wrmsr'}]
    urls = {'source': 'https://github.com/wrmsr/omlish'}
    license = {'text': 'BSD-3-Clause'}
    requires_python = '~=3.12'

    version = __version__

    classifiers = [
        'License :: OSI Approved :: BSD License',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',

        'Operating System :: OS Independent',
        'Operating System :: POSIX',
    ]


class Project(ProjectBase):
    name = 'omlish'
    description = 'omlish'

    #

    optional_dependencies = {
        'async': [
            'anyio ~= 4.6',
            'sniffio ~= 1.3',

            'greenlet ~= 3.1',

            'trio ~= 0.26',
            'trio-asyncio ~= 0.15',
        ],

        'compress': [
            'lz4 ~= 4.3',
            # 'lz4 @ git+https://github.com/wrmsr/python-lz4@wrmsr_20240830_GIL_NOT_USED'

            'python-snappy ~= 0.7; python_version < "3.13"',

            'zstd ~= 1.5',
        ],

        'diag': [
            'asttokens ~= 2.4',
            'executing ~= 2.1',

            'psutil ~= 6.0',
        ],

        'formats': [
            'orjson ~= 3.10',
            'ujson ~= 5.10',

            'json5 ~= 0.9',

            'pyyaml ~= 6.0',

            'cbor2 ~= 5.6',

            'cloudpickle ~= 3.0',
        ],

        'http': [
            'httpx[http2] ~= 0.27',
        ],

        'misc': [
            'wrapt ~= 1.14',
        ],

        'secrets': [
            'cryptography ~= 43.0',
        ],

        'sqlalchemy': [
            'sqlalchemy[asyncio] ~= 2.0',
        ],

        'sqldrivers': [
            'pg8000 ~= 1.31',
            # 'psycopg2 ~= 2.9',
            # 'psycopg ~= 3.2',

            'pymysql ~= 1.1',
            # 'mysql-connector-python ~= 9.0',
            # 'mysqlclient ~= 2.2',

            'aiomysql ~= 0.2',
            'aiosqlite ~= 0.20',
            'asyncpg ~= 0.29; python_version < "3.13"',

            'apsw ~= 3.46',

            'sqlean.py ~= 3.45; python_version < "3.13"',

            'duckdb ~= 1.1',
        ],

        'testing': [
            'pytest ~= 8.0',
        ],
    }

    #

    _plus_dependencies = [
        'anyio',
        'sniffio',

        'asttokens',
        'executing',

        'orjson',
        'pyyaml',

        'wrapt',
    ]

    _dependency_specs_by_name = (lambda od: {  # noqa
        s.split()[0]: s
        for l in od.values() for s in l
    })(optional_dependencies)

    optional_dependencies['plus'] = (lambda ds, pd: [  # noqa
        ds[n] for n in pd
    ])(_dependency_specs_by_name, _plus_dependencies)

    #

    entry_points = {
        'omlish.manifests': {name: name},
    }


#


class SetuptoolsBase:
    manifest_in = [
        'global-exclude **/conftest.py',
    ]

    find_packages = {
        'exclude': [
            '*.tests',
            '*.tests.*',
        ],
    }

    package_data = {
        '*': [
            '*.c',
            '*.cc',
            '*.cu',
            '*.g4',
            '*.h',

            '.manifests.json',

            'LICENSE',
        ],
    }


class Setuptools(SetuptoolsBase):
    find_packages = {
        'include': [Project.name, f'{Project.name}.*'],
        'exclude': [*SetuptoolsBase.find_packages['exclude']],
    }

import argparse
import importlib.metadata

from .subparser import QueryParser, RegisterParser, SyncParser


class RootParser:
    def __init__(self):
        # Top-level parser
        parser = argparse.ArgumentParser(
            description='''Manage and sync dotfiles across multiple hosts.

By default, folder '~/.dotfiles' will be used as database directory, you can
change it by setting the environment variable `DOTFILES_DIR`.
            ''',
            formatter_class=argparse.RawTextHelpFormatter,
        )
        parser.add_argument(
            '-v',
            '--version',
            action='version',
            version=importlib.metadata.version('dotfile_manager_aquanjsw'),
        )
        subparsers = parser.add_subparsers(title='commands', description='')
        RegisterParser(
            parser=subparsers.add_parser(
                'register', help='Register a new entity', aliases=['r']
            ),
        )
        QueryParser(
            parser=subparsers.add_parser(
                'query',
                help='Query all the database',
                aliases=['q'],
                description='Query all the database',
            ),
        )
        SyncParser(
            parser=subparsers.add_parser(
                'sync',
                help='Sync dotfiles across hosts',
                aliases=['s'],
                description='''Sync dotfiles across hosts.

Depending on whether the `host` argument (the first element of `filter`) is
provided or not, the sync operation will be completely different:

- If `host` is not provided, it will update current host's dotfiles to repo.
  We call this operation *sync-self* for later reference.
- If `host` is provided, it will update current host's dotfiles with the 
  provided host's ones (*sync-host*). Note that *sync-self* will be performed
  first before this operation. Still note that after *sync-host*, the dotfiles
  in this repo may be **outdated** than your current dotfiles.
  But if the provided host is the same as the current host, *sync-self* will
  be skipped. This operation is called *restore-self*.
                ''',
                formatter_class=argparse.RawTextHelpFormatter,
            ),
        )
        parser.set_defaults(func=lambda *_: parser.print_help())

        self._parser = parser

    def get(self):
        return self._parser

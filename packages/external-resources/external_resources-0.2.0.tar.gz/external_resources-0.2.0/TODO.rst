#. dry-run, verbose, force etc. must be taken out of the conf data structure again

#. download all: all resources, all versions

#. rename releases to versions?

#. accept ``version_list: [version1, version2, …]`` as an alternative to the list of structures

#. on a similar note, accept lists of items and of components (excluding lists of structures)

#. for the components (?) of an archive file, accept a list or a single name; if the latter,
   it can contain a format item ``id`` which will be taken (as a list) from extras in pyproject.toml

#. add a ``--prune`` option to the install subcommand which removes all files that wouldn't have been
   installed into a fresh directory tree

#. clarify which attribute is used on which structural level and where it can be set


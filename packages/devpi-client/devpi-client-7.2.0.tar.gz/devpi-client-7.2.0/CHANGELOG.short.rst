

=========
Changelog
=========




.. towncrier release notes start

7.1.0 (2024-10-16)
==================

No significant changes.


7.2.0 (2024-10-16)
==================

Features
--------

- Support ``--no-docs`` and ``--only-docs`` for ``push`` command with devpi-server >= 6.14.0.

- Support ``--register-project`` for ``push`` command to external index with devpi-server >= 6.14.0.

- Add support for ``uv.conf`` to ``devpi use --set-cfg``.



Bug Fixes
---------

- fix #682: fixed encoding issues when decoding output of subprocesses.

- Fix #1052: require pkginfo >= 1.10.0 which supports newer metadata versions.

- Fix #1057: PermissionError during upload due to trying to copy a folder like a file.



7.1.0 (2024-07-17)
==================

Features
--------

- Support upload command configuration from ``pyproject.toml`` in ``[tool.devpi.upload]`` section.

- The ``--fallback-ini`` option of ``devpi test`` can now be relative to the package root. This allows using ``pyproject.toml`` or similar instead of ``tox.ini``.

- Add ``sdist`` and ``wheel`` options for ``setup.cfg``.

- Add detection of tox configs in pyproject.toml and setup.cfg for ``devpi test``.



Bug Fixes
---------

- In ``setup.cfg`` any value for upload settings was interpreted as True, now a warning is printed if it looks like False was meant and how to fix that. For backward compatibility the behavior wasn't changed.



7.0.3 (2024-04-20)
==================

Bug Fixes
---------

- Require ``build>=0.7.0`` to prevent import error with older versions.

- Fix check for extracted path when testing packages related to PEP 625 changes in setuptools.

- If the server returns a message on toxresult upload, then print it as a warning.

- Provide proper error message if the API request for ``devpi use`` fails.

- Fix #1011: change HTTP status codes >=400 to use self.fatal instead of raw SystemExit, protect 403 and 404 errors from SystemExit



7.0.2 (2023-10-19)
==================

Bug Fixes
---------

- Fix #992: Fix error added in 6.0.4 when old authentication data from before 6.x exists.


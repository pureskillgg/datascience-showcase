PureSkill.gg Data Science Showcase
==================================

|PyPI| |GitHub Actions|

.. |PyPI| image:: https://img.shields.io/pypi/v/pureskillgg-datascience-showcase.svg
   :target: https://pypi.python.org/pypi/pureskillgg-datascience-showcase
   :alt: PyPI
.. |GitHub Actions| image:: https://github.com/pureskillgg/datascience-showcase/workflows/main/badge.svg
   :target: https://github.com/pureskillgg/datascience-showcase/actions
   :alt: GitHub Actions

A small published Python package plus example Jupyter notebooks that demonstrate
analyzing PureSkill.gg's public CS:GO/CS2 data set, read from a local "tome"
collection via ``pureskillgg-dsdk``.

What it does
------------

This repo is a public, analyst-facing **showcase**, not a production service. It
has two halves:

- A thin published package, ``pureskillgg_datascience_showcase``, whose real job
  is to bootstrap a Jupyter notebook so it can find and read a local tome data
  set. The rest of the package is template skeleton (a no-op ``todo`` placeholder).
- A ``notebooks/`` directory containing the actual worked analyses against the
  public data set.

The bootstrap path works like this: a notebook calls
``setup_notebook()``, which loads a ``../.env`` file via python-dotenv_ and echoes
the ``PURESKILLGG_TOME_*`` environment variables that tell the dsdk tome curator
where the local CSDS tome collection lives. The notebook then instantiates
``pureskillgg_dsdk.tome.TomeCuratorFs`` (the **local-filesystem** tome reader,
not an S3 reader) and loads named tome dataframes for analysis with pandas,
numpy, matplotlib, and seaborn.

The example notebooks under ``notebooks/`` are the showcase content:

- **Disconnect reason analysis** (``notebooks/player_disconnect_analysis/``)
  loads the ``channel_player_disconnect`` tome, normalizes and buckets disconnect
  reasons (e.g. ``Kicked by Console``, ``VAC authentication error``,
  ``VAC banned from secure server``, timeouts) across tens of thousands of
  matches, then tabulates and plots the counts as charts branded
  "Data provided by PureSkill.gg".
- **M4 usage analysis June 2022** (``notebooks/M4 shift june 2022/``) loads the
  ``channel_player_death`` tome (millions of kill rows), derives a match date from
  each ``match_key``, and measures how the June 2022 CS:GO patch shifted the kill
  share between the M4A4 and the M4A1-S around the patch date. Note: in this data
  set the raw ``weapon_name`` value ``m4a1`` denotes the **M4A4** (renamed to
  ``m4a4_kills`` in the notebook), while ``m4a1_silencer`` / ``m4a1_silencer_off``
  denote the **M4A1-S** (renamed to ``m4a1_kills``).
- A starter **template** (``notebooks/template/template.ipynb``) plus
  ``notebooks/usual_suspects.py``, a shared import/boilerplate snippet
  (pandas / numpy / matplotlib + ``TomeCuratorFs``) that notebooks ``%load``. The
  template demonstrates ``curator.make_tome(...)`` with ``ds_reading_instructions``
  to select specific channels and columns.

For a walkthrough of the tome-curator setup and the ``.env`` variables, see
`docs/notebook-setup.md <docs/notebook-setup.md>`_.

Pipeline role
-------------

This sits at the very downstream / consumer end of the PureSkill.gg pipeline and
is **not** part of the production match-processing flow. The production pipeline
parses demos into CSDS channel data, which is rolled up into "tome" data sets and
published (including via AWS Data Exchange). This repo's notebooks load those
tomes from a **local filesystem** collection (for example ``H:\CSDS_tomes\`` for
the disconnect notebook and ``H:\CSDS_tomes_ADX\`` for the M4 notebook) using
``TomeCuratorFs``.

It consumes tome data; nothing downstream consumes this repo. It is a public PyPI
package and a demonstration, not a service.

Major modules and notebooks
---------------------------

Confirmed components, by their real names:

- ``setup_notebook`` (``pureskillgg_datascience_showcase/notebook/setup_notebook.py``)
  — notebook bootstrap; loads ``../.env`` and echoes the tome paths. Imported by
  all three example notebooks.
- ``setup_env_from_dotenv`` / ``echo_paths`` / ``echo`` / ``get_env_var``
  (``pureskillgg_datascience_showcase/env_functions/env_setup.py``) — load
  ``../.env`` via python-dotenv and read/print the ``PURESKILLGG_TOME_*`` env vars.
  The ``ENV_PREFIX`` is ``pureskillgg_tome``; the echoed names are
  ``PURESKILLGG_TOME_DEFAULT_HEADER_NAME``, ``PURESKILLGG_TOME_DS_TYPE``,
  ``PURESKILLGG_TOME_COLLECTION_PATH``, and ``PURESKILLGG_TOME_DS_COLLECTION_PATH``.
- ``todo`` (``pureskillgg_datascience_showcase/todo.py``) — placeholder skeleton
  function that returns its argument; the package is otherwise a template.
- ``notebooks/player_disconnect_analysis/Disconnect reason analysis.ipynb`` — the
  disconnect-reason notebook.
- ``notebooks/M4 shift june 2022/M4 usage analysis June 2022.ipynb`` — the
  M4 kill-share notebook.
- ``notebooks/usual_suspects.py`` and ``notebooks/template/template.ipynb`` —
  shared boilerplate and a ``make_tome`` starter template.

Dependencies of note: ``pureskillgg-dsdk`` (the tome curator), plus
``pureskillgg-csgo-dsdk``, with ``numpy<2`` and ``pandas<2`` pins. These are the
pre-Python-migration 1.x betas, consistent with a not-yet-fully-modernized
showcase. This was also the **first uv-migrated** PureSkill.gg repo, so its
tooling is uv-based (see the ``Makefile``).

Logs and observability
----------------------

This repo owns **no cloud resources**: no DynamoDB, SQS/DLQ, SNS, S3, Lambda,
Step Functions, EventBridge, AppSync, CloudFront, or API Gateway, and no IaC of
any kind (no ``serverless*.yml``, ``*.tf``, ``cdk.json``, or SAM template). It
reads only a local ``../.env`` and local tome files through ``TomeCuratorFs``.
``boto3`` appears only as a transitive lock-file dependency (via
``pureskillgg-dsdk``) and is not used by any source file. There are therefore no
CloudWatch log groups, DLQs, Sentry, or runtime ``LOG_LEVEL`` handling.

Failures surface only in development and CI:

- **Locally**, via the Makefile: ``make test`` (pytest + coverage), ``make lint``
  (pylint + ``black --check``), and ``make watch`` (pytest-watch). Notebook
  problems surface as cell output / tracebacks when running ``make notebook``.
- **In CI**, as red checks in the GitHub Actions UI. Workflows: ``main.yml``
  (build/test), ``publish.yml`` (publishes to PyPI; triggers **only on tag push**,
  ``tags: v*``, and needs the ``PYPI_API_TOKEN`` secret as ``TWINE_PASSWORD``),
  plus ``format.yml`` and ``version.yml``.

Documentation
-------------

- `docs/notebook-setup.md <docs/notebook-setup.md>`_ — how the notebook bootstrap,
  the ``.env`` / ``PURESKILLGG_TOME_*`` variables, and ``TomeCuratorFs`` fit
  together to load a local tome collection.

Installation
------------

This package is registered on the `Python Package Index (PyPI)`_
as pureskillgg-datascience-showcase_.

Install it with

::

    $ uv add pureskillgg-datascience-showcase

.. _pureskillgg-datascience-showcase: https://pypi.python.org/pypi/pureskillgg-datascience-showcase
.. _Python Package Index (PyPI): https://pypi.python.org/
.. _python-dotenv: https://pypi.python.org/pypi/python-dotenv

Development and Testing
-----------------------

Quickstart
~~~~~~~~~~

::

    $ git clone https://github.com/pureskillgg/datascience-showcase.git
    $ cd pyskill
    $ uv sync

Run each command below in a separate terminal window:

::

    $ make watch

Primary development tasks are defined in the `Makefile`.

Source Code
~~~~~~~~~~~

The `source code`_ is hosted on GitHub.
Clone the project with

::

    $ git clone https://github.com/pureskillgg/datascience-showcase.git

.. _source code: https://github.com/pureskillgg/datascience-showcase

Requirements
~~~~~~~~~~~~

You will need `Python 3`_ and uv_.

Install the development dependencies with

::

    $ uv sync

.. _uv: https://docs.astral.sh/uv/
.. _Python 3: https://www.python.org/

Tests
~~~~~

Lint code with

::

    $ make lint


Run tests with

::

    $ make test

Run tests on changes with

::

    $ make watch

Publishing
~~~~~~~~~~

Use the bump2version_ command to release a new version.
Push the created git tag which will trigger a GitHub action.

.. _bump2version: https://github.com/c4urself/bump2version

Publishing may be triggered using on the web
using a `workflow_dispatch on GitHub Actions`_.

.. _workflow_dispatch on GitHub Actions: https://github.com/pureskillgg/datascience-showcase/actions?query=workflow%3Aversion

GitHub Actions
--------------

*GitHub Actions should already be configured: this section is for reference only.*

The following repository secrets must be set on GitHub Actions.

- ``PYPI_API_TOKEN``: API token for publishing on PyPI.

These must be set manually.

Secrets for Optional GitHub Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The version and format GitHub actions
require a user with write access to the repository
including access to read and write packages.
Set these additional secrets to enable the action:

- ``GH_USER``: The GitHub user's username.
- ``GH_TOKEN``: A personal access token for the user.
- ``GIT_USER_NAME``: The name to set for Git commits.
- ``GIT_USER_EMAIL``: The email to set for Git commits.
- ``GPG_PRIVATE_KEY``: The `GPG private key`_.
- ``GPG_PASSPHRASE``: The GPG key passphrase.

.. _GPG private key: https://github.com/marketplace/actions/import-gpg#prerequisites

Contributing
------------

Please submit and comment on bug reports and feature requests.

To submit a patch:

1. Fork it (https://github.com/pureskillgg/datascience-showcase/fork).
2. Create your feature branch (`git checkout -b my-new-feature`).
3. Make changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin my-new-feature`).
6. Create a new Pull Request.

License
-------

This Python package is licensed under the MIT license.

Warranty
--------

This software is provided by the copyright holders and contributors "as is" and
any express or implied warranties, including, but not limited to, the implied
warranties of merchantability and fitness for a particular purpose are
disclaimed. In no event shall the copyright holder or contributors be liable for
any direct, indirect, incidental, special, exemplary, or consequential damages
(including, but not limited to, procurement of substitute goods or services;
loss of use, data, or profits; or business interruption) however caused and on
any theory of liability, whether in contract, strict liability, or tort
(including negligence or otherwise) arising in any way out of the use of this
software, even if advised of the possibility of such damage.

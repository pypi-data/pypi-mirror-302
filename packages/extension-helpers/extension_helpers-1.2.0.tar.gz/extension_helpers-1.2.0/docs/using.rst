Using extension-helpers
=======================

To use extension-helpers in your package, you will need to make sure your
package uses a ``pyproject.toml`` file as described in `PEP 518
<https://www.python.org/dev/peps/pep-0518/>`_.

You can then add extension-helpers to the build-time dependencies in your
``pyproject.toml`` file::

    [build-system]
    requires = ["setuptools",
                "wheel",
                "extension-helpers==1.*"]

If you have Cython extensions, you will need to make sure ``cython`` is included
in the above list too.

.. note:: It is highly recommended to pin the version of extension-helpers
          to a major version, such as ``1.*``, since extension-helpers uses
          `semantic versioning <https://semver.org>`_
          and there will therefore likely be breaking changes when the major version is bumped.
          If you do not specify any pinning, then old versions of your package that are already
          on PyPI may no longer be installable on source without disabling the build isolation
          and installing build dependencies manually.

The main functionality in extension-helpers is the
:func:`~extension_helpers.get_extensions` function which can be
used to collect package extensions. Defining functions is then done in two ways:

* For simple Cython extensions, :func:`~extension_helpers.get_extensions`
  will automatically generate extension modules with no further work.

* For other extensions, you can create ``setup_package.py`` files anywhere
  in your package, and these files can then include a ``get_extensions``
  function that returns a list of :class:`setuptools.Extension` objects.

In the second case, the idea is that for large packages, extensions can be defined
in the relevant sub-packages rather than having to all be listed in the main
``setup.py`` file.

To use this, you should modify your ``setup.py`` file to use
:func:`~extension_helpers.get_extensions`  as follows::

    from extension_helpers import get_extensions
    ...
    setup(..., ext_modules=get_extensions())

Note that if you use this, extension-helpers will also we create a
``packagename.compiler_version`` submodule that contain information about the
compilers used.

It is also possible to enable extension-helpers in ``setup.cfg`` instead of
``setup.py`` by adding the following configuration to the ``setup.cfg`` file::

    [extension-helpers]
    use_extension_helpers = true

Moreover, one can also enable extension-helpers in ``pyproject.toml`` by adding
the following configuration to the ``pyproject.toml`` file::

    [tool.extension-helpers]
    use_extension_helpers = true

.. note::
  For backwards compatibility, the setting of ``use_extension_helpers`` in
  ``setup.cfg`` will override any setting of it in ``pyproject.toml``.

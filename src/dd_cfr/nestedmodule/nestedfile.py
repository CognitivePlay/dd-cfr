"""
Documentation of nestedfile.py.
"""


def nestedfunc() -> None:
    """
    No-op function.
    """


class NestedClass:
    """
    Class nested in :obj:`nestedmodule`, and in particular in
    :obj:`nestedmodule.nestedfile``, or :obj:`nestedfile` for short.

    See the `Sphinx Documentation \
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html\
#cross-referencing-python-objects>`_
    for info how to cross-reference in general using Sphinx for
    Python.
    """

    def __init__(self, x: int) -> None:
        """
        Construct a new instance.

        :param x: Some integer that will be saved.
        """

        self._x = x

    def get_x(self) -> int:
        """
        Return the saved integer.

        :return: Returns the saved integer.
        """
        return self._x


class NestedChild(NestedClass):
    """Class deriving from :obj:`NestedClass`."""

    def __init__(self) -> None:
        """
        Construct stuff.
        """

        super().__init__(123)

    @staticmethod
    def derived_static() -> None:
        """No-op defined in derived class, as a static method."""

    def derived(self) -> None:
        """No-op defined in derived class, as a non-static method."""

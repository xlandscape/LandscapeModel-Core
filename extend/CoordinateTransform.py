"""
Class definition of the Landscape Model CoordinateTransform class.
"""
import datetime
import base


class CoordinateTransform:
    """
    Extends values by the possibility to transform them.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`extend.CoordinateTransform` ")
    base.VERSION.changed("1.3.33", "`extend.CoordinateTransform` refactored")
    base.VERSION.added("1.4.1", "Changelog in `extend.CoordinateTransform`")
    base.VERSION.changed("1.5.3", "`extend.CoordinateTransform` changelog uses markdown for code elements")

    def __init__(self, transformation_type, offset):
        if transformation_type == "date":
            self._offset = (datetime.datetime.strptime(offset, "%Y-%m-%d").date() -
                            datetime.datetime.utcfromtimestamp(0).date()).days
        else:
            raise ValueError("Unsupported offset type")
        return

    def register(self, values):
        """
        Registers the extension.
        :param values: The values to register the extension for.
        :return: Nothing.
        """
        values.extension["t"] = self.t
        return

    def t(self, value):
        """
        The custom transform function.
        :param value: Te value to transform.
        :return: The transformed value.
        """
        if isinstance(value, datetime.date):
            return (value - datetime.datetime.utcfromtimestamp(0).date()).days - self._offset
        else:
            raise TypeError("Unsupported value type")

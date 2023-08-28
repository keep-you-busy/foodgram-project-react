class ObjectExistsError(Exception):
    """Исключение из-за наличия объектов при методе DELETE."""

    pass


class ObjectNotFoundError(Exception):
    """Исключение из-за отсутствия объектов при методе POST."""

    pass

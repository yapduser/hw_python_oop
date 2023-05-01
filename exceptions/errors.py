from dataclasses import dataclass
from typing import Any


class ExceptionWorkoutError(Exception):
    """Исключения при обработке данных от датчиков."""
    pass


@dataclass
class ExceptionWorkoutTypeError(ExceptionWorkoutError):
    """Исключение при обработке вида тренировки."""
    data: Any

    def __str__(self):
        err_msg = (
            f'Пакет данных содержит неизвестный вид тренировки: '
            f'"{self.data}". \n'
            f'Доступные виды тренировок "RUN", "WLK", "SWM".'
        )

        return err_msg


@dataclass
class ExceptionWorkoutDataError(ExceptionWorkoutError):
    """Исключение при обработке пакета данных."""
    data: Any

    def __str__(self):
        err_msg = (
            f'Передан пакет данных {self.data} типа {type(self.data)}. \n'
            f'Допустимый тип пакета данных list[Union[int, float]] содержащий '
            f'не менее трех элементов.'
        )

        return err_msg

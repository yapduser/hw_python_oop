from typing import Type, Union, ClassVar
from dataclasses import dataclass
import exceptions.errors as err


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вернуть сообщение с результатами."""
        info_msg: str = (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )

        return info_msg


@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_H: ClassVar[int] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f'В дочернем классе {self.__class__.__name__}, метод не определен.'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""
    SPEED_MULT: ClassVar[int] = 18
    SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        """Рассчитать количество затраченных калорий."""
        speed_transform: float = (
            self.SPEED_MULT * self.get_mean_speed() + self.SPEED_SHIFT
        )

        return (
            speed_transform * self.weight / self.M_IN_KM * self.duration
            * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_MULT_1: ClassVar[float] = 0.035
    WEIGHT_MULT_2: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[int] = 100

    height: float

    def get_spent_calories(self) -> float:
        """Рассчитать количество затраченных калорий."""
        speed_height_ratio: float = (
            (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
            / (self.height / self.CM_IN_M)
        )

        speed_weight_mult: float = (
            self.WEIGHT_MULT_1 * self.weight + speed_height_ratio
            * self.WEIGHT_MULT_2 * self.weight
        )

        return speed_weight_mult * self.duration * self.MIN_IN_H


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    SPEED_SHIFT: ClassVar[float] = 1.1
    SPEED_MULT: ClassVar[int] = 2

    length_pool: int
    count_pool: int

    def get_mean_speed(self) -> float:
        """Рассчитать среднюю скорость при плаванье."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Рассчитать количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SPEED_SHIFT) * self.SPEED_MULT
            * self.weight * self.duration
        )


def read_package(workout_type: str, data: list[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_data: dict[str, Type[Training]] = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }

    if workout_type not in workout_data:
        raise err.ExceptionWorkoutTypeError(workout_type)

    check_data = all(map(lambda x: isinstance(x, (int, float)), data))
    if not isinstance(data, list) or len(data) < 3 or not check_data:
        raise err.ExceptionWorkoutDataError(data)

    return workout_data[workout_type](*data)


def main(training: Training) -> None:
    info_msg: InfoMessage = training.show_training_info()
    print(info_msg.get_message())


if __name__ == '__main__':
    # Тестовые пакеты данных
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)

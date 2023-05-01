from typing import Type, Union

import exceptions.errors as err


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Вернуть сообщение с результатами."""
        info_msg: str = (
            f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}."
        )

        return info_msg


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f"В дочернем классе {self.__class__.__name__}, метод не определен."
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


class Running(Training):
    """Тренировка: бег."""

    SPEED_MULT: float = 18
    SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed_transform: float = (
            self.SPEED_MULT * self.get_mean_speed() + self.SPEED_SHIFT
        )

        return (
            speed_transform
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGHT_MULT_1: float = 0.035
    WEIGHT_MULT_2: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        speed_height_ratio: float = (
            self.get_mean_speed() * self.KMH_IN_MSEC
        ) ** 2 / (self.height / self.CM_IN_M)

        speed_weight_mult: float = (
            self.WEIGHT_MULT_1 * self.weight
            + speed_height_ratio * self.WEIGHT_MULT_2 * self.weight
        )

        return speed_weight_mult * self.duration * self.MIN_IN_H


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SPEED_SHIFT: float = 1.1
    SPEED_MULT: int = 2

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: int,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость при плаванье."""
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (
            (self.get_mean_speed() + self.SPEED_SHIFT)
            * self.SPEED_MULT
            * self.weight
            * self.duration
        )


def read_package(workout_type: str, data: list[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_data: dict[str, Type[Training]] = {
        "RUN": Running,
        "WLK": SportsWalking,
        "SWM": Swimming,
    }

    if workout_type not in workout_data:
        raise err.ExceptionWorkoutTypeError(workout_type)

    check_data = all(map(lambda x: isinstance(x, (int, float)), data))
    if not isinstance(data, list) or len(data) < 3 or not check_data:
        raise err.ExceptionWorkoutDataError(data)

    return workout_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info_msg: InfoMessage = training.show_training_info()
    print(info_msg.get_message())


if __name__ == "__main__":
    # Тестовые пакеты данных.
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)

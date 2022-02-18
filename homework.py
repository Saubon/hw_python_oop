class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(
        self,
        training_type: str,
        duration: float,
        distance: float,
        speed: float,
        calories: float
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.calories = calories
        self.speed = speed

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; ',
                f'Длительность: {self.duration:.3f} ч; ',
                f'Дистанция: {self.distance:.3f} км; ',
                f'Ср. скорость: {self.speed:.3f} км/ч; ',
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        coef_callorie1: float = 18.0
        coef_callorie2: float = 20.0
        duration_min: float = self.duration * 60
        spent_calories: float = ((coef_callorie1 * super().get_mean_speed()
                                 - coef_callorie2) * self.weight
                                 / super().M_IN_KM * duration_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        coef_c1: float = 0.035
        coef_c2: float = 0.029
        duration_min: float = self.duration * 60
        spent_c: float = ((coef_c1 * self.weight
                          + (super().get_mean_speed() ** 2 // self.height)
                          * coef_c2 * self.weight) * duration_min)
        return spent_c


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость плавания."""
        mean_speed = (self.lenght_pool * self.count_pool
                      / super().M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        spent_calories = (self.get_mean_speed() + 1.1) * 2 * self.weight
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming
    }
    workout = workout_types[workout_type](*data)
    return workout


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

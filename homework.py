class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:

        self.training_type = training_type
        self.duration = round(duration, 3)
        self.distance = round(distance, 3)
        self.speed = round(speed, 3)
        self.calories = round(calories, 3)

    def get_message(self) -> str:
        return (f'''Тип тренировки: {self.training_type};
Длительность: {self.duration} ч.;
Дистанция: {self.distance} км;
Ср. скорость: {self.speed} км/ч;
Потрачено ккал: {self.calories}.
''')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 len_step=0.65
                 ) -> None:

        self.M_IN_KM = 1000
        self.IN_MINUTE = 60
        self.LEN_STEP = len_step

        self.action = action
        self.duration = duration
        self.weight = weight

        self.training_type = self.__class__.__name__

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:

        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 18
        coeff_calorie_2 = 20

        return ((coeff_calorie_1 * self.get_mean_speed()
                 - coeff_calorie_2)
                * self.weight
                / self.M_IN_KM * (self.duration * self.IN_MINUTE))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:

        super().__init__(action, duration, weight)

        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 0.035
        coeff_calorie_2 = 0.029

        return ((coeff_calorie_1 * self.weight
                 + (self.get_mean_speed()**2 // self.height)
                 * coeff_calorie_2 * self.weight)
                * self.duration * self.IN_MINUTE)


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float,
                 len_step=1.38
                 ) -> None:

        super().__init__(action, duration, weight)

        self.LEN_STEP = len_step

        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2

        return ((self.get_mean_speed() + coeff_calorie_1)
                * coeff_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    training_dict = {'RUN': Running,
                     'WLK': SportsWalking,
                     'SWM': Swimming}

    return training_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info().get_message()

    print(info)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

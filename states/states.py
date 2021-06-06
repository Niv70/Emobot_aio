from aiogram.dispatcher.filters.state import StatesGroup, State


# Создаем класс состояний обработки сообщений при начале работы бота
class Start(StatesGroup):
    Name = State()  # Пользователь ввел свое имя и должен прочитать Инфо
    Q1 = State()  # Пользователь ввел Начнем или Зачем? и должен прочитать Инфо
    Q2 = State()  # Пользователь ввел Дальше и должен почитать Инфо
    Q3 = State()  # Пользователь ввел Я чувствую интерес и должен ввести время начала опроса
    Q4 = State()  # Пользователь ввел цифру и должен ввести время завершения опроса
    Q5 = State()  # Пользователь ввел цифру и должен ввести период опроса
    Q6 = State()  # Пользователь ввел цифру и должен ввести время задачки "на прокачку"
    Q7 = State()  # Пользователь ввел цифру и переходит к ожиданию опроса на следующий день

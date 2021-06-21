from aiogram.dispatcher.filters.state import StatesGroup, State


# Класс состояний обработки сообщений при начале работы бота
class Start(StatesGroup):
    set_user_name = State()  # Пользователь должен ввести свое имя, бот выдает Инфо с кнопками
    Call_01 = State()  # Пользователь должен нажать кнопки Начнем или Зачем?, бот выдает Инфо с кнопками
    Call_02 = State()  # Пользователь должен нажать кнопки Уже_знаком или Интересно, бот выдает Инфо с кнопкой
    Call_03 = State()  # Пользователь должен нажать кнопку Дальше, бот Инфо о термометре с кнопкой
    Call_04 = State()  # Пользователь должен нажать кнопку Дальше, бот Инфо о списке чувств с кнопкой
    Call_05 = State()  # Пользователь должен нажать кнопку Договорились, бот выдает запрос на ввод Я чувствую интерес
    Tst = State()  # Пользователь должен ввести Я чувствую интерес, бот Инфо о задаче с кнопкой
    Call_05_1 = State()  # Пользователь должен нажать кнопку Дальше, бот выдает запрос на ввод Часовой пояс
    set_tmz = State()  # Пользователь ввести цифру Часовой пояс, бот выдает запрос на подтверждение с кнопками
    Call_06 = State()  # Пользователь должен нажать кнопки Да или Нет, если (Да) бот выдает запрос на ввод Время начала
    set_start_t = State()  # Пользователь ввел цифру Время начала опроса, бот выдает запрос на ввод Время завершения
    set_end_t = State()  # Пользователь ввел цифру Время завершения опроса, бот выдает запрос на ввод Период опроса
    set_period = State()  # Пользователь ввел цифру Период опроса и должен ввести Время задачки "на прокачку"
    set_tsk_t = State()  # Пользователь ввел цифру Время задачки, бот переходит к ожиданию опроса на следующий день
    Wait = State()  # Бот ждет очередного действия. Для этого сотояния нет обработчика. Все сообщения "не команды"
    #                 попадают в Эхо.


# Класс состояний обработки сообщений при опросе эмоций
class Pool(StatesGroup):
    Emo = State()  # Пользователь должен ввести эмоцию, бот сообщает о необходимости ввода причины этой эмоции (ветка 1)
    Reason = State()  # Пользователь должен ввести причину, бот переходит к ожиданию очередного опроса (ветка 1)
    EmoTask = State()  # Пользователь должен ввести эмоцию, бот сообщает о необходимости ввода причины этой эмоции
    ReasonTask = State()  # Пользователь должен ввести причину, бот запускает задачу


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 2-го дня
class Task02(StatesGroup):
    Answer_02_01 = State()  # Пользователь должен вв 1й ответ к задаче 2го дня, бот сообщает о необходимости вв 2го
    Answer_02_02 = State()
    Answer_02_03 = State()
    Answer_02_04 = State()  # 1я картина
    Answer_02_05 = State()
    Answer_02_06 = State()
    Answer_02_07 = State()  # 2я картина
    Answer_02_08 = State()
    Answer_02_09 = State()
    Answer_02_10 = State()  # 3я картина
    Answer_02_11 = State()
    Answer_02_12 = State()
    Answer_02_13 = State()  # 4я картина
    Answer_02_14 = State()
    Answer_02_15 = State()
    Answer_02_16 = State()  # 5я картина
    Answer_02_17 = State()
    Answer_02_18 = State()
    Answer_02_19 = State()  # бот переходит к ожиданию след.опроса


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 3-го дня
class Task03(StatesGroup):
    Answer_03_01 = State()  # 1й музыкальный фрагмент
    Answer_03_02 = State()
    Answer_03_03 = State()  # 2й музыкальный фрагмент
    Answer_03_04 = State()
    Answer_03_05 = State()  # 3й музыкальный фрагмент
    Answer_03_06 = State()
    Answer_03_07 = State()  # бот переходит к ожиданию след.опроса


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 4-го дня
class Task04(StatesGroup):
    Answer_04_01 = State()  # Пользователь должен ввести ответ о начале задачки, бот выводит 1ю картину и вопрос
    Answer_04_02 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 1я картина, бот выводит коммент
    Answer_04_03 = State()  # Пользователь должен ввести ответ (СЛЕДУЮЩАЯ), бот выводит 2ю картину и вопрос
    Answer_04_04 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 2й картине, бот выводит коммент
    Answer_04_05 = State()  # Пользователь должен ввести ответ (СЛЕДУЮЩАЯ), бот выводит 3ю картину и вопрос
    Answer_04_06 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 3й картине, бот выводит коммент
    Answer_04_07 = State()  # Пользователь должен ввести ответ (СЛЕДУЮЩАЯ), бот выводит 4ю картину и вопрос
    Answer_04_08 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 4й картине, бот выводит коммент
    Answer_04_09 = State()  # Пользователь должен ввести ответ (СЛЕДУЮЩАЯ), бот выводит 5ю картину и вопрос
    Answer_04_10 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 5й картине, бот выводит коммент
    Answer_04_11 = State()  # Пользователь должен ввести ответ (СЛЕДУЮЩАЯ), бот выводит 6ю картину и вопрос
    Answer_04_12 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 6й картине, бот выводит коммент
    Answer_04_13 = State()  # Пользователь должен ввести ответ (СЛЕДУЮЩАЯ), бот выводит 7ю картину и вопрос
    Answer_04_14 = State()  # Пользователь должен ввести ответ (ЗАВЕРШИТЬ), бот выводит 7ю картину и коммент
    #                         и переходит к ожиданию след.опроса


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 5-го дня
class Task05(StatesGroup):
    Answer_05_01 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 1я картина, бот выводит коммент и 2ю картину
    Answer_05_02 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 2й картине, бот выводит коммент и 3ю картину
    Answer_05_03 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 3й картине, бот выводит коммент и 4ю картину
    Answer_05_04 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 4й картине, бот выводит коммент и 5ю картину
    Answer_05_05 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 5й картине, бот выводит коммент и 6ю картину
    Answer_05_06 = State()  # Пользователь должен ввести ответ (ЭМОЦИЯ) к 6й картине, бот выводит коммент 7ю картину
    #                         и переходит к ожиданию след.опроса


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 6-го дня
class Task06(StatesGroup):
    Answer_06_01 = State()
    Answer_06_02 = State()
    Answer_06_03 = State()
    Answer_06_04 = State()
    Answer_06_05 = State()


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 7-го дня
class Task07(StatesGroup):
    Answer_07_01 = State()
    Answer_07_02 = State()
    Answer_07_03 = State()
    Answer_07_04 = State()
    Answer_07_05 = State()
    Answer_07_06 = State()
    Answer_07_07 = State()
    Answer_07_08 = State()
    Answer_07_09 = State()
    Answer_07_10 = State()
    Answer_07_11 = State()
    Answer_07_12 = State()
    Answer_07_13 = State()

# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 8-го дня
class Task08(StatesGroup):
    Answer_08_01 = State()
    Answer_08_02 = State()
    Answer_08_03 = State()
    Answer_08_04 = State()
    Answer_08_05 = State()
    Answer_08_06 = State()
    Answer_08_07 = State()
    Answer_08_08 = State()
    Answer_08_09 = State()
    Answer_08_10 = State()
    Answer_08_11 = State()
    Answer_08_12 = State()
    Answer_08_13 = State()


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 9-го дня
class Task09(StatesGroup):
    Answer_09_01 = State()
    Answer_09_02 = State()
    Answer_09_03 = State()
    Answer_09_04 = State()
    Answer_09_05 = State()
    Answer_09_06 = State()



# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 10-го дня
class Task10(StatesGroup):
    Answer_10_01 = State()
    Answer_10_02 = State()
    Answer_10_03 = State()


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 11-го дня
class Task11(StatesGroup):
    Answer_11_01 = State()
    Answer_11_02 = State()
    Answer_11_03 = State()
    Answer_11_04 = State()


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 12-го дня
class Task12(StatesGroup):
    Answer_12_01 = State()
    Answer_12_02 = State()
    Answer_12_03 = State()
    Answer_12_04 = State()



# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 13-го дня
class Task13(StatesGroup):
    Answer_13_01 = State()
    Answer_13_02 = State()
    Answer_13_03 = State()
    Answer_13_04 = State()


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 14-го дня
class Task14(StatesGroup):
    Answer_14_01 = State()
    Answer_14_02 = State()
    Answer_14_03 = State()
    Answer_14_04 = State()


# Класс состояний обработки сообщений при нажатии текстовой кнопки Настройки. Сделал отдельным классом, чтобы при
# очередном запуске действия по расписанию не оказаться с непонятными настройками и чтобы думать как не запускать цикл)
class Sett(StatesGroup):
    Stage0 = State()  # Пользователь должен ввести номер измененяемого параметра, бот задает по нему вопрос
    Stage1 = State()  # Пользователь должен ввести имя, бот проверка+запись и в Start:Wait
    Stage2 = State()  # Пользователь должен ввести Часовой пояс, бот проверка+запись и в Start:Wait
    Stage3 = State()  # Пользователь должен ввести Время начала опроса, бот проверка+запись и в Start:Wait
    Stage4 = State()  # Пользователь должен ввести Время завершения опроса, бот проверка+запись и в Start:Wait
    Stage5 = State()  # Пользователь должен ввести Периодичность опроса, бот проверка+запись и в Start:Wait
    Stage6 = State()  # Пользователь должен ввести Время выполнения задачи, бот проверка+запись и в Start:Wait

from aiogram.dispatcher.filters.state import StatesGroup, State


# Класс состояний обработки сообщений при начале работы бота
class Start(StatesGroup):
    set_user_name = State()  # Пользователь должен ввести свое имя, бот выдает Инфо с кнопками
    Call_01 = State()  # Пользователь должен нажать кнопки Начнем или Зачем?, бот выдает Инфо с кнопками
    Call_02 = State()  # Пользователь должен нажать кнопки Уже_знаком или Интересно, бот выдает Инфо с кнопкой
    Call_03 = State()  # Пользователь должен нажать кнопку Дальше, бот Инфо о термометре с кнопкой
    Call_04 = State()  # Пользователь должен нажать кнопку Дальше, бот Инфо о списке чувств с кнопкой
    Call_05 = State()  # Пользователь должен нажать кнопку Договорились, бот выдает запрос на ввод Я чувствую интерес
    Tst = State()  # Пользователь должен ввести Я чувствую интерес, бот выдает запрос на ввод Часовой пояс
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
    Answer_02_03 = State()  # 1я картина
    Answer_02_04 = State()
    Answer_02_05 = State()
    Answer_02_06 = State()  # 2я картина
    Answer_02_07 = State()
    Answer_02_08 = State()
    Answer_02_09 = State()  # 3я картина
    Answer_02_10 = State()
    Answer_02_11 = State()
    Answer_02_12 = State()  # 4я картина
    Answer_02_13 = State()
    Answer_02_14 = State()
    Answer_02_15 = State()  # 5я картина
    Answer_02_16 = State()
    Answer_02_17 = State()
    Answer_02_18 = State()  # бот переходит к ожиданию след.опроса

# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 3-го дня
class Task03(StatesGroup):
    Answer_03_01 = State()
    Answer_03_02 = State()
    Answer_03_03 = State()


# Класс состояний обработки сообщений при выполнении задачки "на прокачку" 4-го дня
class Task04(StatesGroup):
    Answer_04_01 = State()  # Пользователь должен вв 1й ответ к задаче 4го дня, бот сообщает о необходимости вв 2го
    Answer_04_02 = State()
    Answer_04_03 = State()  # 1я картина
    Answer_04_04 = State()
    Answer_04_05 = State()
    Answer_04_06 = State()  # 2я картина
    Answer_04_07 = State()
    Answer_04_08 = State()
    Answer_04_09 = State()  # 3я картина
    Answer_04_10 = State()
    Answer_04_11 = State()
    Answer_04_12 = State()  # 4я картина
    Answer_04_13 = State()
    Answer_04_14 = State()
    Answer_04_15 = State()  # 5я картина
    Answer_04_16 = State()
    Answer_04_17 = State()
    Answer_04_18 = State()  # бот переходит к ожиданию след.опроса


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

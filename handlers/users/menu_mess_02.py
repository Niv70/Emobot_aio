# В этом модуле выполняется обработка сообщений из текстового меню
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from loader import dp


Possible_Emotions = ['злость', 'трепет', 'угрюмость', 'отчужденность',
                     'гнев', 'обеспокоенность ', 'серьезность', 'неловкость',
                     'возмущение', 'испуг', 'подавленность', 'удивление',
                     'ненависть', 'тревога', 'разочарование', 'шок',
                     'обида', 'волнение', 'боль', 'поражение',
                     'сердитость', 'боязнь', 'застенчивость', 'остолбенение',
                     'досада', 'ужас', 'покинутость', 'изумление',
                     'раздражение', 'ощущение угрозы', 'удрученность', 'потрясение',
                     'оскорбленность', 'ошеломленность', 'усталость', 'энтузиазм',
                     'воинственность', 'опасение', 'глупость', 'восторг',
                     'бунтарство', 'уныние', 'апатия', 'возбужденность',
                     'сопротивление', 'ощущение тупика', 'самодовольство', 'страсть',
                     'зависть', 'запутанность', 'скука', 'эйфория',
                     'надменность', 'потерянность', 'истощение', 'трепет',
                     'презрение', 'дезориентация', 'расстройство', 'решимость',
                     'отвращение', 'бессвязность', 'упадок сил', 'дерзость',
                     'подавленность', 'одиночество', 'нетерпеливость', 'удовлетворенность',
                     'уязвленность', 'изолированность', 'вспыльчивость', 'гордость',
                     'подозрительноость', 'грусть', 'тоска', 'сентиментальность',
                     'настороженность', 'печаль', 'стыд', 'счастье',
                     'озабоченность', 'горе', 'вина', 'радость',
                     'тревожность', 'угнетенность', 'униженность', 'блаженство',
                     'страх', 'мрачность', 'ущемленность', 'забавность',
                     'нервозность', 'отчаяние', 'смущение', 'восхищение',
                     'ожидание', 'опустошенность', 'неудобство', 'триумф',
                     'взволнованность', 'беспомощность', 'тяжесть', 'удовольствие',
                     'слабость', 'сожаление', 'мечтательность',
                     'ранимость', 'скорбь', 'очарование',
                     'неудовольствие', 'растерянность ', 'принятие']


@dp.message_handler(Text(equals="Список эмоций и чувств"), state='*')
async def get_list(message: Message):
    await message.answer("{}".format(Possible_Emotions))


@dp.message_handler(Text(equals="Термометр"), state='*')
async def get_list(message: Message):
    img = open("./IMG/Термометр.jpg", "rb")
    await message.answer_photo(img)
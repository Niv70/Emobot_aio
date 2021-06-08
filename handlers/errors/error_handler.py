import logging
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)


from loader import dp


@dp.errors_handler()
async def errors_handler(update, exception):

    #    Exceptions handler. Catches all exceptions within task factory tasks.
    #    :param dispatcher:
    #    :param update:
    #    :param exception:
    #    :return: stdout logging

    if isinstance(exception, CantDemoteChatCreator):
        logging.exception("ОшИбКа: Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception('ОшИбКа: Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.exception('ОшИбКа: Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception('ОшИбКа: Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.exception('ОшИбКа: MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.exception(f'ОшИбКа: Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'ОшИбКа: InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'ОшИбКа: TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        logging.exception(f'ОшИбКа: RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        logging.exception(f'ОшИбКа: CantParseEntities: {exception} \nUpdate: {update}')
        return True
    
    logging.exception(f'ОшИбКа: Update: {update} \n{exception}')

from aiogram import Dispatcher, types
from main import test, bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup



class QState(StatesGroup):
    Answered = State() 
    questionNumber = 0
    result = 0

async def startTest(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Let's get started! Press 'OK'.")
    await state.set_state(QState.Answered)
    # questions = test.find()
    # for el in questions:
    #     testQuestion = (
    #         el['question'] 
    #         + '\n 1) ' + el['variants'][0] 
    #         + '\n 2) ' + el['variants'][1] 
    #         + '\n 3) ' + el['variants'][2]
    #         )
    #     await bot.send_message(message.from_user.id, testQuestion)
async def Test(message: types.Message, state: FSMContext):
    questions = test.find()
    if QState.questionNumber < len(list(test.find())):
        question = questions[QState.questionNumber]
        testQuestion = (
                question['question'] 
                + '\n 1) ' + question['variants'][0] 
                + '\n 2) ' + question['variants'][1] 
                + '\n 3) ' + question['variants'][2]
                )
        QState.questionNumber += 1
        await state.set_state(QState.Answered)
        await bot.send_message(message.from_user.id, testQuestion)
    else:
        await bot.send_message(message.from_user.id, "no more questions")
        QState.questionNumber = 0
        await state.finish()
def initTest(dp: Dispatcher):
    dp.register_message_handler(startTest, content_types=['text'], state='*', commands=['testme'])
    dp.register_message_handler(Test, content_types=['text'], state = QState.Answered)
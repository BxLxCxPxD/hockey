from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

TOKEN = "6052247347:AAFxYJoiwOJhS9Kk3w_lumhKFrCxp7Cwmjc"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

products = []


class State:
    def handle(self, message):
        pass

class MainMenuState(State):
    async def handle(self, message):
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Выбрать игроков", "Выбрать событие"]
        keyboard_markup.add(*buttons)

        await message.answer("Выберите действие:", reply_markup=keyboard_markup)

class ListItemsState(State):
    async def handle(self, message):
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Нападающие", "Защитники"]
        keyboard_markup.add(*buttons)

        await message.answer("Выберите позиции игроков", reply_markup=keyboard_markup)

class AddProductState(State):
    async def handle(self, message):
        await message.answer("Введите номер игрока:")

        global current_state
        current_state = ProductEntryState()

class ProductEntryState(State):
    async def handle(self, message):
        global products
        product_name = message.text.strip()  
        words = product_name.split()

        if len(words) <= 5:
            products.append(product_name)
            await message.answer(f"Игрок '{product_name}' выбран!.")
            
            global current_state
            current_state = MainMenuState()
            await current_state.handle(message)
        else:
            await message.answer("Ошибка ввода!")

class ShowProductsState(State):
    async def handle(self, message):
        global products
        if not products:
            await message.answer("Нет таких игроков")
        else:
            products_text = "\n".join(products)
            await message.answer(f"Список игроков:\n{products_text}")

class RemoveProductsState(State):
    async def handle(self, message):
        global products
        products = []  # Очистить список продуктов
        await message.answer("Все игроки удалены.")

# Начальное состояние
current_state = MainMenuState()

# Шаблон состояния для сортировки покупок
class SortPurchaseState(State):
    async def handle(self, message):
        keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Важные", "Купленные", "Общее", "Назад", "Удалить лишние товары"]
        keyboard_markup.add(*buttons)

        await message.answer("Выберите категорию для сортировки:", reply_markup=keyboard_markup)

# Обработка команды начать сортировку покупок
@dp.message_handler(lambda message: message.text == "Отсортировать покупку")
async def process_sort_purchase(message: types.Message):
    global current_state
    current_state = SortPurchaseState()
    await current_state.handle(message)

# Обработка сортировки по категориям
@dp.message_handler(lambda message: message.text in ["Важные", "Купленные", "Общее", "Удалить лишние товары"])
async def process_sort_category(message: types.Message):
    global current_state
    await message.answer(f"Вы выбрали сортировку по категории: {message.text}")
    current_state = MainMenuState()
    await current_state.handle(message)

# Обработка команд связанных с главным меню
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    global current_state
    await current_state.handle(message)

# Обработка команды вернуться в главное меню
@dp.message_handler(lambda message: message.text == "Проконтролировать покупку")
async def process_purchase_control(message: types.Message):
    global current_state
    current_state = MainMenuState()
    await current_state.handle(message)

# Обработка команды составить список товаров
@dp.message_handler(lambda message: message.text == "Составить список товаров")
async def process_list_items(message: types.Message):
    global current_state
    current_state = ListItemsState()
    await current_state.handle(message)

# Обработка команды добавить продукт
@dp.message_handler(lambda message: message.text == "Выбрать игроков")
async def process_add_product(message: types.Message):
    global current_state
    current_state = AddProductState()
    await current_state.handle(message)

# Обработка команды показать все продукты
@dp.message_handler(lambda message: message.text == "Выбрать событие")
async def process_show_products(message: types.Message):
    global current_state
    current_state = ShowProductsState()
    await current_state.handle(message)

# Обработка команды удалить все продукты
@dp.message_handler(lambda message: message.text == "Удалить все продукты")
async def process_remove_products(message: types.Message):
    global current_state
    current_state = RemoveProductsState()
    await current_state.handle(message)

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)

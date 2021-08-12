from aiogram.dispatcher.filters.state import StatesGroup, State


class SVO(StatesGroup):
	question = State()
	again = State()
	transport = State()
	from_location = State()
	to_location = State()

from app.templates import texts, keyboards

from aiogram import Router, types
from aiogram.filters import CommandStart, Command


async def start(message: types.Message):
    
	await message.answer(
        texts.START, 
        reply_markup=keyboards.generate_hello_keyboard(),
    )

async def help_(message: types.Message):
    
	await message.answer(
        texts.HELP,
        disable_web_page_preview=True, 
        reply_markup=keyboards.generate_hello_keyboard(),
    )


async def author(message: types.Message):
	
    await message.answer(
        texts.AUTHORS, 
        reply_markup=keyboards.generate_hello_keyboard(),
    )
 
 
def register(router: Router):
    
    router.message.register(start, CommandStart())
    router.message.register(help_, Command('help'))
    router.message.register(author, Command('author'))

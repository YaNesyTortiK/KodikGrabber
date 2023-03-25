import asyncio
import logging

from app import handlers, utils

from aiogram import Bot, Dispatcher


logger = logging.getLogger(__name__)

async def main():

    config = utils.load_config('config.yaml')
    kodik = utils.KodikParser(config.kodik_token)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("Starting bot...")


    bot = Bot(
        token=config.token,
        parse_mode="HTML",
    )
    dp = Dispatcher()

    handlers.setup(dp)

    try:

        await dp.start_polling(bot, config=config, kodik=kodik)

    finally:

        await dp.fsm.storage.close()


try:

    asyncio.run(main())

except (
    KeyboardInterrupt,
    SystemExit,
):

    logger.info("Bot stopped")

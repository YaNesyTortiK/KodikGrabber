from . import (
    start,
    serie,
)

from aiogram import Router


def setup(router: Router):
    
    start.register(router)
    serie.register(router)

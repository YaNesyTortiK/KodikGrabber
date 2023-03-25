from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton, 
    ReplyKeyboardMarkup, 
    KeyboardButton,
)
    
    
def generate_quality_inline_keyboard(series_count: int, translation_id: str, serial_id: str) -> InlineKeyboardMarkup:
    """Callback: Q_720/480/360_{series_count}_{translation_id}_{serial_id}"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="720p", callback_data=f"Q_720_{series_count}_{translation_id}_{serial_id}")],
        [InlineKeyboardButton(text="480p", callback_data=f"Q_480_{series_count}_{translation_id}_{serial_id}")],
        [InlineKeyboardButton(text="360p", callback_data=f"Q_360_{series_count}_{translation_id}_{serial_id}")],
    ])
    return keyboard

def generate_quality_inline_keyboard_for_film(series_count: int, translation_id: str, serial_id: str) -> InlineKeyboardMarkup:
    """Callback: DS_{0}_{translation_id}_{serial_id}_720"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="720p", callback_data=f"DS_{0}_{translation_id}_{serial_id}_720")],
        [InlineKeyboardButton(text="480p", callback_data=f"DS_{0}_{translation_id}_{serial_id}_480")],
        [InlineKeyboardButton(text="360p", callback_data=f"DS_{0}_{translation_id}_{serial_id}_360")],
    ])
    return keyboard

def generate_hello_keyboard() -> ReplyKeyboardMarkup:
    """Callback: DS_{0}_{translation_id}_{serial_id}_720"""
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="/help")],
        [KeyboardButton(text="/author")],
    ], resize_keyboard=True)
    return keyboard

def generate_series_keyboard(series_count: int, translation_id: str, serial_id: str, quality: str):
    """callback_data: DA(S)_{series_count}/{seria_num}_{translation_id}_{serial_id}_{quality}"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            *(
                [InlineKeyboardButton(text=str(i), callback_data=f"DS_{i}_{translation_id}_{serial_id}_{quality}")]
                for i in range(1, series_count+1)
            ),
            [InlineKeyboardButton(text="Скачать все", callback_data=f"DA_{series_count}_{translation_id}_{serial_id}_{quality}")]
            if series_count <= 12 else []
        ]
    )
    return keyboard

def generate_translations_inline_keyboard(translations: list, series_count: int, serial_id: str) -> InlineKeyboardMarkup:
    """Callback: T_t['id']_t['name']_{series_count}_{serial_id}"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t['name'], callback_data=f"T_{t['id']}_{t['name'][:15]}_{series_count}_{serial_id}")]
        for t in translations
    ])

    return keyboard

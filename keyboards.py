import emoji
from telebot import types
import actions


def get_start_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            emoji.emojize(':fire: Create Post'),
            callback_data=actions.CREATE_POST
        )
    )
    return keyboard


def get_photo_option_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton(
            emoji.emojize(':check_mark_button: Yes'),
            callback_data=actions.PHOTO_OPTION_YES
        ),
        types.InlineKeyboardButton(
            emoji.emojize(':no_entry: No'),
            callback_data=actions.PHOTO_OPTION_NO
        ),
    )
    return keyboard


def get_review_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(
        types.InlineKeyboardButton(
            emoji.emojize(':sparkle: Create new button'),
            callback_data=actions.PREVIEW_ADD_BUTTON,
        ),
        types.InlineKeyboardButton(
            emoji.emojize(':rocket: Upload to Papa bet'),
            callback_data=actions.UPLOAD_TO_PAPA_BET,
        ),
    )

    keyboard.row(
        types.InlineKeyboardButton(
            emoji.emojize(':downwards_button: Switch to next line'),
            callback_data=actions.GO_TO_NEW_LINE
        )
    )

    keyboard.row(
        types.InlineKeyboardButton(
            emoji.emojize(':memo: View Post'),
            callback_data=actions.VIEW_POST
        )
    )
    return keyboard


def generate_user_buttons(buttons):
    keyboard = types.InlineKeyboardMarkup()
    rows = {}  # Dictionary to hold buttons for each row

    # Group buttons by row
    for button in buttons:
        row_number = button["row"]
        if row_number not in rows:
            rows[row_number] = []
        rows[row_number].append(button)

    # Add buttons row by row
    for row_number, buttons_in_row in rows.items():
        buttons_row = []
        for button_data in buttons_in_row:
            buttons_row.append(
                types.InlineKeyboardButton(
                    button_data["name"], url=button_data["link"])
            )
        keyboard.row(*buttons_row)

    return keyboard

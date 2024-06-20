import emoji
import telebot
import actions
import keyboards
from validators import is_valid_url

TOKEN = '6819828480:AAHWQlXw4PeNTmgN74aOg431bZ25UE6BOJU'
# DEV_TOKEN = '7077237570:AAFjgOaXSkNZWkAK4TMqovfttL-KCh7JMGs'

ADMINS = [1212190489, 6536843409, 6308823202, 1036517255]

PAPA_BET_CHANNEL_ID = '-1001962069227'

bot = telebot.TeleBot(TOKEN)


user_state = {}
user_post_content = {}
user_photo = {}
user_video = {}
user_gif = {}
user_buttons_row = {}
user_buttons = []


def clean_up(id):
    user_state.pop(id, None)
    user_post_content.pop(id, None)
    user_photo.pop(id, None)
    user_video.pop(id, None)
    user_gif.pop(id, None)
    user_buttons_row[id] = 1
    user_buttons.clear()


def show_result(call):
    if call.message.chat.id in user_photo:
        bot.send_photo(call.message.chat.id,
                       user_photo[call.message.chat.id],
                       caption=user_post_content[call.message.chat.id],
                       reply_markup=keyboards.generate_user_buttons(
                           user_buttons)
                       )
    elif call.message.chat.id in user_video:
        bot.send_video(call.message.chat.id,
                       user_video[call.message.chat.id],
                       caption=user_post_content[call.message.chat.id],
                       reply_markup=keyboards.generate_user_buttons(
                           user_buttons)
                       )
    elif call.message.chat.id in user_gif:
        bot.send_animation(call.message.chat.id,
                       user_gif[call.message.chat.id],
                       caption=user_post_content[call.message.chat.id],
                       reply_markup=keyboards.generate_user_buttons(
                           user_buttons)
                       )
    else:
        bot.send_message(
            call.message.chat.id,
            user_post_content[call.message.chat.id],
            reply_markup=keyboards.generate_user_buttons(user_buttons)
        )


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id not in ADMINS:
        return
    clean_up(message.chat.id)
    user_buttons_row[message.chat.id] = 1
    bot.send_message(
        message.chat.id,
        emoji.emojize(
            ":high_voltage: Papa bet glass button bot :high_voltage:"),
        reply_markup=keyboards.get_start_inline_keyboard()
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.from_user.id not in ADMINS:
        return
    if call.data == actions.CREATE_POST:
        user_state[call.message.chat.id] = actions.WAITING_FOR_POST_CONTENT
        bot.send_message(
            call.message.chat.id,
            emoji.emojize(":memo: Enter post content")
        )

    is_photo_upload_state = user_state.get(
        call.message.chat.id) == actions.WAITING_FOR_PHOTO_OPTION

    if is_photo_upload_state:
        if call.data == actions.PHOTO_OPTION_YES:
            bot.send_message(
                call.message.chat.id,
                emoji.emojize(
                    ":camera_with_flash: Please send the photo, video or GIF file you want to add."))
            user_state[call.message.chat.id] = actions.WAITING_FOR_PHOTO
        elif call.data == actions.PHOTO_OPTION_NO:
            user_state[call.message.chat.id] = actions.WAITING_FOR_BUTTON_NAME
            bot.send_message(
                call.message.chat.id,
                emoji.emojize(
                    ":white_large_square: Please enter the name of the button for this post.")
            )
    if call.data == actions.VIEW_POST:
        show_result(call)
    elif call.data == actions.PREVIEW_ADD_BUTTON:
        user_state[call.message.chat.id] = actions.WAITING_FOR_BUTTON_NAME
        bot.send_message(
            call.message.chat.id,
            emoji.emojize(
                ":check_mark_button:  Button name"
            ),
        )
    elif call.data == actions.UPLOAD_TO_PAPA_BET:
        if call.message.chat.id in user_photo:
            bot.send_photo(
                PAPA_BET_CHANNEL_ID,
                user_photo[call.message.chat.id],
                caption=user_post_content[call.message.chat.id],
                reply_markup=keyboards.generate_user_buttons(user_buttons)
            )
        else:
            bot.send_message(
                PAPA_BET_CHANNEL_ID,
                user_post_content[call.message.chat.id],
                reply_markup=keyboards.generate_user_buttons(user_buttons)
            )
    elif call.data == actions.GO_TO_NEW_LINE:
        user_buttons_row[call.message.chat.id] += 1
        bot.send_message(call.message.chat.id, 'going to next line')


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.chat.id not in ADMINS:
        return
    current_state = user_state.get(message.chat.id)
    if current_state == actions.WAITING_FOR_POST_CONTENT:
        # Save post content
        user_post_content[message.chat.id] = message.text
        # Set user state to 'waiting_for_photo_option'
        user_state[message.chat.id] = actions.WAITING_FOR_PHOTO_OPTION
        bot.send_message(
            message.chat.id,
            emoji.emojize(
                ":check_mark_button: Content has been received \n\n :framed_picture: Do you want to add photo, video or GIF file to your post?"
            ),
            reply_markup=keyboards.get_photo_option_inline_keyboard()
        )
    elif current_state == actions.WAITING_FOR_BUTTON_NAME:
        user_state[message.chat.id] = actions.WAITING_FOR_BUTTON_LINK
        user_buttons.append({
            "name": message.text,
            "link": "#",
            "row": user_buttons_row[message.chat.id]
        })
        bot.send_message(
            message.chat.id,
            emoji.emojize(
                ':check_mark_button: Great now send me button link (format should be http or https)')
        )
    elif current_state == actions.WAITING_FOR_BUTTON_LINK:
        if is_valid_url(message.text):
            user_state[message.chat.id] = actions.PREVIEW_OR_ADD_NEW_BUTTON
            user_buttons[-1]['link'] = message.text
            bot.send_message(
                message.chat.id,
                emoji.emojize(
                    ':check_mark: New button has been created \n\n :shuffle_tracks_button: You can finish by clicking Review or add new button'
                ),
                reply_markup=keyboards.get_review_inline_keyboard()
            )
        else:
            bot.send_message(
                message.chat.id,
                emoji.emojize(
                    ':cross_mark: Invalid url format. \n\n The URL format should start with http or with https')
            )


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if message.chat.id not in ADMINS:
        return
    if user_state.get(message.chat.id) == actions.WAITING_FOR_PHOTO:
        # Save the photo
        photo_id = message.photo[-1].file_id
        # Store photo ID
        user_photo[message.chat.id] = photo_id
        # Ask for the name of the button
        user_state[message.chat.id] = actions.WAITING_FOR_BUTTON_NAME
        bot.send_message(
            message.chat.id,
            emoji.emojize(
                ":check_mark_button: Photo received \n\n :white_large_square: Please enter the name of the button for this photo.")
        )


@bot.message_handler(content_types=['video'])
def handle_video(message):
    if message.chat.id not in ADMINS:
        return
    if user_state.get(message.chat.id) == actions.WAITING_FOR_PHOTO:
        # Save the video
        video_id = message.video.file_id
        # Store video ID
        user_video[message.chat.id] = video_id
        # Ask for the name of the button
        user_state[message.chat.id] = actions.WAITING_FOR_BUTTON_NAME
        bot.send_message(
            message.chat.id,
            emoji.emojize(
                ":check_mark_button: Video received \n\n :white_large_square: Please enter the name of the button for this video.")
        )


@bot.message_handler(content_types=['animation'])
def handle_gif(message):
    if user_state.get(message.chat.id) == actions.WAITING_FOR_PHOTO:
        if message.document.mime_type == "video/mp4":
            gif_id = message.animation.file_id
            user_gif[message.chat.id] = gif_id
            # Ask for the name of the button
            user_state[message.chat.id] = actions.WAITING_FOR_BUTTON_NAME
            bot.send_message(
                message.chat.id,
                emoji.emojize(
                    ":check_mark_button: GIF received \n\n :white_large_square: Please enter the name of the button for this GIF.")
            )


bot.infinity_polling()

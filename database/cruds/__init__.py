
from .users import (
    get_user_by_tg_id,
    update_user_by_tg_id,
    delete_user_by_tg_id,
)

from .likes import (
    add_like,
    delete_like,
)

from .dislikes import (
    add_dislike,
    delete_dislike,
)

from .photos import (
    add_photo,
    get_photos_by_tg_id,
    update_photo_by_id,
    delete_photo_by_id,
)

from .messages import (
    create_message,
    update_message_by_id,
    delete_message_by_id,
)

from .chat import (
    get_chat_by_users,
)

from .groups import (
    create_group,
    get_group_messages,
)
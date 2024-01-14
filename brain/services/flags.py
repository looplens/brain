from enum import Enum


class UserFlags(Enum):
    GLYNET_EMPLOYEE = 1
    VERIFIED_USER = 2
    ARTIST_USER = 4
    SPAMMER = 8
    SYSTEM = 16
    HAS_UNREAD_URGENT_MESSAGES = 32
    VERIFIED_MAIL = 64
    USED_WEB_CLIENT = 128
    USED_MOBILE_CLIENT = 256
    UNDERAGE_DELETED = 512
    SELF_DELETED = 1024
    DELETED = 2048
    DISABLED_SUSPICIOUS_ACTIVITY = 4096
    SELF_DISABLED = 8192
    DISABLED = 16384
    NSFW_PROFILE = 32768
    MEMORIALIZED_PROFILE = 65536


class NotificationFlags(Enum):
    LOGIN_ALERT = 1
    MENTION_ALERT = 2
    COMMENTS_MENTION_ALERT = 4
    ANNOUNCEMENTS = 8
    TIPS = 16


class CommentFlags(Enum):
    SELF_DELETED = 1
    SYSTEM_DELETED = 2
    POST_DELETED = 4
    CONTAINS_GIF = 8
    SPAM_CONTENT = 16
    POST_AUTHOR_DELETE = 32


class PostFlags(Enum):
    SELF_DELETED = 1
    SYSTEM_DELETED = 2
    SPAM_CONTENT = 4
    NSFW_CONTENT = 8
    ARCHIVED = 16
    DISABLED_COMMENTS = 32


class UserPrivacyFlags(Enum):
    HIDE_FOLLOWINGS = 1
    PRIVATE_ACCOUNT = 2
    FILTER_NSFW = 4


def calculate_flags(enum_type, flag):
    flag_num = int(flag)
    results = []

    for i in range(64):
        bitwise = 1 << i

        if flag_num & bitwise:
            flag_name = enum_type(bitwise).name
            results.append(flag_name)

    return results if results else "NONE"


def calculate_post_flags(flag):
    return calculate_flags(PostFlags, flag)


def calculate_comment_flags(flag):
    return calculate_flags(CommentFlags, flag)


def calculate_user_flags(flag):
    return calculate_flags(UserFlags, flag)


def calculate_user_privacy_flags(flag):
    return calculate_flags(UserPrivacyFlags, flag)


def calculate_notification_flags(flag):
    return calculate_flags(NotificationFlags, flag)

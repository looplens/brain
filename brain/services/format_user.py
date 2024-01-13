def format_user(data):
  return {
    "id": getattr(data, "id", None),
    "name": getattr(data, "name", None),
    "username": getattr(data, "username", None),
    "avatar": getattr(data, "avatar", None),
    "flags": getattr(data, "flags", 0),
    "accent_color": getattr(data, "accent_color", None),
    "joined_at": getattr(data, "created_at", None)
  }


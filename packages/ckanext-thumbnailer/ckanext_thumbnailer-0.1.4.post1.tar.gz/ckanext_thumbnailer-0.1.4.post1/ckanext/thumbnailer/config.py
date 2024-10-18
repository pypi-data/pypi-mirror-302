from __future__ import annotations

import ckan.plugins.toolkit as tk

WIDTH = "ckanext.thumbnailer.width"
HEIGHT = "ckanext.thumbnailer.height"
MAX_REMOTE_SIZE = "ckanext.thumbnailer.max_remote_size"


def width() -> int:
    return tk.config[WIDTH]


def height() -> int:
    return tk.config[HEIGHT]


def max_remote_size() -> int:
    return tk.config[MAX_REMOTE_SIZE]

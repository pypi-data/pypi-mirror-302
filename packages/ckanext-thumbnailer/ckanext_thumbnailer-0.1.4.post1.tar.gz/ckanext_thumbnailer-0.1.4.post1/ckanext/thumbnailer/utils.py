from __future__ import annotations
import logging

from typing import Any

import ckan.plugins.toolkit as tk

log = logging.getLogger(__name__)

CONFIG_FORMATS = "ckanext.thumbnailer.auto_formats"
DEFAULT_FORMATS = []


def create_thumbnail(context, data_dict):
    formats = tk.aslist(tk.config.get(CONFIG_FORMATS, DEFAULT_FORMATS))
    fmt = data_dict.get("format")

    if not fmt or fmt.lower() not in formats:
        return

    try:
        result = tk.get_action("thumbnailer_resource_thumbnail_create")(
            context, data_dict
        )
        log.info("Thumbnail for %s created at %s", data_dict["id"], result["thumbnail"])
    except tk.ValidationError as e:
        log.error("Cannot create thumbnail: %s", e)


def resource_file(id: str) -> dict[str, Any] | None:
    """Return information about resource's thumbnail.

    Args:
        id: ID of the resource

    Returns:
        thumbnail's file details
    """

    files = tk.get_action("files_file_search")(
        {"ignore_auth": True},
        {
            "owner_type": "resource",
            "owner_id": id,
            "storage": "thumbnail",
            "sort": "ctime",
            "reverse": True,
            "rows": 1,
        },
    )
    if files["results"]:
        return files["results"][0]

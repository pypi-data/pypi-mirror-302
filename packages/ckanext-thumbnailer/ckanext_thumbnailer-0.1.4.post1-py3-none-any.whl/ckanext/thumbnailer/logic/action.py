from __future__ import annotations

import tempfile
import os
import logging
import subprocess
import datetime
from typing import Any
from ckanext.files.utils import contextlib
from preview_generator.exception import UnsupportedMimeType
from preview_generator.manager import PreviewManager
from werkzeug.datastructures import FileStorage

import ckan.plugins.toolkit as tk
from ckanext.toolbelt.decorators import Collector
from ckanext.toolbelt.utils.fs import path_to_resource
from ckanext.files.shared import get_storage, FileData
from ckanext.thumbnailer import utils, config

log = logging.getLogger(__name__)
action, get_actions = Collector("thumbnailer").split()


@action
def resource_thumbnail_create(context, data_dict):
    tk.check_access("thumbnailer_resource_thumbnail_create", context, data_dict)

    res = tk.get_action("resource_show")(context, {"id": data_dict["id"]})

    preview = _get_preview(res)
    upload = open(preview, "rb")
    existing = utils.resource_file(res["id"])

    if existing:
        result = tk.get_action("files_file_replace")(
            {"ignore_auth": True, "user": context["user"]},
            {
                "id": existing["id"],
                "upload": upload,
            },
        )

    else:
        result = tk.get_action("files_file_create")(
            {"ignore_auth": True, "user": context["user"]},
            {
                "name": "-{}.jpeg".format(res["id"]),
                "storage": "thumbnail",
                "upload": upload,
            },
        )

        tk.get_action("files_transfer_ownership")(
            {"ignore_auth": True},
            {
                "id": result["id"],
                "owner_id": res["id"],
                "owner_type": "resource",
            },
        )

    storage = get_storage("thumbnail")

    return {"thumbnail": storage.public_link(FileData.from_dict(result))}


def _get_preview(res: dict[str, Any]):
    cache = os.path.join(
        tempfile.gettempdir(), tk.config["ckan.site_id"], "ckanext-thumbnailer"
    )
    manager = PreviewManager(cache, create_folder=True)

    max_size = config.max_remote_size()
    force = False
    with contextlib.suppress(TypeError, KeyError):
        uploaded_at = datetime.datetime.fromisoformat(res["last_modified"])
        age = datetime.datetime.now() - uploaded_at
        force = age < datetime.timedelta(minutes=10)

    with path_to_resource(res, max_size) as path:
        if not path:
            raise tk.ValidationError({"id": ["Cannot determine path to resource"]})
        try:
            return manager.get_jpeg_preview(
                path,
                width=config.width(),
                height=config.height(),
                force=force,
            )
        except (UnsupportedMimeType, subprocess.CalledProcessError) as e:
            log.error("Cannot extract thumbnail for resource %s: %s", res["id"], e)
            raise tk.ValidationError({"id": ["Unsupported media type"]})

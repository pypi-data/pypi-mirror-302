from __future__ import annotations

import ckan.model as model
import ckan.plugins.toolkit as tk

from ckanext.toolbelt.decorators import Collector
from ckanext.files.shared import get_storage, FileData
from .utils import resource_file

helper, get_helpers = Collector("thumbnailer").split()


@helper
def resource_thumbnail_url(id_: str, qualified: bool = False):
    info = resource_file(id_)
    if not info:
        return

    data = FileData.from_dict(info)
    storage = get_storage("thumbnail")
    link = storage.public_link(data)

    return tk.h.url_for_static(link, qualified=qualified)

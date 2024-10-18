from __future__ import annotations

import sqlalchemy as sa
import click
import ckan.model as model
import ckan.plugins.toolkit as tk

from . import utils

def get_commands():
    return [thumbnailer]


@click.group(short_help="ckanext-thumbnailer CLI.")
def thumbnailer():
    """ckanext-thumbnailer CLI.
    """
    pass

@thumbnailer.command()
@click.argument("ids", nargs=-1)
@click.option("-o", "--offset", type=int, default=0)
def process(ids: tuple[str], offset: int):
    """Create thumbnails for the given/all resources
    """
    user = tk.get_action("get_site_user")({"ignore_auth": True}, {})
    resources = _get_resources(ids)
    with click.progressbar(resources, length=resources.count()) as bar:
        for step, res in enumerate(bar):
            if step < offset:
                continue
            utils.create_thumbnail({"user": user["name"]}, {
                "id": res.id,
                "format": res.format,
            })

def _get_resources(ids: tuple[str]):
    q = model.Session.query(model.Resource).filter(
        model.Resource.state == "active"
    ).order_by(model.Resource.id)
    if ids:
        q = q.filter(model.Resource.id.in_(ids))

    return q



@thumbnailer.command()
def migrate():
    """Migrate thumbnails created via ckanext-files pre-v1.
    """

    from ckanext.files.shared import Multipart
    stmt = sa.select(Multipart).where(Multipart.storage == "thumbnail")

    total = model.Session.scalar(sa.select(sa.func.count()).select_from(stmt))

    with click.progressbar(model.Session.scalars(stmt), total) as bar:
        for obj in bar:
            bar.label = obj.id
            if "location" in obj.storage_data:
                obj.location = obj.storage_data["location"]
            model.Session.commit()

            tk.get_action("files_multipart_refresh")({"ignore_auth": True}, {"id": obj.id})

            model.Session.refresh(obj)
            if "uploaded" in obj.storage_data:
                obj.size = obj.storage_data["uploaded"]

            obj.content_type = "image/jpeg"
            model.Session.commit()

            try:
                file = tk.get_action("files_multipart_complete")(
                    {"ignore_auth": True}, {"id": obj.id, "keep_storage_data": True}
                )
            except tk.ValidationError as e:
                tk.error_shout(
                    f"File {obj.id} with data {obj.storage_data} is not migrated: {e.error_dict}"
                )
                continue

            tk.get_action("files_transfer_ownership")(
                {"ignore_auth": True},
                {
                    "id": file["id"],
                    "owner_id": obj.storage_data["thumbnailer"]["resource_id"],
                    "owner_type": "resource",
                },
            )

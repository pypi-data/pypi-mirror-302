import asyncio
from pathlib import Path
from typing import Optional, List

from onepassword import Client, ItemField, VaultOverview, ItemOverview
from onepassword.types import Item
from .models import Config, FieldUpdate

__ctx = {}

def __get_client() -> Client:
    return __ctx["client"]


def __get_config() -> Config:
    return __ctx["config"]


async def init(env_path: Optional[Path] = None) -> None:
    __ctx["config"] = Config() if env_path is None else Config(_env_file=env_path)

    client = await Client.authenticate(
        auth=__get_config().service_token,
        integration_name="pj-stack",
        integration_version="v1.0.0",
    )

    __ctx["client"] = client


async def load_secret(op_path: str) -> str:
    client = __get_client()
    return await client.secrets.resolve(f"op://{op_path}")


async def update_secret(
    item_name: str, vault_name: str, fields: List[FieldUpdate]
) -> Item:
    client = __get_client()

    vault = await get_vault_by_name(vault_name)
    item_overview = await get_item_by_name(vault.id, item_name)
    item = await client.items.get(vault_id=vault.id, item_id=item_overview.id)
    for field in fields:
        filtered_fields_indices = [
            ndx for ndx, f in enumerate(item.fields) if f.title == field.title
        ]
        if len(filtered_fields_indices) == 0:
            raise ValueError(f"field {field.title} does not exist")

        item.fields[filtered_fields_indices[0]].value = field.new_value
    updated_item = await client.items.put(item)
    return updated_item


async def get_vault_by_name(name: str) -> VaultOverview:
    client = __get_client()

    vaults = await client.vaults.list_all()
    async for vault in vaults:
        if vault.title == name:
            return vault


async def get_item_by_name(vault_id: str, name: str) -> ItemOverview:
    client = __get_client()
    items = await client.items.list_all(vault_id=vault_id)

    async for item in items:
        if item.title == name:
            return item


if __name__ == "__main__":

    async def main() -> None:
        await init()
        await update_secret("dummy", "fake", "test", "1234")

    asyncio.run(main())

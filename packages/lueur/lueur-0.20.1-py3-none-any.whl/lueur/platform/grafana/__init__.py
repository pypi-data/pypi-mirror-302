import asyncio
import secrets
from typing import Any, Literal, Sequence, cast

from lueur.make_id import make_id
from lueur.models import Discovery, Meta
from lueur.platform.grafana.slo import expand_links as slo_expand_links
from lueur.platform.grafana.slo import explore_slo

__all__ = ["explore", "expand_links"]

Targets = ("slo",)


async def explore(
    stack_url: str,
    token: str,
    include: Sequence[Literal["slo",]] | None = None,
) -> Discovery:
    resources = []
    tasks: list[asyncio.Task] = []

    if include is None:
        include = cast(Sequence, Targets)

    async with asyncio.TaskGroup() as tg:
        if "slo" in include:
            tasks.append(tg.create_task(explore_slo(stack_url, token)))

    for task in tasks:
        result = task.result()
        if result is None:
            continue
        resources.extend(result)

    name = secrets.token_hex(8)

    return Discovery(
        id=make_id(name),
        resources=resources,
        meta=Meta(name=name, display="Grafana", kind="grafana", category=None),
    )


def expand_links(d: Discovery, serialized: dict[str, Any]) -> None:
    slo_expand_links(d, serialized)

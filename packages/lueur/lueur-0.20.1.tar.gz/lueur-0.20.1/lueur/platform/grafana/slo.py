# mypy: disable-error-code="index,call-arg,union-attr"
import logging
from typing import Any

import httpx
import msgspec

from lueur.make_id import make_id
from lueur.models import Discovery, K8SMeta, Resource
from lueur.platform.grafana.client import Client

__all__ = ["explore_slo", "expand_links"]
logger = logging.getLogger("lueur.lib")


async def explore_slo(
    stack_url: str,
    token: str,
) -> list[Resource]:
    resources = []

    async with Client(stack_url, token) as c:
        nodes = await explore_slos(c)
        resources.extend(nodes)

    return resources


###############################################################################
# Private functions
###############################################################################
async def explore_slos(c: httpx.AsyncClient) -> list[Resource]:
    response = await c.get("/api/plugins/grafana-slo-app/resources/v1/slo")

    if response.status_code == 403:
        logger.warning("Grafana API authentication failed")
        return []

    slos = msgspec.json.decode(response.content)

    results = []
    for slo in slos["items"]:
        results.append(
            Resource(
                id=make_id(slo["id"]),
                meta=K8SMeta(
                    name=slo["name"],
                    display=slo["name"],
                    kind="slo",
                    platform="grafana",
                    category="observability",
                ),
                struct=slo,
            )
        )

    return results


def expand_links(d: Discovery, serialized: dict[str, Any]) -> None:
    pass

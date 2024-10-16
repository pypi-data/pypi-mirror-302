# mypy: disable-error-code="call-arg,index"
import logging

import msgspec
from kubernetes import client

from lueur.make_id import make_id
from lueur.models import K8SMeta, Resource
from lueur.platform.k8s.client import AsyncClient, Client

__all__ = ["explore_service"]
logger = logging.getLogger("lueur.lib")


async def explore_service() -> list[Resource]:
    resources = []

    async with Client(client.CoreV1Api) as c:
        services = await explore_services(c)
        resources.extend(services)

    return resources


###############################################################################
# Private functions
###############################################################################
async def explore_services(c: AsyncClient) -> list[Resource]:
    f = "list_service_for_all_namespaces"
    response = await c.execute(f)

    if response.status == 403:
        logger.warning("Kubernetes API server failed authentication")
        return []

    if response.status == 404:
        logger.warning(f"Kubernetes API server '{f}' not found")
        return []

    services = msgspec.json.decode(response.data)

    if "items" not in services:
        logger.warning(f"No services found: {services}")
        return []

    results = []
    for service in services["items"]:
        meta = service["metadata"]
        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=K8SMeta(
                    name=meta["name"],
                    display=meta["name"],
                    kind="service",
                    platform="k8s",
                    ns=meta["namespace"],
                    category="network",
                ),
                struct=service,
            )
        )

    return results

# mypy: disable-error-code="call-arg,index"
import logging
from typing import Any

import msgspec
from kubernetes import client

from lueur.links import add_link
from lueur.make_id import make_id
from lueur.models import Discovery, K8SMeta, Link, Resource
from lueur.platform.k8s.client import AsyncClient, Client
from lueur.rules import iter_resource

__all__ = ["explore_deployment"]
logger = logging.getLogger("lueur.lib")


async def explore_deployment() -> list[Resource]:
    resources = []

    async with Client(client.AppsV1Api) as c:
        pods = await explore_deployments(c)
        resources.extend(pods)

    return resources


###############################################################################
# Private functions
###############################################################################
async def explore_deployments(c: AsyncClient) -> list[Resource]:
    f = "list_deployment_for_all_namespaces"
    response = await c.execute(f)

    if response.status == 403:
        logger.warning("Kubernetes API server failed authentication")
        return []

    if response.status == 404:
        logger.warning(f"Kubernetes API server '{f}' not found")
        return []

    deployments = msgspec.json.decode(response.data)

    if "items" not in deployments:
        logger.warning(f"No deployments found: {deployments}")
        return []

    results = []
    for deployment in deployments["items"]:
        meta = deployment["metadata"]
        results.append(
            Resource(
                id=make_id(meta["uid"]),
                meta=K8SMeta(
                    name=meta["name"],
                    display=meta["name"],
                    kind="deployment",
                    platform="k8s",
                    ns=meta["namespace"],
                    category="compute",
                ),
                struct=deployment,
            )
        )

    return results


def expand_links(d: Discovery, serialized: dict[str, Any]) -> None:
    for deployment in iter_resource(
        serialized,
        "$.resources[?@.meta.kind=='deployment' && @.meta.platform=='k8s'].meta.name",  # noqa: E501
    ):
        r_id = deployment.parent.parent.obj["id"]  # type: ignore
        name = deployment.value

        p = f"$.resources[?@.meta.kind=='replicaset'].struct.metadata.ownerReferences[?@.kind=='Deployment' && @.name=='{name}']"  # noqa E501
        for ownerRef in iter_resource(serialized, p):
            rs = ownerRef.parent.parent.parent.parent  # type: ignore
            add_link(
                d,
                r_id,
                Link(
                    direction="out",
                    kind="replicaset",
                    path=rs.path,  # type: ignore
                    pointer=str(rs.pointer()),  # type: ignore
                ),
            )

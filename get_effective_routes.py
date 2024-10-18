import asyncio
import aiohttp
from azure.identity import DefaultAzureCredential
from azure.mgmt.network.aio import NetworkManagementClient
import logging
from pprint import pprint

"""
# PREREQUISITES: az login
# Usage: python get_effective_routes.py
"""

# Uncomment for troubleshooting
# logging.basicConfig(
#     format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

async def async_get_effective_routes(client, resource_group, virtual_hub_name, hub_route_table_name, subscription_id):
    """
    Retrieve effective routes for a single virtual hub asynchronously.

    Args:
        client (NetworkManagementClient): The network management client.
        resource_group (str): The name of the resource group.
        virtual_hub_name (str): The name of the virtual hub.
        hub_route_table_name (str): The name of the hub route table.
        subscription_id (str): The subscription ID.

    Returns:
        None
    """
    body = {
        "resource_id": f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Network/virtualHubs/{virtual_hub_name}/hubRouteTables/{hub_route_table_name}",
        "virtual_wan_resource_type": "RouteTable"
    }

    response = await client.virtual_hubs.begin_get_effective_virtual_hub_routes(
        resource_group_name=resource_group,
        virtual_hub_name=virtual_hub_name,
        effective_routes_parameters=body
    ).result()

    for route in response.value:
        pprint(
            {"address_prefix": route.address_prefixes, 
             "next_hops": route.next_hops, 
             "next_hop_type": route.next_hop_type, 
             "as_path": route.as_path, 
             "route_origin": route.route_origin}
        )

async def async_main(hubs, subscription_id):
    """
    Iterate over a list of hubs and retrieve effective routes asynchronously.

    Args:
        hubs (list): A list of dictionaries containing hub information.
        subscription_id (str): The subscription ID.

    Returns:
        None
    """
    credential = DefaultAzureCredential()
    client = NetworkManagementClient(
        credential=credential,
        subscription_id=subscription_id,
    )

    tasks = []
    for hub in hubs:
        resource_group = hub["resource_group"]
        virtual_hub_name = hub["virtual_hub_name"]
        hub_route_table_name = hub.get("hub_route_table_name", "defaultRouteTable")
        tasks.append(async_get_effective_routes(client, resource_group, virtual_hub_name, hub_route_table_name, subscription_id))

    await asyncio.gather(*tasks)

def main():
    """
    Main function to run the async method for retrieving effective routes.

    Returns:
        None
    """
    hubs = [
        {"resource_group": "", "virtual_hub_name": ""},
        # Add more hubs as needed
    ]
    subscription_id = ""

    asyncio.run(async_main(hubs, subscription_id))

if __name__ == "__main__":
    main()

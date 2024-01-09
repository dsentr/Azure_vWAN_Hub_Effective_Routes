from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
import logging
from pprint import pprint

"""
# PREREQUISITES: az login
# Usage: python get_effective_routes.py
"""

# Uncomment for troubleshooting
# logging.basicConfig(
#     format='%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

def main():
    RESOURCE_GROUP = ""
    VIRTUAL_HUB_NAME = ""
    HUB_ROUTE_TABLE_NAME = "defaultRouteTable"
    SUBSCRIPTION_ID=""

    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID,
    )
    
    BODY = {
        "resource_id": "/subscriptions/" + SUBSCRIPTION_ID + "/resourceGroups/" + RESOURCE_GROUP + "/providers/Microsoft.Network/virtualHubs/" + VIRTUAL_HUB_NAME + "/hubRouteTables/" + HUB_ROUTE_TABLE_NAME,
        "virtual_wan_resource_type": "RouteTable"
    }
    

    response = client.virtual_hubs.begin_get_effective_virtual_hub_routes(
        resource_group_name=RESOURCE_GROUP,
        virtual_hub_name=VIRTUAL_HUB_NAME,
        effective_routes_parameters=BODY
    ).result()

    for route in response.value:
        pprint(
            {"address_prefix": route.address_prefixes, 
             "next_hops": route.next_hops, 
             "next_hop_type": route.next_hop_type, 
             "as_path": route.as_path, 
             "route_origin": route.route_origin}
             )

if __name__ == "__main__":
    main()

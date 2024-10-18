# Azure_vWAN_Hub_Effective_Routes

## Overview

To list effective routes on an Azure vWAN Hub using the Azure SDK for Python, run this script for each Hub.

```sh
pip install -r requirements.txt
python get_effective_routes.py
```

## Asynchronous Method

To list effective routes on multiple Azure vWAN Hubs asynchronously using the Azure SDK for Python, run this script:

```sh
pip install -r requirements.txt
python get_effective_routes.py
```

Make sure to update the `hubs` list and `subscription_id` in the `main` function of `get_effective_routes.py` with the appropriate values.

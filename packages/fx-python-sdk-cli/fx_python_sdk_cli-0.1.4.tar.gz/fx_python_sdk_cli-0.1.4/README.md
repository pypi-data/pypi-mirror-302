# FX Python SDK with CLI

Usage: `pip install fx_python_sdk_cli`

Enter Provider / Consumer FX-Port details in the config files `consumer_cfg` and `provider_cfg`.

Use CLI as provider:
- Get own EDC Assets
- Create EDC Asset for AAS Submodel
- Create generic EDC Access policy
- Create generic EDC Usage policy
- Create generic EDC Contract for specific EDC Asset
- Get EDC policies

Use CLI as consumer:
- Request EDC Assets from Provider
- Request EDRS (after negotiation)
- Request data (requires EDRS)
- Negotiate
- Get Negotiation State (to check after negotiating)

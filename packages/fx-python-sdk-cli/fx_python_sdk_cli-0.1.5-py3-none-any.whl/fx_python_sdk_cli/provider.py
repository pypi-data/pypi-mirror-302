import requests # Apache License 2.0
from requests.auth import HTTPBasicAuth

import uuid
import base64   # in python
import yaml     # MIT
import os

from .utils import make_create_secure_asset_body, create_generic_Access_PolicyDefinitionRequest_body, create_generic_Usage_PolicyDefinitionRequest_body, create_generic_ContractDefinitionRequest_body, print_edc_assets

current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_file_path = os.path.join(current_dir, 'provider_cfg.yaml')

# --- variables ---
with open(yaml_file_path, 'r') as file:
    provider_cfg = yaml.safe_load(file)

# - control plane -
url_edc_provider_control_plane_base = provider_cfg['provider-edc-control-plane']['endpoint']
header_control_plane = provider_cfg['provider-edc-control-plane']['header'] # this contains secrets, so please use -at least- a secretsmanager instead

# construct urls based on standard:
url_edc_provider_asset_management    = url_edc_provider_control_plane_base + "/management/v3/assets"
url_edc_provider_policy_management   = url_edc_provider_control_plane_base + "/management/v2/policydefinitions"
url_edc_provider_contract_management = url_edc_provider_control_plane_base + "/management/v2/contractdefinitions"


# - "identities" -
edc_consumer_bpn = provider_cfg['trusted-consumers-bpn']['consumer_A']


# - submodel repository -
submodel_repo_url = provider_cfg['submodel-repository']['endpoint'] 
proxy_auth_header = provider_cfg['submodel-repository']['authtoken'] 

def request_own_assets():
    # look up the existing assets:
    res_get_assets = requests.post(url_edc_provider_asset_management + "/request", headers=header_control_plane)
    print_edc_assets(res_get_assets)

def create_edc_asset(edc_asset_id):    
    # - create EDC-Asset -
    # the asset  here is a submodel
    uuid_base = base64.b64encode(edc_asset_id.encode('utf-8')).decode('utf-8')
    target_url = submodel_repo_url + "/submodels/" + uuid_base
    print(target_url)
    edc_asset_type = "Submodel" # according to https://w3id.org/catenax/taxonomy#Submodel

    create_asset_body = make_create_secure_asset_body(edc_asset_id, edc_asset_type, target_url, proxy_auth_header)
    # register asset:
    res_create_edc_asset = requests.post(url_edc_provider_asset_management, headers=header_control_plane, json=create_asset_body)
    res_create_edc_asset
    # - check if the asset exists already -
    # look up the existing assets 
    res_get_assets = requests.post(url_edc_provider_asset_management + "/request", headers=header_control_plane)

    if res_get_assets.status_code == 200:
        asset_ids = [retrived_asset["@id"] for retrived_asset in res_get_assets.json()]
        if  edc_asset_id in asset_ids:
            print('Asset already exists ... resolving conflict via update')
        else:
            print("Asset doesn't exist, conflict reason unknown.")

    else:
        print('Request Error: ' + str(res_get_assets.status_code))
    # create:
    res_update_edc_asset = requests.put(url_edc_provider_asset_management, headers=header_control_plane, json=create_asset_body)
    print(res_update_edc_asset)

# # remove assets:
# asset_deletion_body = {
#     "@context": "https://w3id.org/edc/v0.0.1/ns/",    
#     "@id": "test_AAS_registration_C_3",
# }
# res_delete_edc_asset = requests.delete(url_edc_provider_asset_management, headers=header_control_plane, json=create_asset_body)
# res_delete_edc_asset
# ------------------------------------------------------------------------------------------------------

def create_access_policy():
    ### Attaching a Policy to the created Asset
    # create access policy:
    create_access_policy_body = create_generic_Access_PolicyDefinitionRequest_body("access-policy-generic"+uuid.uuid4(), edc_consumer_bpn, policy_action="use")

    res_create_asset_access_plicy = requests.post(url_edc_provider_policy_management, headers=header_control_plane, json=create_access_policy_body)
    res_create_asset_access_plicy # post against: "{{EDCTX-10-1-URL}}/management/v2/policydefinitions"

def create_usage_policy():    
    # create usage policy:
    create_usage_policy_body = create_generic_Usage_PolicyDefinitionRequest_body("usage-policy-generic"+uuid.uuid4(), policy_action="use") 

    res_create_asset_usage_plicy = requests.post(url_edc_provider_policy_management, headers=header_control_plane, json=create_usage_policy_body)
    res_create_asset_usage_plicy # post against: "{{EDCTX-10-1-URL}}/management/v2/policydefinitions"

def create_contract(edc_asset_id):
    # create contract:
    create_access_policy_body = create_generic_Access_PolicyDefinitionRequest_body("access-policy-generic"+uuid.uuid4(), edc_consumer_bpn, policy_action="use")
    access_policy_id = create_access_policy_body['@id']
    create_usage_policy_body = create_generic_Usage_PolicyDefinitionRequest_body('usage-policy-generic'+uuid.uuid4(), policy_action="use") 
    usage_policy_id  = create_usage_policy_body['@id']
    edc_asset_type = "Submodel" # according to https://w3id.org/catenax/taxonomy#Submodel
    uuid_base = base64.b64encode(edc_asset_id.encode('utf-8')).decode('utf-8')
    target_url = submodel_repo_url + "/submodels/" + uuid_base
    create_asset_body = make_create_secure_asset_body(edc_asset_id, edc_asset_type, target_url, proxy_auth_header)
    asset_id         = create_asset_body['@id']

    create_contract_body = create_generic_ContractDefinitionRequest_body(asset_id, 'contract-generic'+uuid.uuid4(), access_policy_id, usage_policy_id)

    res_create_asset_contract = requests.post(url_edc_provider_contract_management, headers=header_control_plane, json=create_contract_body)
    res_create_asset_contract # post against: "url": "{{EDCTX-10-1-URL}}/management/v2/contractdefinitions"

def get_policies():    
    # - which policies are registered with the provider -
    res_policies = requests.post(url_edc_provider_contract_management + "/request", headers=header_control_plane)
    print(res_policies)

    print("{idx:8} {id:28} {asset_id:42} {accespolicy:28} {usagepolicy:28}".format(idx="Index", id="id", asset_id="Asset", accespolicy="Access Policy", usagepolicy="Usage Policy"))
    print("-"*8 + " " + "-"*28 + " " + "-"*42 + " " + "-"*28 + " " + "-"*28)

    for idx, retrived_contract in enumerate(res_policies.json()):
        # get asset
        try:   
            asset_ = retrived_contract['assetsSelector'][0]['operandRight']
        except:
            try:  # please don't do this ...
                asset_ = retrived_contract['assetsSelector']['operandRight']
            except:
                asset_ = "None"
        print("{idx:8} {id:28} {asset_id:42} {accespolicy:28} {usagepolicy:28}".format(idx=str(idx)+ ":", id=retrived_contract["@id"], 
                                                    asset_id=asset_,
                                                    accespolicy=retrived_contract['accessPolicyId'], 
                                                    usagepolicy=retrived_contract['contractPolicyId']))
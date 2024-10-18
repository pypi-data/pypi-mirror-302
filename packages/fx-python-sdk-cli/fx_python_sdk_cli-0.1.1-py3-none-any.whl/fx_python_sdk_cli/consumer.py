import requests # Apache License 2.0
from requests.auth import HTTPBasicAuth

import base64   # in python
import yaml     # MIT
import json

from utils import get_data_offer, offer2et, create_poc_ContractRequest_body
from utils import str_edc_catalog

# --- variables ---
with open('consumer_cfg.yaml', 'r') as file:
    consumer_cfg = yaml.safe_load(file)

# - control plane -
url_edc_consumer_control_plane_base = consumer_cfg['consumer-edc-control-plane']['endpoint']
header_control_plane = consumer_cfg['consumer-edc-control-plane']['header'] # this contains secrets, so please use -at least- a secretsmanager instead

# - "identities" -
edc_provider_bpn = consumer_cfg['trusted-providers']['provider_A']['BPN']  # "{{EDCTX-10-1-BPN}}"
url_edc_provider_control_plane_base = consumer_cfg['trusted-providers']['provider_A']['endpoint-control-plane']
# -------------------------------------------------------------------------------------------------------------------
object_of_agreement = 'MB-DSCS'#'simple_test' # we 'magically' know this due to the push notification

def get_edrs_for_object(object_of_agreement):
    # see if there are some edrs which have been negotiated for
    # Load the JSON from the file
    with open('agreement_body.json', 'r') as f:
        loaded_agreement_body = json.load(f)

    # Replace the placeholder with the actual object of agreement
    loaded_agreement_body["filterExpression"][0]["operandRight"] = object_of_agreement

    res_catalog_agreement = requests.post(url=url_edc_consumer_control_plane_base + '/management/v2/edrs/request', headers=header_control_plane, json=loaded_agreement_body)
    #res_catalog_agreement
    res_offer, offer = get_data_offer(res_catalog_agreement.json())
    print("Status Offer: "+ str(res_offer))

    if res_offer == 0:
        res_et, et_dict = offer2et(offer, url_edc_consumer_control_plane_base, header_control_plane)
        if res_et == -2:
            print("Token Request Failed:" + str(et_dict))
        else:
            print("Status Endpoint and Token: " + str(res_et))
        return et_dict
    
def get_data(et_dict):
    # obtain data:
    res_data_info = requests.get(url=et_dict['endpoint'], headers={'Authorization': et_dict['token']})
    res_data_info
    res_data = requests.get(url=et_dict['endpoint'] + '/$value?extent=WithBlobValue', headers={'Authorization': et_dict['token']})
    res_data
    element_id = res_data_info.json()['submodelElements'][0]['idShort']
    value_enc  = res_data.json()[element_id]['value']
    val = res_data.json()[res_data_info.json()['submodelElements'][0]['idShort']]['value']
    base64.b64decode(val).decode('utf-8')

def request_assets_from_provider():
     # obtain all offers from the data provider using a catalog request:
    # Load the JSON from the file
    with open('catalog_request_body', 'r') as f:
        loaded_catalog_request_body = json.load(f)
    # Replace the placeholders with actual values
    loaded_catalog_request_body["counterPartyId"] = edc_provider_bpn
    loaded_catalog_request_body["counterPartyAddress"] = url_edc_provider_control_plane_base + "/api/v1/dsp"
    # note: we query against our own EDC (the consumer EDC, who then will negotiate with the target EDC)
    res_catalog = requests.post(url=url_edc_consumer_control_plane_base + '/management/v2/catalog/request', headers=header_control_plane, json=loaded_catalog_request_body)
    print(str_edc_catalog(res_catalog))
    return res_catalog

def negotiate(object_of_agreement):
    ### Negotiate for Asset
    res_catalog = request_assets_from_provider()
    # filter offer and endpoint
    for dcat_dataset in res_catalog.json()['dcat:dataset']:
        # look for the dataset with our id:
        if dcat_dataset['@id'] == object_of_agreement:
            asset_policy = dcat_dataset['odrl:hasPolicy']
            offer_id     = asset_policy['@id']

            # get negotiation endpoint: dct_endpointUrl
            dct_endpointUrl = None
            for distribution_method in dcat_dataset['dcat:distribution']:
                if distribution_method['dct:format']['@id'] == 'HttpData-PULL':
                    dct_endpointUrl = distribution_method['dcat:accessService']['dct:endpointUrl']
                    break
            # check if we actuall got the desired endpoint        
            if dct_endpointUrl is not None:
                break

    # create request body for the EDR negotiate
    edr_negotiation_body = create_poc_ContractRequest_body(dct_endpointUrl, offer_id, edc_provider_bpn, object_of_agreement)
    res_edr_negotiation  = requests.post(url=url_edc_consumer_control_plane_base + '/management/v2/edrs', headers=header_control_plane, json=edr_negotiation_body)
    #res_edr_negotiation		
    edr_negotation_id = res_edr_negotiation.json()['@id']
    return edr_negotation_id   # <- necessary to get the state 

def get_negotiation_state(edr_negotation_id):
    # get the negotiation state:
    res_get_edr_negotiation_state = requests.get(url=url_edc_consumer_control_plane_base + '/management/v2/contractnegotiations/' + edr_negotation_id + '/state', headers=header_control_plane)
    res_get_edr_negotiation_state
    res_get_edr_negotiation_state.json()    # <- this should say finalized
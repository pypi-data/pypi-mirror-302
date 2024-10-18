from consumer import *
from provider import *

def provider_interface():
    while True:
        print("1: Get own EDC Assets")
        print("2: Create EDC Asset for AAS Submodel")
        print("3: Create generic EDC Access policy")
        print("4: Create generic EDC Usage policy")
        print("5: Create generic EDC Contract for specific EDC Asset")
        print("6: Get EDC policies")
        print("7: Return")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Getting assets...")
            request_own_assets()
        elif choice == "2":
            asset_id = input("Enter submodel uuid: ")
            print("Creating asset for...")
            create_edc_asset(asset_id)
        elif choice == "3":
            print("Creating access policy...")
            create_access_policy()
        elif choice == "4":
            print("Creating usage policy...")
            create_usage_policy()
        elif choice == "5":
            print("Creating contract...")
            edc_asset_id = input("Enter EDC asset id: ")
            create_contract(edc_asset_id)
        elif choice == "6":
            print("Getting policies...")
            get_policies()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

def client_interface():
    while True:
        print("1: Request EDC Assets from Provider")
        print("2: Request EDRS (after negotiation)")
        print("3: Request data (requires EDRS)")
        print("4: Negotiate")
        print("5: Get Negotiation State (check after step 4)")
        print("6: Return")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Requesting assets...")
            request_assets_from_provider()
        elif choice == "2":
            object_of_agreement = input("Enter id of EDC asset: ")
            print("Requesting EDRS...")
            edrs = get_edrs_for_object(object_of_agreement)
        elif choice == "3":
            object_of_agreement = input("Enter id of EDC asset: ")
            print("Requesting data...")
            get_data(edrs)
        elif choice == "4":
            object_of_agreement = input("Enter id of EDC asset: ")
            print("Negotiating...")
            edr_negotation_id = negotiate(object_of_agreement)
        elif choice == "5":
            print("Getting state...")
            get_negotiation_state(edr_negotation_id)    
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    while True:
        print("1: Provider")
        print("2: Client")
        print("3: Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            provider_interface()
        elif choice == "2":
            client_interface()
        elif choice == "3":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
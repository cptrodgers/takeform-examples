import requests
import time
import json

TAKE_FORM_API_KEY="YOUR_API_KEY"

# This is W-9 Form. You can view here https://platform.takeform.app/forms/854d35dc-c401-4079-aadc-63c309a052e8
FORM_ID="854d35dc-c401-4079-aadc-63c309a052e8"

# JSON Input Sample form W-9 Form Above.
mapping_data = {
	"address_line_1": "123 Main St",
	"business_name_disregarded_entity_name": "Acme Corp",
	"city_state_zip": "Anytown, CA, 91234",
	"exemptions": {
		"exempt_payee_code": "4",
		"exemption_from_fatca_reporting_code": "A"
	},
	"federal_tax_classification": {
		"c_corporation": True,
		"individual_sole_proprietor": False,
		"llc_checkbox": False,
		"other_classification_checkbox": False,
		"partnership": False,
		"s_corporation": False,
		"trust_estate": False
	},
	"foreign_partners_owners_beneficiaries_indicator": False,
	"list_account_numbers": "12345, 67890",
	"name_of_entity_individual": "John Doe",
	"requester_name_address": "Jane Smith\n456 Elm St\nAnytown, CA 91234",
	"taxpayer_identification_number": {
		"ein_part_1": "12",
		"ein_part_2": "3456789"
	}
}

def fill_form():
    url = f"https://api.takeform.app/developer/v1/forms/{FORM_ID}/fill"
    headers = {
        'X-API-Key': TAKE_FORM_API_KEY,
        'Content-Type': 'application/json; charset=utf-8',
    }

    response = requests.post(
        url,
        headers=headers,
        json={
            "mapping": mapping_data,
        },
    )
    print("Fill succesfully: Filled Form Object", response.json())
    # Expected Output: Fill succesfully: Filled Form Object {'created_at': 1744736364, 'file_id': '4a1609c5-7113-4f11-b22d-af70d40f9bed', 'filled_via': 'Api', 'form_id': '854d35dc-c401-4079-aadc-63c309a052e8', 'id': 'e31c24cc-6883-4e52-ab9b-474601d89543', 'name': 'w-9.pdf', 'status': 'Filling', 'updated_at': 1744736363, 'user_id': 'df0bebb1-c460-4263-a654-6d9f5dda7428'}

    return response.json()["id"]


def download_form(filled_form_id: str):
    url = f"https://api.takeform.app/developer/v1/filled-forms/{filled_form_id}/download-url"
    headers = {
        'X-API-Key': TAKE_FORM_API_KEY,
        'Content-Type': 'application/json; charset=utf-8',
    }

    response = requests.get(
        url,
        headers=headers,
    )
    print("Filled Form", response.json())
    # Output: Filled Form https://storage.googleapis.com/takeform/8da53c8c-5334-4ebb-8074-a1c6cd79d1ca?...


filled_form_id = fill_form()
time.sleep(5)
download_form(filled_form_id)

import requests
import time
import json

TAKE_FORM_API_KEY=""

# This is W-9 Form. You can view here https://platform.takeform.app/forms/854d35dc-c401-4079-aadc-63c309a052e8
FORM_ID="854d35dc-c401-4079-aadc-63c309a052e8"

# JSON Input Sample form W-9 Form Above.
mapping_data = {
	"address_line_1": "123 Main St",
	"business_name_disregarded_entity_name": "Acme Corp",
	"foreign_partners_owners_beneficiaries_indicator": False,
	"name_of_entity_individual": "John Doe",
	"requester_name_address": "Jane Smith\n456 Elm St\nAnytown, CA 91234"
}

# Dynamic Data, Free Text
dynamic_text_data = """
City, State, ZIP: Anytown, CA, 91234

Federal Tax Classification:
C Corporation: true

Exemptions:
Exempt Payee Code: 4
Exemption from FATCA Reporting Code: A

List of Account Numbers:
12345, 67890

Taxpayer Identification Number (EIN):
12-3456789
"""

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
            "dynamic": {
                "sources": [
                    {
                        "type": "Text",
                        "text": dynamic_text_data
                    },
                ]
            }
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
time.sleep(15)
download_form(filled_form_id)

import requests

TAKE_FORM_API_KEY=""

# Read more about TakeForm Webhook at: https://takeform.gitbook.io/docs/api-developer/api-webhook
def webhook_handler(filled_form):
    if filled_form.get("status") == "Done":
        print("Form is completed, download it")
        download_form(filled_form.get("id"))



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

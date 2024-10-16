# leosheet
 Python SDK for Google Sheet Interaction

## installation
```
pip install leosheet
```

## Steps
1. put a `.secrest.toml` file in the save folder as your main python scritp, say `main.py`
    ```toml
    private_gsheets_url=""

    [gcp_service_account]
    type = "service_account"
    project_id = "xxx"
    private_key_id = "xxx"
    private_key = "xxx"
    client_email = "xxx"
    client_id = "xxx"
    auth_uri = "https://accounts.google.com/o/oauth2/auth"
    token_uri = "https://oauth2.googleapis.com/token"
    auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
    client_x509_cert_url = "xxx"
    ```

    You can get this data by refering to https://docs.streamlit.io/develop/tutorials/databases/gcs

2. run your main python script `python main.py`
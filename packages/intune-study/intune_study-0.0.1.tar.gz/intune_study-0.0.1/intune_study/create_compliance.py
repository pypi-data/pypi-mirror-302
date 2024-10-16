import requests
import json

# Function to get the access token using OAuth 2.0
def get_access_token(tenant_id, client_id, client_secret):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        'client_id': client_id,
        'scope': 'https://graph.microsoft.com/.default',
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()['access_token']

# Function to create a device compliance policy in Intune
def create_compliance_policy(tenant_id, client_id, client_secret):
    access_token = get_access_token(tenant_id, client_id, client_secret)
    url = "https://graph.microsoft.com/v1.0/deviceManagement/deviceCompliancePolicies"
    
    # Define your Windows 10 compliance policy configuration
    payload = {
        "@odata.type": "#microsoft.graph.windows10CompliancePolicy",
        "displayName": "Windows 10 Compliance Policy",
        "description": "Compliance policy for ensuring device security on Windows 10",
        "passwordRequired": True,
        "passwordMinimumLength": 8,
        "passwordMinutesOfInactivityBeforeLock": 15,
        "passwordExpirationDays": 90,
        "passwordPreviousPasswordBlockCount": 5,
        "osMinimumVersion": "10.0.19041.0",
        "storageRequireEncryption": True,
        "deviceThreatProtectionEnabled": True,
        "deviceThreatProtectionRequiredSecurityLevel": "high",
        "scheduledActionsForRule": [
            {
                "ruleName": "PasswordRequired",
                "scheduledActionConfigurations": [
                    {
                        "actionType": "block",
                        "gracePeriodHours": 72,
                        "notificationMessageCCList": []
                    }
                ]
            }
        ]
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code == 201:
        print("Device Compliance Policy created successfully.")
    else:
        print(f"Failed to create device compliance policy: {response.status_code}, {response.text}")

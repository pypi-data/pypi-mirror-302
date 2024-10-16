# DeviceComp

**DeviceComp** is a Python package designed to interact with Microsoft Intune via the Microsoft Graph API. It allows users to create and manage device compliance policies programmatically by passing necessary credentials directly into the functions.

## Features

- Create device compliance policies in Microsoft Intune.
- Retrieve access tokens via OAuth 2.0 for API authentication.
- Easily pass Azure credentials (tenant ID, client ID, client secret) as parameters.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-repo-url.git
cd DeviceComp


import my_package.compliance_policy as compliance

# User-provided credentials
tenant_id = "<your-tenant-id>"
client_id = "<your-client-id>"
client_secret = "<your-client-secret>"

# Create a device compliance policy
compliance.create_compliance_policy(tenant_id, client_id, client_secret)

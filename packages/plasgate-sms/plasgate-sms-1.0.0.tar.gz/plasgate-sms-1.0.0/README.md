# Plasgate SMS API Client

`plasgate` is a powerful Python library designed for seamless interaction with the Plasgate SMS API. It enables users to send SMS messages effortlessly and manage One-Time Passwords (OTPs) with ease.

## Features

- **Send SMS Messages**: Quickly send individual or batch SMS messages.
- **OTP Management**: Generate and validate OTPs for secure authentication.
- **Delivery Reports**: Track message delivery status with optional callbacks.
- **Batch Processing**: Efficiently send messages to multiple recipients in a single request.

## Installation

To install the `plasgate` library, use pip. Open your terminal and execute the following command:

```bash
pip install plasgate-sms
```

## Configuration

Before using the library, ensure you have your API keys from Plasgate. You'll need:

- **Private Key**: Unique identifier for your account.
- **Secret Key**: Used for authenticating requests.

These can usually be found in your Plasgate account settings.

## Usage

### Single Sending

To send a single SMS message, follow this example:

```python
from plasgate.rest import Client

# Initialize client with your API credentials
private = "PLASGATE_PRIVATE_KEY_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
secret = "PLASGATE_SECRET_KEY_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

client = Client(private, secret)

# Send a message
response = client.messages.create(
    to="855972432661",
    sender="PlasGate",  # Your sender ID
    content="TestAPI",   # Message content
    dlr="yes",           # Delivery report request
    dlr_url="https://webhook-test.com/273e777973dc8334bbaa2ef63f3d9cf6",  # URL for delivery reports
)

print(response)
```

### Batch Sending

For sending messages to multiple recipients at once, you can use batch sending:

```python
from plasgate.rest import Client

# Initialize client with your API credentials
private = "PLASGATE_PRIVATE_KEY_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
secret = "PLASGATE_SECRET_KEY_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

client = Client(private, secret, batch_sending=True)

# Send batch messages
response = client.messages.create(
    messages=[
        {"to": ["85581848677", "855972432661"], "content": "Test plasgate client"}
    ],
    globals={
        "sender": "PlasGate",  # Sender ID for all messages
        "dlr": "yes",           # Request delivery reports
        "dlr_level": 3,         # Level of detail for delivery reports
        "dlr_url": "https://webhook-test.com/273e777973dc8334bbaa2ef63f3d9cf6",  # URL for delivery reports
    },
)

print(response)
```

### Twilio Migration

If you are migrating from Twilio, you can use the same structure with Plasgate:

```python
from plasgate.rest import Client

# Initialize client with your API credentials
account_sid = "PLASGATE_PRIVATE_KEY_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
auth_token = "PLASGATE_SECRET_KEY_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

client = Client(account_sid, auth_token)

# Send a message using the Twilio-like syntax
message = client.messages.create(
    to="+855972432661",  # Recipient's number
    from_="PlasGate",    # Your sender ID
    body="Hello from Python!"  # Message body
)

print(message)
```

## Additional Considerations

- **Error Handling**: Ensure you implement error handling to manage any issues with sending messages (e.g., invalid numbers, network errors).
- **Rate Limiting**: Be aware of any rate limits imposed by Plasgate to avoid disruptions in service.
- **Secure Your Keys**: Always keep your API keys confidential and do not expose them in public repositories.

For more information and detailed documentation, please refer to the official Plasgate API documentation.

import requests

# Replace with your Speech Services subscription key
subscription_key = "3f80ab84124d4539aeef2610dab29da0"

# Replace with your Speech Services region
region = "eastus2"

# Replace with your Speech Services resource name
resource_name = "caito"

# The endpoint URL for listing transcriptions
endpoint = (
    f"https://{region}.api.cognitive.microsoft.com/speechtotext/v3.0/transcriptions"
)

# The headers for the GET request
headers = {
    "Ocp-Apim-Subscription-Key": subscription_key,
}

# Make the GET request
response = requests.get(endpoint, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # If successful, print out the list of transcriptions
    transcriptions = response.json()
    for transcription in transcriptions:
        print(transcription)
else:
    # If not successful, print out the error message
    print(f"Error: {response.status_code}")
    print(response.text)

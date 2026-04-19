import pandas as pd
import requests
import io


def fetch_valid_data():
    # List of possible URLs where Krish Sir might have the data
    urls = [
        "https://raw.githubusercontent.com/krishnaik06/NetworkSecurity/main/Network_Data/phisingData.csv",
        "https://raw.githubusercontent.com/krishnaik06/NetworkSecurity/refs/heads/main/Network_Data/phisingData.csv",
        "https://raw.githubusercontent.com/krishnaik06/The-Grand-Complete-Data-Science-Materials"
        "/main/Machine%20Learning/NetworkSecurity/phisingData.csv"
    ]

    for url in urls:
        print(f"Trying to fetch from: {url}")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text))
                df.to_csv("test.csv", index=False)
                print(f"✅ Success! Saved {len(df)} rows to test.csv")
                return df
            else:
                print(f"❌ Failed (Status {response.status_code})")
        except Exception as e:
            print(f"⚠️ Error: {e}")

    print("‼️ All sources failed. Please check your internet connection or the repository manually.")
    return None


if __name__ == "__main__":
    fetch_valid_data()

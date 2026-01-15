import requests
import json
import time

URL = "http://127.0.0.1:8080/api/v1/product/info"
TARGET_AMAZON_URL = "https://www.amazon.com/-/ko/dp/B00FLYWNYQ/ref=sr_1_1?_encoding=UTF8&content-id=amzn1.sym.8158743a-e3ec-4239-b3a8-31bfee7d4a15&dib=eyJ2IjoiMSJ9.Jcq8w8ngb1LGhnPudpuQJeCEN08eoApyis3Ufgp5uPfzTSf6EgvqLoCyigK1wiSRSTWR2UgWvh8fEWzWJ3mGQ1Z_ZWc0fbixlyb34ITzGLAdBl_gPhApgmG5h7dx18aaHLwy6mz30mtytDR4_v_R3goA-x-aKM2QbFlph9fm6xEaQcUfTHCSEVpBPo7UDc5CN8kjcuO10dd9jTASwPNYMc9O_hgVtoNuwRsuSHGoDXs.9eucKV9S0V-Xk42SV-5hiaO-YA0KCPuJdzVcSdZKmjE&dib_tag=se&keywords=cooker&pd_rd_r=223ba315-1f9e-43e5-9471-b32e970bb87a&pd_rd_w=sEl11&pd_rd_wg=jGb1B&qid=1768451625&sr=8-1&th=1"

def test_crawl():
    print(f"Testing URL: {TARGET_AMAZON_URL}")
    payload = {"url": TARGET_AMAZON_URL}
    
    try:
        response = requests.post(URL, json=payload, timeout=120)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response Data:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print("Error Response:")
            print(response.text)
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    # Wait a bit for server to stand up
    time.sleep(5)
    test_crawl()

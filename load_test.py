import requests
import threading
import time

URL = "http://localhost:3000/api/data"
NUM_REQUESTS = 150  # Enough to trigger the 100 request limit
CONCURRENT_THREADS = 10

def make_request(request_id):
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            print(f"Request {request_id}: Success (200)")
        elif response.status_code == 429:
            print(f"Request {request_id}: BLOCKED (429) - Rate Limit Exceeded")
        else:
            print(f"Request {request_id}: Status {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request {request_id}: Failed - {e}")

def run_load_test():
    print(f"Starting load test on {URL}")
    print(f"Sending {NUM_REQUESTS} requests...")
    
    threads = []
    for i in range(NUM_REQUESTS):
        t = threading.Thread(target=make_request, args=(i+1,))
        threads.append(t)
        t.start()
        
        # Adding a tiny delay to not completely overwhelm the local network stack instantly
        # and better simulate a burst of traffic
        if i % CONCURRENT_THREADS == 0:
            time.sleep(0.1)

    for t in threads:
        t.join()

    print("Load test completed.")

if __name__ == "__main__":
    run_load_test()

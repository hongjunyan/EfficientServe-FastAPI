from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import Counter
import requests
import time


def say_hello_to(url: str):
    _time = time.time()
    is_success = False
    resp = requests.get(url, timeout=30)
    if resp.status_code == 200:
        is_success = True
    response_time  = time.time() - _time
    return response_time, is_success


def test_performance(url: str, num_requests: int, num_threads: int):
    url_list = [url] * num_requests
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = executor.map(say_hello_to, url_list)
    return results


num_requests = 100
url = "http://127.0.0.1:9990/ner"
num_threads = 100
results = test_performance(url, num_requests, num_threads)


# convert result to int
successes = 0
errors = 0
success_times = 0
error_times = 0
dists = []
for response_time, is_success in results:
    if is_success:
        successes += 1
        success_times += response_time
    else:
        errors += 1
        error_times += response_time
    dists.append(int(response_time))

print(f"Total requests: {num_requests}")
print(f"Concurrency: {num_threads}")
print(f"Average Request Time: {(success_times + error_times) / num_requests} sec/request")
print(f"Throughput: {successes / (success_times or 1):.2f} requests/sec")
print(f"Error rate: {errors / num_requests} %")
print(f"Request_time distribution (sec, count): {sorted(Counter(dists).items())}")
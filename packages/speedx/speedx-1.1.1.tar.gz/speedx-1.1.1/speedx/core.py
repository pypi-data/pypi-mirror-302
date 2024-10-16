# speedx/core.py

import speedtest
import socket
import time

def run_speed_test():
    retries = 3
    for attempt in range(retries):
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            upload_speed = st.upload() / 1_000_000      # Convert to Mbps
            ping = st.results.ping

            server = st.get_best_server()
            server_info = {
                'host': server['host'],
                'name': server['name'],
                'country': server['country']
            }

            ip_address = socket.gethostbyname(socket.gethostname())

            return {
                'download_speed': round(download_speed, 2),
                'upload_speed': round(upload_speed, 2),
                'ping': ping,
                'server': server_info,
                'ip_address': ip_address
            }
        except speedtest.ConfigRetrievalError as e:
            print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            time.sleep(2)  # Wait a bit before retrying
    raise Exception("Failed to retrieve speed test configuration after several retries.")

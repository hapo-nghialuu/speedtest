import speedtest
import requests
import json
from datetime import datetime
import pytz
from time import sleep
from dotenv import load_dotenv
import os
from pprint import pprint  # Thêm vào đây

# Tải biến môi trường từ .env file
load_dotenv()
webhook_url = os.getenv('SLACK_WEBHOOK_URL')

# Hàm gửi thông điệp qua Slack
def send_message_to_slack(message):
    data = {'text': message}
    response = requests.post(webhook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        raise ValueError(
            f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}")

# Hàm đo tốc độ mạng và tạo thông điệp


def measure_speed():
    timezone = pytz.timezone(os.getenv('TIMEZONE'))
    current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download()
    upload_speed = st.upload()
    ping = st.results.ping
    client_ip = st.results.client['ip']

    message = {
        "Thời điểm test": current_time,
        "IP": client_ip,
        "Tốc độ Download": f"{download_speed / 10**6:.2f} Mbps",
        "Tốc độ Upload": f"{upload_speed / 10**6:.2f} Mbps",
        "Ping": f"{ping} ms"
    }

    return message

if __name__ == "__main__":
    start_time = datetime.now()
    while (datetime.now() - start_time).seconds < 60: # Lặp trong 10 giây
        message = measure_speed()
        pprint(message)  # Sử dụng pprint để in thông điệp
        print(message)  # Sử dụng pprint để in thông điệp

        # send_message_to_slack("\n".join([f"{key}: {value}" for key, value in message.items()]))

        sleep(10)  # Nghỉ 1 giây trước khi đo lại

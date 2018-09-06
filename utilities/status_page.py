import urllib.parse as urllib

import requests
import time
from threading import Timer


class StatusPage:
    def __init__(self, config, client):
        self.total_points = (60 / 5 * 24)
        self.config = config
        self.api_base = 'https://api.statuspage.io'
        self.client = client

    def init(self):
        if self.client.is_in_debug_mode():
            return
        headers = {"Content-Type": "application/x-www-form-urlencoded",
                   "Authorization": "OAuth " + self.config["statuspage"]["api_key"]}
        value = int(self.client.latency * 1000)
        params = urllib.urlencode({'data[timestamp]': time.time(), 'data[value]': value})
        requests.post(f'{self.api_base}/v1/pages/{self.config["statuspage"]["page_id"]}/metrics/'
                      f'{self.config["statuspage"]["metric_id"]}'
                      f'/data.json', headers=headers, data=params)
        Timer(60.0, self.init).start()

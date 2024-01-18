import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 1000,
  duration: '30s',
};

export default function () {
  const url = 'https://group3-container.graycoast-fbecffe8.francecentral.azurecontainerapps.io/predict';

  const payload = { "features": [5.1, 3.5, 1.4, 0.2] }

  const headers = {
    'Content-Type': 'application/json'
  };

  const response = http.post(url, JSON.stringify(payload), { headers: headers });

  sleep(1);
}
import os
import requests
import argparse
from dotenv import load_dotenv
load_dotenv()

def get_bitlink(TOKEN, user_url):
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': 'Bearer {}'.format(TOKEN),
    }
    payload = {
        "long_url": user_url,
    }   
    response = requests.post(bitly_url, json=payload, headers=headers)
    if response.ok:
        response_data = response.json()
        return response_data['id']

def count_total_clicks(TOKEN, user_url):
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'.format(user_url)
    headers = {
        'Authorization': 'Bearer {}'.format(TOKEN),
    }
    payload = {
        'unit': 'day',
        'units': '-1', 
    }
    response = requests.get(bitly_url, params=payload, headers=headers)
    if response.ok:
        response_data = response.json()
        return response_data['total_clicks']

if __name__ == '__main__':
    
    TOKEN = os.getenv('TOKEN')
    parser = argparse.ArgumentParser(
    description='Ссылки и их аналитика сервиса bitly.com'
    )
    parser.add_argument('user_url', 
                        help='Адрес сайта или битлинк юзера')
    args = parser.parse_args()    
    user_url = args.user_url

    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'.format(user_url)
    headers = {
        'Authorization': 'Bearer {}'.format(TOKEN),
    }
    response = requests.get(bitly_url, headers=headers)
    if response.ok:
        total_clicks = count_total_clicks(TOKEN, user_url)
        print('Total clicks:', total_clicks)
    else:
        bitlink = get_bitlink(TOKEN, user_url)
        if bitlink is None:
            print('Wrong url')
        else:
            print('Bitlink:', bitlink)

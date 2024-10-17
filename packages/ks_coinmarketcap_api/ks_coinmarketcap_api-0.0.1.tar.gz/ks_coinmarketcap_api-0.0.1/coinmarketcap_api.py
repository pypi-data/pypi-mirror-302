import json
from json import JSONDecodeError
from binance.api import API
import logging
import requests
import multitasking
from time import sleep
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import traceback
from base_td.logger import LoggerBase

from binance.error import ClientError, ServerError

from .constant import RetCode, APPLE_COUNTRIES, DATE_FMT

class KsCoinmarketcapAPI(API, LoggerBase):
    """API base class

    Keyword Args:
        base_url (str, optional): the API base url, useful to switch to testnet, etc. By default it's https://api.binance.com
        timeout (int, optional): the time waiting for server response, number of seconds. https://docs.python-requests.org/en/master/user/advanced/#timeouts
        proxies (obj, optional): Dictionary mapping protocol to the URL of the proxy. e.g. {'https': 'http://1.2.3.4:8080'}
        show_limit_usage (bool, optional): whether return limit usage(requests and/or orders). By default, it's False
        show_header (bool, optional): whether return the whole response header. By default, it's False
        private_key (str, optional): RSA private key for RSA authentication
        private_key_pass(str, optional): Password for PSA private key
    """
    
    running: bool = True
    refresh_token: str = ''
    expires_in: int = 0
    

    def __init__(
        self,
        api_key=None,
        api_secret=None,
        access_token=None,
        base_url='https://pro-api.coinmarketcap.com/v1',
        timeout=None,
        proxies=None,
        show_limit_usage=False,
        show_header=False,
        private_key=None,
        private_key_pass=None,
        client_id=None,
        client_secret=None
    ):
        API.__init__(
            self,
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            timeout=timeout,
            proxies=proxies,
            show_limit_usage=show_limit_usage,
            show_header=show_header,
            private_key=private_key,
            private_key_pass=private_key_pass,
        )
        LoggerBase.__init__(self)

        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.base_url = base_url
        self.timeout = timeout
        self.proxies = None
        self.show_limit_usage = False
        self.show_header = False
        self.private_key = private_key
        self.private_key_pass = private_key_pass
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json;charset=utf-8",
                "X-CMC_PRO_API_KEY": access_token
            }
        )

        if show_limit_usage is True:
            self.show_limit_usage = True

        if show_header is True:
            self.show_header = True

        if type(proxies) is dict:
            self.proxies = proxies

        self._logger = logging.getLogger(__name__)
    
    def _handle_exception(self, response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)['error']
            except JSONDecodeError:
                raise ClientError(
                    status_code, None, response.text, None, response.headers
                )
            error_data = err
            if "status" in err:
                error_data = err["status"]['error_message']
            raise ClientError(
                status_code, err["status"]['error_code'], error_data, response.headers, error_data
            )
        raise ServerError(status_code, response.text)
            

    def listings_latest(self, start: str = 1, limit: str = 5000, sort: str = 'volume_24h', convert: str = 'USDT', sort_dir: str = 'desc', cryptocurrency_type: str = 'all'):
        url_path = f'/cryptocurrency/listings/latest'
        return self.send_request('GET', url_path, {
            'start': start,
            'limit': limit,
            'sort': sort,
            'convert': convert,
            'sort_dir': sort_dir,
            'cryptocurrency_type': cryptocurrency_type
        })
    
    def quotes_latest(self, symbol: str, convert: str = None):
        url_path = f'/cryptocurrency/quotes/latest'
        params = {
            'symbol': symbol
        }
        if convert:
            params['convert'] = convert
        return self.send_request('GET', url_path, params)
    
    # 批量获取，由于ranks单次只能获取1一个月
    def ranks_bulk(self, product_ids: str, granularity: str, start_date: str, end_date: str, countries: str = APPLE_COUNTRIES, filter: int = 1000, tz: str = 'user', format: str = 'json'):
        start = parse(start_date)
        end = parse(end_date)

        all_ranks = {'dates': [], 'data': []}

        devices = ['desktop', 'handheld', 'tablet']
        names = ['Finance', 'Top Apps', 'Top Grossing', 'Top Overall']
        subtypes = ['free', 'paid', 'topgrossing']
        product_ids_list = [int(x) for x in product_ids.split(',')]
        countries_list = countries.split(',')
        for product_id in product_ids_list:
            for country in countries_list:
                for device in devices:
                    for category_name in names:
                        for sub_type in subtypes:
                            all_ranks['data'].append({
                                "country": country,
                                "category": {
                                    "store": "apple",
                                    "device": device,
                                    "name": category_name,
                                    "subtype": sub_type,
                                },
                                "product_id": product_id,
                                "positions": [
                                ],
                                "deltas": [
                                ]
                            })
        
        current = start
        while current <= end:
            following = current + relativedelta(months=1)
            self.log(f'fetching {current}~{following}...')
            ret_code, ranks = self.ranks(
                product_ids = product_ids,
                granularity = granularity, 
                start_date = current.strftime(DATE_FMT),
                end_date = following.strftime(DATE_FMT),
                countries = countries,
                filter = filter,
                tz = tz,
                format = format
            )
            if ret_code == RetCode.ERROR:
                return RetCode.ERROR, ranks
            if ret_code == RetCode.OK:
                all_ranks = _concat_ranks(all_ranks, ranks)
            current = following
        self.log(f'fetching done.')
        return RetCode.OK, all_ranks

def _concat_ranks(all_ranks, ranks):
    all_ranks['dates'] = all_ranks['dates'][:-1] + ranks['dates']
    for item in all_ranks['data']:
        country = item['country']
        product_id = item['product_id']
        store = item['category']['store']
        device = item['category']['device']
        name = item['category']['name']
        subtype = item['category']['subtype']

        target = next(iter([x for x in ranks['data'] if x['country'] == country and x['product_id'] == product_id and x['category']['store'] == store and x['category']['device'] == device and x['category']['name'] == name and x['category']['subtype'] == subtype]), None)
        if target:
            item['positions'] = item['positions'][:-1] + target['positions']
            item['deltas'] = item['deltas'][:-1] + target['deltas']
        else:
            # 不存在数据，要插入空数据
            insert_nums = (len(ranks['dates'])-1) if len(item['positions']) > 1 else len(ranks['dates'])
            item['positions'] = item['positions'] + [None] * insert_nums
            item['deltas'] = item['deltas'] + [None] * insert_nums
    return all_ranks
from jav.web.base import Request, resp2html
from jav.web.base import Request, read_proxy, resp2html
from jav.web.exceptions import *
from jav.web.proxyfree import get_proxy_free_url
from jav.config import Cfg, CrawlerID

def init_network_cfg():
    """设置合适的代理模式和base_url"""
    request.timeout = 5
    proxy_free_url = get_proxy_free_url('javlib')
    urls = [str(Cfg().network.proxy_free[CrawlerID.javlib]), permanent_url]
    if proxy_free_url and proxy_free_url not in urls:
        urls.insert(1, proxy_free_url)
    # 使用代理容易触发IUAM保护，先尝试不使用代理访问
    proxy_cfgs = [{}, read_proxy()] if Cfg().network.proxy_server else [{}]
    for proxies in proxy_cfgs:
        request.proxies = proxies
        for url in urls:
            if proxies == {} and url == permanent_url:
                continue
            try:
                resp = request.get(url, delay_raise=True)
                if resp.status_code == 200:
                    request.timeout = Cfg().network.timeout.seconds
                    return url
            except Exception as e:
                logger.debug(f"Fail to connect to '{url}': {e}")
    logger.warning('无法绕开JavLib的反爬机制')
    request.timeout = Cfg().network.timeout.seconds
    return permanent_url

url = 'https://www.javlibrary.com/cn/vl_searchbyid.php?keyword=dass-425'
request = Request(use_scraper=True)
response = request.get(url)
result = resp2html(response)
print(result)
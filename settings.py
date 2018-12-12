"""
    存储项目所需要的路径
"""

from os.path import join
import os

def init_dir(dir_path):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

dir_data_path = join("data")
dir_loc_path = join("loc")
init_dir(dir_data_path)
init_dir(dir_loc_path)
dir_raw_path = join("raw")


# dir_google_path = join(dir_loc_path, "google_info")

xlsx_country2language_path = join("raw", "country_languange_dict.xlsx")
xlsx_wangfang_path = join("raw", "万方放射学者20181210-new.xlsx")

pkl_affi_wangfang_path = join(dir_data_path, "affi_wangfang.pkl")   # affi of wangfang
dict_country2language_path = join("data", "country_languange_dict.json")

result_dict_wangfang_path = join("data", "result_wangfang.json")


"""
    获取合适的代理
"""

p = {
    "proxyHost": "proxy.crawlera.com",
    "proxyPort": "8010",
    "proxyAuth": ":"
}

proxy_auth = p['proxyAuth']
proxy_host = p['proxyHost']
proxy_port = p['proxyPort']


def get_proxy(isHome=True):
    proxy_a = {"https": "https://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),
            "http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port)}
    proxy_b =  {'http': 'socks5://127.0.0.1', 'https': 'socks5://127.0.0.1'}

    return proxy_b if isHome else proxy_a

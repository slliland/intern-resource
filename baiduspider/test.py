from pprint import pprint
from baiduspider import BaiduSpider

result = BaiduSpider().search_web('Python')
print(result)  # print
print('\n\n')
pprint(result)  # pprint
import requests

item_sold = {}
item_profit = {}

file1 = open('type_ids.txt', 'r')
items = {}
for i in file1.readlines():
    items[i.split('|')[0]] = i.split('|')[1].split()


for type_id in items.keys():
    url = f'https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=sell&page=1&type_id={type_id}'
    page = requests.get(url).json()
    print(type_id, ' ', items[type_id])
    
    if page is None or len(page) == 0:
        continue
    
    for i in range(len(page)):
        for j in range(len(page) - 1):
            if page[j].get('price') > page[j + 1].get('price'):
                page[j], page[j + 1] = page[j + 1], page[j]

    sold_volume = 0
    last = page[0].get('price')
    total_price = page[0].get('price') * page[0].get('volume_remain')
    sold_volume = 0
    max_ratio = -1000
    flag = False
    sold_price = 0
    
    for i in page:
        sold_volume += (i.get('volume_total') - i.get('volume_remain'))

    for i in range(1, len(page)):
        if total_price >= 30000000:
            break
            
        ratio = page[i].get('price') / last
        
        if ratio > max_ratio:
            max_ratio = ratio
            
        if ratio >= 1.6:
            item_profit[type_id] = total_price * (ratio - 1) * 0.9372
            item_sold[type_id] = sold_volume
            sold_price = page[i].get('price')
            flag = True
    
        total_price += page[i].get('price') * page[i].get('volume_remain')
        last = page[i].get('price')

    print('------ ', max_ratio, ' ', sold_volume)
    if flag:
        f = open('items.txt', 'a')
        f.write(f'{items[type_id]} | item profit: {int(item_profit[type_id])} | items sold: {item_sold[type_id]} | sell price: {sold_price}')
        f.write('\n')
        f.close()

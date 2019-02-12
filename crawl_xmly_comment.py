def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 \
            QQBrowser/10.3.2727.400'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    users = [a.find(class_='orange-1').get_text() for a in soup.find_all(class_='comment-head')]  # find第一个用户名为
    time = [i.get_text() for i in soup.find_all(class_='comment-time')]
    comments = [emoji.demojize(i.get_text()) for i in soup.find_all(class_='comment-body')]
    #upvotes = [i.string for i in soup.find_all(i)]
    return users, time, comments

def write_2_file(html):
    users, time, comments = parse_one_page(html)
    with open('comments.csv', 'a') as f:
        for i in range(len(users)):
            #print(u, t ,c)
            f.write(f'{users[i]},')
            f.write(f'{time[i]},')
            try:
                f.write(f'{comments[i]}\n')
            except:
                continue
        
def main(page):
    url = 'https://www.ximalaya.com/renwen/7651313/54212132/p'+str(page)
    write_2_file(get_one_page(url))
    
if __name__ == '__main__':
    with open('comments.csv', 'a') as f:
        f.write('评论人, 评论时间, 评论内容\n')
    
    print('Crawling Start...')
    for i in range(1, 35):
            main(page=i)
            if i % 5 == 0:
                print(f'{i} pages have been crawled...')
            time.sleep(1)
    print('Crawling Complete')
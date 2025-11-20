# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def collect_with_selenium(url, max_pages=60):
    print("使用Selenium启动浏览器...")

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except:
        print("Chrome驱动安装失败，尝试使用Edge...")
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=chrome_options)

    all_data = []

    try:
        for page in range(max_pages):
            start = page * 20
            if page == 0:
                page_url = f"{url}comments"
            else:
                page_url = f"{url}comments?start={start}"

            print(f"正在爬取第{page+1}页...")
            driver.get(page_url)
            time.sleep(3)

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            comments = soup.find_all('div', class_='comment-item')

            print(f"  找到{len(comments)}条评论")

            if not comments:
                break

            for comment in comments:
                try:
                    username = comment.find('span', class_='comment-info').find('a').text.strip()
                    time_elem = comment.find('span', class_='comment-time')
                    comment_time = time_elem['title'] if time_elem else ''
                    content = comment.find('span', class_='short').text.strip()

                    all_data.append({
                        '用户名': username,
                        '评论时间': comment_time,
                        '评论内容': content
                    })
                except:
                    continue

            print(f"  当前共{len(all_data)}条")
            time.sleep(2)

    finally:
        driver.quit()
        print("浏览器已关闭")

    return all_data

def collect_douban_comments(url, max_pages=60):
    cookies = {
        'bid': 'XjEg__EjyZY',
        'dbcl2': '292199783:35Q7IZXbvp8',
        '__utma': '30149280.1536989496.1762061639.1762061639.1762669908.2',
        '__utmb': '30149280.6.10.1762669908',
        '__utmc': '30149280',
        '__utmz': '30149280.1762061639.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
        '__utmv': '30149280.29219',
        'ck': 'stN8'
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://movie.douban.com/',
        'Upgrade-Insecure-Requests': '1'
    }

    all_data = []

    try:
        for page in range(max_pages):
            start = page * 20
            if page == 0:
                page_url = f"{url}comments"
            else:
                page_url = f"{url}comments?start={start}"

            retry_count = 0
            max_retries = 3
            success = False

            while retry_count < max_retries and not success:
                try:
                    response = requests.get(page_url, headers=headers, cookies=cookies, timeout=15)
                    if response.status_code == 200:
                        success = True
                    elif response.status_code == 403:
                        print(f"第{page+1}页被拒绝访问，等待后重试...")
                        time.sleep(5)
                        retry_count += 1
                    else:
                        print(f"获取第{page+1}页失败，状态码{response.status_code}")
                        retry_count += 1
                        time.sleep(2)
                except Exception as e:
                    print(f"请求出错: {str(e)}，重试中...")
                    retry_count += 1
                    time.sleep(3)

            if not success:
                print(f"第{page+1}页多次重试失败，停止爬取")
                break

            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            comments = soup.find_all('div', class_='comment-item')

            if not comments:
                print(f"未获取到评论，页面标题: {soup.title.string if soup.title else '无标题'}")
                print(f"状态码: {response.status_code}, URL: {page_url}")
                break

            for comment in comments:
                try:
                    username = comment.find('span', class_='comment-info').find('a').text.strip()
                    time_elem = comment.find('span', class_='comment-time')
                    comment_time = time_elem['title'] if time_elem else ''
                    content = comment.find('span', class_='short').text.strip()

                    all_data.append({
                        '用户名': username,
                        '评论时间': comment_time,
                        '评论内容': content
                    })
                except:
                    continue

            print(f"已爬取第{page+1}页，当前共{len(all_data)}条")

            if (page + 1) % 10 == 0:
                print("已爬取10页，休息5秒...")
                time.sleep(5)
            else:
                time.sleep(random.uniform(1, 2))

    except Exception as e:
        print(f"爬取出错: {str(e)}")

    return all_data

def create_sample_data():
    import datetime

    positive_templates = [
        '哪吒这部电影真的太好看了特效很棒剧情也很感人',
        '我命由我不由天这句台词太燃了',
        '国漫之光支持国产动画',
        '特效做得很用心场面震撼值得二刷',
        '敖丙和哪吒的友情让人感动剧情反转很精彩',
        '哪吒的成长历程很励志给了我很多启发',
        '画面精美每一帧都是壁纸制作水准很高',
        '剧情紧凑不拖沓前后呼应做得好',
        '这部电影让我重新认识了国漫太惊艳了',
        '导演很有才华期待后续作品',
        '票房破40亿实至名归国漫崛起',
        '打斗场面设计得很精彩节奏把握得好',
        '电影音乐也很好听很有感染力',
        '配音演员表现很棒尤其是太乙真人笑死我了',
        '李靖的父爱表现得很细腻让我泪目',
        '哪吒的人物塑造非常成功有血有肉',
        '故事改编得很好不是传统的哪吒形象孩子很喜欢',
        '电影传递的价值观很正适合全家观看',
        '特效水准达到了国际水平团队很用心',
        '申公豹的角色也很有趣口吃设定太好笑了',
        '看完电影很震撼国漫真的在进步',
        '哪吒和敖丙的对手戏很精彩演得很好',
        '第二次看又发现了很多细节值得多刷',
        '带学生们一起看的很有教育意义',
        '强烈推荐给身边所有人必看的国漫',
        '剧情设计很巧妙每个角色都很立体',
        '视觉效果一流观影体验非常好',
        '哪吒形象虽丑但很可爱有个性',
        '故事内核很深刻不只是娱乐片',
        '动作戏份设计精彩打斗很流畅',
        '看了三遍还是觉得很精彩',
        '国产动画的里程碑之作',
        '每个角色都刻画得很饱满',
        '笑点和泪点都把握得很好',
        '整体制作水平非常高',
        '配乐恰到好处烘托气氛',
        '故事节奏掌控得很棒',
        '人物关系处理得很细腻',
        '视听效果震撼人心',
        '主题立意深刻引人思考',
        '细节处理很到位',
        '角色设定新颖独特',
        '剧本扎实逻辑清晰',
        '动画制作精良流畅',
        '情感表达真挚动人',
        '想象力丰富创意十足',
        '完成度很高瑕不掩瑜',
        '娱乐性和艺术性兼顾',
        '老少皆宜合家欢影片',
        '超出预期的优秀作品',
    ]

    neutral_templates = [
        '电影还可以吧有些地方不错',
        '整体来说中规中矩没有特别惊艳',
        '剧情有点简单但画面还行',
        '适合带小孩子看的动画片',
        '特效不错但故事一般般',
        '看完感觉还好没有想象中那么好',
        '画面制作用心了剧情有待提高',
        '作为国产动画已经不错了',
        '有笑点也有泪点中等水平',
        '孩子很喜欢大人觉得还行',
        '没有宣传的那么好但也不差',
        '中规中矩的商业动画',
        '有优点也有缺点比较平衡',
        '可以看但不必吹得太高',
        '制作水平尚可剧情中等',
        '娱乐性还可以深度不够',
        '适合家庭观看的爆米花电影',
        '符合预期没有太大惊喜',
        '作为消遣还是不错的',
        '整体及格线以上的作品',
    ]

    negative_templates = [
        '剧情有点拖沓节奏不太好',
        '有些笑点太刻意了不太自然',
        '期待值太高了实际感觉一般',
        '故事改编得不太满意',
        '有些地方逻辑不太通顺',
        '觉得宣传有点过度了',
        '人物设定有些单薄',
        '部分情节处理比较仓促',
        '配乐有点吵影响观影',
        '笑点比较低俗不太喜欢',
        '剧情缺乏新意比较套路',
        '角色太脸谱化不够真实',
        '有些台词很尴尬',
        '节奏把握不太好',
        '结局处理得不够满意',
    ]

    usernames = [
        '电影爱好者', '国漫支持者', '动画迷', '观众A', '路人甲', '影评人', '学生党',
        '家长', '配音粉', '普通观众', '动作片迷', '励志青年', '音乐爱好者', '导演粉',
        '票房观察员', '角色粉', '父母', '喜剧迷', '国漫新粉', '视觉控', '二刷观众',
        '剧情党', '泪点低', '特效师', '老师', '哪吒粉', '敖丙粉', '三刷观众', '周边收集者',
        '推荐达人', '电影评论家', '资深影迷', '动漫达人', '观影达人', '文艺青年',
        '95后观众', '00后学生', '宝妈', '奶爸', '上班族', '大学生', '中学生',
        '影院常客', '国漫粉丝', '特效爱好者', '配乐粉', '声优粉', '导演研究者'
    ]

    sample_comments = []
    start_date = datetime.datetime(2019, 7, 13, 10, 0, 0)

    suffixes = ['', '', '', '真的不错', '值得推荐', '必看', '超赞', '给力', '棒棒的',
                 '非常喜欢', '太赞了', '很满意', '还不错', '挺好的', '推荐观看',
                 '不虚此行', '物超所值', '印象深刻', '回味无穷', '意犹未尽',
                 '赞一个', '很感动', '很震撼', '不错不错', '点赞', '支持',
                 '佩服', '厉害', '精彩', '完美', '优秀', '杰出', '卓越']

    for i in range(1200):
        comment_date = start_date + datetime.timedelta(
            days=random.randint(0, 60),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )

        rand = random.random()
        if rand < 0.75:
            content = random.choice(positive_templates)
        elif rand < 0.9:
            content = random.choice(neutral_templates)
        else:
            content = random.choice(negative_templates)

        if random.random() > 0.3:
            content = content + random.choice(suffixes)

        sample_comments.append({
            '用户名': f"{random.choice(usernames)}{random.randint(1, 999)}",
            '评论时间': comment_date.strftime('%Y-%m-%d %H:%M:%S'),
            '评论内容': content
        })

    return sample_comments

def save_to_csv(data, filename='raw_data.csv'):
    if not os.path.exists('data'):
        os.makedirs('data')

    filepath = os.path.join('data', filename)
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"数据已保存到 {filepath}")
    return filepath

def simple_crawl(max_pages=50):
    print("开始简单爬取...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Cookie': 'bid=XjEg__EjyZY; dbcl2="292199783:35Q7IZXbvp8"; ck=stN8'
    }

    all_data = []

    for page in range(max_pages):
        url = f'https://movie.douban.com/subject/34780991/comments?start={page*20}&limit=20&status=P&sort=new_score'

        print(f'爬取第{page+1}页...')

        try:
            r = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(r.content, 'html.parser')
            comments = soup.find_all('div', class_='comment-item')

            if not comments:
                print(f'  未找到评论，停止')
                break

            for c in comments:
                try:
                    user = c.find('span', class_='comment-info').find('a').text.strip()
                    time_elem = c.find('span', class_='comment-time')
                    ctime = time_elem.get('title', '') if time_elem else ''
                    content = c.find('span', class_='short').text.strip()
                    all_data.append({'用户名': user, '评论时间': ctime, '评论内容': content})
                except:
                    pass

            print(f'  获取{len(comments)}条，总计{len(all_data)}条')
            time.sleep(1)

        except Exception as e:
            print(f'  出错: {e}')
            break

    return all_data

def main():
    print("开始采集哪吒电影评论数据...")

    data = simple_crawl(50)

    if data:
        print(f"共采集到 {len(data)} 条评论")
        save_to_csv(data)
        print("数据采集完成")
    else:
        print("未能采集到数据")

if __name__ == '__main__':
    main()

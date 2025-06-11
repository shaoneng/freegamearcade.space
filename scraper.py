# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import os
import time

# --- 配置 ---
BASE_URL = "https://www.onlinegames.io/"
GAMES_TO_SCRAPE_PER_DAY = 4
# 修改文件路径，使其保存在freegamearcade.space文件夹中
PROCESSED_GAMES_FILE = os.path.join(os.path.dirname(__file__), 'processed_games.txt')
GAMES_ARCHIVE_FILE = os.path.join(os.path.dirname(__file__), 'games_archive.json')

def load_json_file(filename):
    """安全地加载JSON文件。"""
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_processed_urls():
    """从文件中读取已处理的游戏URL。"""
    if not os.path.exists(PROCESSED_GAMES_FILE):
        return set()
    with open(PROCESSED_GAMES_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

def scrape_new_games():
    """主抓取函数，抓取新游戏并深入页面获取iframe链接和描述。"""
    print("开始抓取新游戏...")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(BASE_URL, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"错误: 无法访问主网站: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    game_elements = soup.select('article.c-card')

    if not game_elements:
        print("警告: 未找到任何游戏元素。请检查选择器 'article.c-card' 是否仍然有效。")
        return

    processed_urls = get_processed_urls()
    all_games = load_json_file(GAMES_ARCHIVE_FILE)
    new_games_found = []

    for game_elem in game_elements:
        if len(new_games_found) >= GAMES_TO_SCRAPE_PER_DAY:
            break

        link_tag = game_elem.select_one('.c-card__title a')
        if not link_tag:
            continue
            
        game_url = link_tag.get('href')
        if not game_url or game_url in processed_urls:
            continue

        game_title = link_tag.get_text(strip=True)
        print(f"发现新游戏: {game_title}")

        # --- 更新逻辑: 访问游戏详情页，抓取iframe链接和描述 ---
        iframe_url = ""
        description_text = ""
        short_description_text = ""
        try:
            print(f"  -> 正在访问详情页: {game_url}")
            game_page_response = requests.get(game_url, headers=headers, timeout=10)
            game_page_response.raise_for_status()
            game_soup = BeautifulSoup(game_page_response.text, 'html.parser')
            
            # 抓取Iframe
            iframe_tag = game_soup.select_one('iframe#gameFrame, iframe[src*="cloud.onlinegames.io"]')
            if iframe_tag and iframe_tag.get('src'):
                iframe_url = iframe_tag['src']
                if iframe_url.startswith('//'): iframe_url = 'https:' + iframe_url
                print(f"  -> 成功找到 iframe 链接")
            else:
                iframe_url = game_url # 后备链接
                print(f"  -> 警告: 未找到 iframe 链接")

            # 抓取详细描述 (for AI)
            description_tag = game_soup.select_one('div.post__entry')
            if description_tag:
                paragraphs = description_tag.find_all('p')
                description_text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                print(f"  -> 成功抓取详细描述文本")
            else:
                 print(f"  -> 警告: 未找到详细描述文本")

            # 抓取简短描述 (for homepage)
            short_desc_tag = game_soup.select_one('meta[name="description"]')
            if short_desc_tag and short_desc_tag.get('content'):
                short_description_text = short_desc_tag.get('content')
                print(f"  -> 成功抓取首页简介")
            else:
                print(f"  -> 警告: 未找到首页简介")

        except requests.RequestException as e:
            print(f"  -> 错误: 无法访问游戏详情页 {game_url}: {e}")
            iframe_url = game_url

        img_tag = game_elem.select_one('.c-card__image img')
        thumbnail_url = img_tag.get('src') if img_tag else ''

        safe_name = "".join(c for c in game_title if c.isalnum()).lower() or str(int(time.time()))

        game_data = {
            "id": safe_name,
            "title": game_title,
            "url": game_url,
            "iframe_url": iframe_url,
            "thumbnail": thumbnail_url,
            "description": description_text, 
            "short_description": short_description_text, # 新增字段
            "page_filename": f"{safe_name}.html"
        }
        new_games_found.append(game_data)
        
    if new_games_found:
        all_games.extend(new_games_found)
        with open(GAMES_ARCHIVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_games, f, ensure_ascii=False, indent=4)
        with open(PROCESSED_GAMES_FILE, 'a', encoding='utf-8') as f:
            for game in new_games_found:
                f.write(game['url'] + '\n')
        print(f"\n成功添加 {len(new_games_found)} 个新游戏到存档。")
    else:
        print("\n本次运行未发现新游戏。")

if __name__ == '__main__':
    scrape_new_games()

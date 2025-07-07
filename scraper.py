# scraper.py
import requests
from bs4 import BeautifulSoup
import json
import os
import time
from PIL import Image # 导入Pillow库 (Import Pillow library)
import io # 导入io库 (Import io library)

# --- 配置 (Configuration) ---
BASE_URL = "https://www.onlinegames.io/"
# --- 恢复每日抓取数量限制 (Restore daily scraping limit) ---
GAMES_TO_SCRAPE_PER_DAY = 4
# 获取当前脚本所在目录 (Get the directory of the current script)
CURRENT_DIR = os.path.dirname(__file__)
PROCESSED_GAMES_FILE = os.path.join(CURRENT_DIR, 'processed_games.txt')
GAMES_ARCHIVE_FILE = os.path.join(CURRENT_DIR, 'games_archive.json')
# 新增：图片存储目录 (New: Image storage directory)
IMAGE_DIR = os.path.join(CURRENT_DIR, 'assets', 'images')

def load_json_file(filename):
    """安全地加载JSON文件。 (Safely load a JSON file.)"""
    if not os.path.exists(filename) or os.path.getsize(filename) == 0:
        return []
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_processed_urls():
    """从文件中读取已处理的游戏URL。 (Read processed game URLs from a file.)"""
    if not os.path.exists(PROCESSED_GAMES_FILE):
        return set()
    with open(PROCESSED_GAMES_FILE, 'r', encoding='utf-8') as f:
        return set(line.strip() for line in f)

# 新增：下载并转换图片的函数 (New: Function to download and convert images)
def download_and_convert_image(url, safe_name):
    """下载图片，转换为WebP格式，并返回本地相对路径。"""
    """Downloads an image, converts it to WebP format, and returns the local relative path."""
    if not url:
        return ""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, stream=True)
        response.raise_for_status()

        # 使用Pillow处理图片 (Process image using Pillow)
        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        
        # 定义WebP文件的保存路径 (Define the save path for the WebP file)
        webp_filename = f"{safe_name}.webp"
        webp_filepath = os.path.join(IMAGE_DIR, webp_filename)
        
        # 保存为WebP格式，质量为85 (Save as WebP format with quality 85)
        image.save(webp_filepath, 'WEBP', quality=85)
        
        print(f"  -> 图片成功保存为 (Image successfully saved as): {webp_filepath}")
        
        # 返回用于HTML的相对路径 (Return the relative path for HTML use)
        return f"assets/images/{webp_filename}"

    except requests.RequestException as e:
        print(f"  -> 错误: 下载图片失败 (Error: Failed to download image) {url}: {e}")
        return url # 下载失败则返回原URL (Return original URL on download failure)
    except Exception as e:
        print(f"  -> 错误: 处理图片失败 (Error: Failed to process image) {url}: {e}")
        return url # 处理失败也返回原URL (Return original URL on processing failure)

def scrape_new_games():
    """主抓取函数，抓取新游戏，下载并转换图片。"""
    """Main scraping function to fetch new games, download, and convert images."""
    print(f"开始抓取新游戏 (每日上限: {GAMES_TO_SCRAPE_PER_DAY} 个)...")
    print(f"Starting to scrape new games (Daily limit: {GAMES_TO_SCRAPE_PER_DAY})...")
    
    # 确保图片目录存在 (Ensure the image directory exists)
    os.makedirs(IMAGE_DIR, exist_ok=True)
    print(f"图片将保存至 (Images will be saved to): {IMAGE_DIR}")
    
    processed_urls = get_processed_urls()
    all_games = load_json_file(GAMES_ARCHIVE_FILE)
    new_games_found = []
    
    page_number = 1
    # --- 带有数量限制的翻页逻辑 (Pagination logic with limit) ---
    while len(new_games_found) < GAMES_TO_SCRAPE_PER_DAY:
        if page_number == 1:
            url_to_scrape = BASE_URL
        else:
            url_to_scrape = f"{BASE_URL}page/{page_number}/"
        
        print(f"\n--- 正在抓取页面 (Scraping page): {url_to_scrape} ---")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url_to_scrape, headers=headers, timeout=15)
            if response.status_code == 404:
                print("页面未找到 (404)，已到达网站最后一页。 (Page not found (404), reached the last page.)")
                break
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"错误: 无法访问页面 (Error: Cannot access page) {url_to_scrape}: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        game_elements = soup.select('article.c-card')

        if not game_elements:
            print("当前页面未找到任何游戏元素，抓取结束。 (No game elements found on the current page, scraping finished.)")
            break
        
        # 遍历当前页面的游戏 (Iterate through games on the current page)
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
            print(f"发现新游戏 (New game found) ({len(new_games_found) + 1}/{GAMES_TO_SCRAPE_PER_DAY}): {game_title}")

            iframe_url = ""
            description_text = ""
            short_description_text = ""
            try:
                # ... (此处省略了抓取详情页的逻辑，与原版相同)
                # (Logic for scraping detail page is omitted here, same as original)
                game_page_response = requests.get(game_url, headers=headers, timeout=10)
                game_page_response.raise_for_status()
                game_soup = BeautifulSoup(game_page_response.text, 'html.parser')
                
                iframe_tag = game_soup.select_one('iframe#gameFrame, iframe[src*="cloud.onlinegames.io"]')
                if iframe_tag and iframe_tag.get('src'):
                    iframe_url = iframe_tag['src']
                    if iframe_url.startswith('//'): iframe_url = 'https:' + iframe_url
                else:
                    iframe_url = game_url

                description_tag = game_soup.select_one('div.post__entry')
                if description_tag:
                    paragraphs = description_tag.find_all('p')
                    description_text = "\n".join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                
                short_desc_tag = game_soup.select_one('meta[name="description"]')
                if short_desc_tag and short_desc_tag.get('content'):
                    short_description_text = short_desc_tag.get('content')

            except requests.RequestException as e:
                print(f"  -> 错误: 无法访问游戏详情页 (Error: Cannot access game detail page) {game_url}: {e}")
                iframe_url = game_url

            img_tag = game_elem.select_one('.c-card__image img')
            thumbnail_url = img_tag.get('src') if img_tag else ''
            safe_name = "".join(c for c in game_title if c.isalnum()).lower() or str(int(time.time()))

            # --- 图片处理新逻辑 (New image processing logic) ---
            print(f"  -> 正在处理图片 (Processing image): {thumbnail_url}")
            local_thumbnail_path = download_and_convert_image(thumbnail_url, safe_name)

            game_data = {
                "id": safe_name,
                "title": game_title,
                "url": game_url,
                "iframe_url": iframe_url,
                "thumbnail": local_thumbnail_path, # 使用本地路径 (Use local path)
                "description": description_text,
                "short_description": short_description_text,
                "page_filename": f"{safe_name}.html"
            }
            new_games_found.append(game_data)
        
        page_number += 1
        time.sleep(1)

    # --- 抓取循环结束后，统一保存 (Save uniformly after the scrape loop ends) ---
    if new_games_found:
        all_games.extend(new_games_found)
        with open(GAMES_ARCHIVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_games, f, ensure_ascii=False, indent=4)
        with open(PROCESSED_GAMES_FILE, 'a', encoding='utf-8') as f:
            for game in new_games_found:
                f.write(game['url'] + '\n')
        print(f"\n抓取完成！成功添加 {len(new_games_found)} 个新游戏到存档。")
        print(f"Scraping complete! Successfully added {len(new_games_found)} new games to the archive.")
    else:
        print("\n本次运行未发现任何新游戏。 (No new games found in this run.)")

if __name__ == '__main__':
    scrape_new_games()

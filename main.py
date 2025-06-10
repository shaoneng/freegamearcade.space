# main.py
import scraper
import page_generator

def main():
    print("--- 每日AI游戏内容生成任务启动 ---")
    scraper.scrape_new_games()
    page_generator.generate_pages()
    print("\n--- 任务完成 ---")

if __name__ == '__main__':
    main()
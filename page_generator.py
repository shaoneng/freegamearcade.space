# page_generator.py
import json
import os
import time
import google.generativeai as genai

# --- 配置 ---
GAMES_ARCHIVE_FILE = 'games_archive.json'
# --- 关键修改: 输出目录现在是 'game' ---
GAME_PAGE_DIR = 'game'  
SITE_BASE_URL = "https://shaoneng.github.io/freegamearcade.space" # 已为您更新

# --- Gemini API 调用函数 ---
def generate_game_page_with_gemini(game_data):
    """使用Gemini API为单个游戏生成完整的HTML页面。"""
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  -> 警告: 未设置 GEMINI_API_KEY 环境变量。无法生成页面。")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro-preview-06-05')
        
        # --- 关键修改: Canonical URL 现在指向 game/ 文件夹 ---
        page_url = f"{SITE_BASE_URL}/game/{game_data['page_filename']}"
        
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q47TS07D8C"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-Q47TS07D8C');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Play Kick the Pirate - Free Online Game | Free Game Arcade</title>
    <meta name="description" content="Play Kick the Pirate for free at Free Game Arcade. Turn this grumpy pirate into your personal punching bag, unlock wacky weapons, and blow off some steam! No download required, play directly in your browser.">
    <link rel="canonical" href="https://freegamearcade.space/game/kick-the-pirate.html">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'apple-bg': '#f5f5f7', 'apple-text': '#1d1d1f', 'apple-blue': '#007aff', 'apple-light-gray-text': '#6e6e73',
                    }
                },
                fontFamily: {
                    sans: ['-apple-system', 'BlinkMacSystemFont', "Segoe UI", 'Roboto', "Helvetica Neue", 'Arial', "Noto Sans", 'sans-serif', "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"],
                }
            }
        }
    </script>
    <style>
        html { height: 100%; } body { min-height: 100%; display: flex; flex-direction: column; } main { flex-grow: 1; } .aspect-16-9 { position: relative; width: 100%; padding-bottom: 56.25%; } .aspect-16-9 iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; }
    </style>
</head>
<body class="bg-apple-bg text-apple-text antialiased">
    <header class="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex-shrink-0"><a href="../index.html" class="text-2xl font-bold text-apple-blue">FGA</a></div>
                <nav class="hidden md:flex space-x-6">
                    <a href="#" class="text-gray-600 hover:text-apple-blue px-3 py-2 rounded-md text-sm font-medium">Action</a>
                    <a href="#" class="text-gray-600 hover:text-apple-blue px-3 py-2 rounded-md text-sm font-medium">Puzzle</a>
                    <a href="#" class="text-gray-600 hover:text-apple-blue px-3 py-2 rounded-md text-sm font-medium">Strategy</a>
                    <a href="#" class="text-gray-600 hover:text-apple-blue px-3 py-2 rounded-md text-sm font-medium">Sports</a>
                </nav>
            </div>
        </div>
    </header>
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <nav class="mb-6" aria-label="Breadcrumb"><ol class="flex items-center space-x-2 text-sm"><li><a href="../index.html" class="text-apple-light-gray-text hover:text-apple-blue">Home</a></li><li><span class="text-gray-400">/</span></li><li class="font-medium text-apple-text" aria-current="page">Pac-Xon New Realms</li></ol></nav>
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-apple-text mb-6 text-center">Kick the Pirate</h1>
        <section class="mb-10"><div id="game-embed-container" class="aspect-16-9 bg-black rounded-lg shadow-2xl overflow-hidden mx-auto max-w-4xl"><iframe id="game-iframe" src="https://cloud.onlinegames.io/games/2022/construct/92/kick-the-pirate/index-og.html" title="Kick the Pirate" class="border-0" allowfullscreen allow="fullscreen; accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" loading="lazy"></iframe></div></section>
        <section class="mb-10 bg-white p-6 sm:p-8 rounded-xl shadow-lg max-w-3xl mx-auto"><h2 class="text-2xl sm:text-3xl font-bold text-apple-text mb-4">How to Play Kick the Pirate</h2><div class="text-apple-light-gray-text space-y-3 leading-relaxed text-sm sm:text-base"><p>Ahoy matey!...</p></div></section>
    
    <!-- You Might Also Like Section -->
        {you_might_also_like_html}
    </main>
    
    <footer class="bg-gray-800 text-gray-300 py-12 mt-auto"><div class="container mx-auto px-4 sm:px-6 lg:px-8 text-center"><p class="text-sm">&copy; <span id="currentYear"></span> FreeGameArcade.space. All rights reserved.</p></div></footer>
    <script >
        /**
         * 网站功能脚本
         * 包含了移动端菜单切换、页脚年份更新以及游戏全屏功能。
        **/

    # 当整个HTML文档加载完成后执行
        // Mobile menu toggle
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        if (mobileMenuButton && mobileMenu) {{
            mobileMenuButton.addEventListener('click', () => {{
                mobileMenu.classList.toggle('hidden');
            }});
        }}

        // Set current year in footer
        const currentYearSpan = document.getElementById('currentYear');
        if (currentYearSpan) {{
            currentYearSpan.textContent = new Date().getFullYear();
        }}

        // Fullscreen functionality
        const fullscreenButton = document.getElementById('fullscreen-button');
        const gameIframe = document.getElementById('game-iframe'); // Target the iframe itself

        if (fullscreenButton && gameIframe) {{
            fullscreenButton.addEventListener('click', () => {{
                if (!document.fullscreenElement) {{
                    // Try to make the iframe fullscreen
                    if (gameIframe.requestFullscreen) {{
                        gameIframe.requestFullscreen().catch(err => console.error("Error attempting to enable full-screen mode:", err));
                    }} else if (gameIframe.mozRequestFullScreen) {{ /* Firefox */
                        gameIframe.mozRequestFullScreen();
                    }} else if (gameIframe.webkitRequestFullscreen) {{ /* Chrome, Safari & Opera */
                        gameIframe.webkitRequestFullscreen();
                    }} else if (gameIframe.msRequestFullscreen) {{ /* IE/Edge */
                        gameIframe.msRequestFullscreen();
                    }}
                }} else {{
                    if (document.exitFullscreen) {{
                        document.exitFullscreen().catch(err => console.error("Error attempting to disable full-screen mode:", err));
                    }}
                }}
            }});

            document.addEventListener('fullscreenchange', () => {{
                // Check if the iframe is the fullscreen element
                if (document.fullscreenElement === gameIframe) {{
                    fullscreenButton.textContent = '退出全屏'; // Exit Fullscreen in Chinese
                }} else {{
                    fullscreenButton.textContent = '进入全屏'; // Enter Fullscreen in Chinese
                }}
            }});
            
        }}
    </script>
</body>
</html>
"""

        prompt = f"""
        You are a ten-year full-stack engineer proficient in Google SEO, HTML, and Tailwind CSS.
        Your task is to populate the provided HTML template with the new game data to create a complete and unique HTML page.

        **New Game Data:**
        - Title: "{game_data['title']}"
        - Iframe URL: "{game_data['iframe_url']}"
        - Canonical URL: "{page_url}"
        - Description for context: "{game_data.get('description', 'A fun and exciting game.')}"

        **HTML Template to use:**
        ```html
        {html_template}
        ```

        **Instructions:**
        1.  Take the HTML template and replace the placeholder content (like "Kick the Pirate") with the new game data.
        2.  **SEO Title:** Create a new, compelling `<title>` tag in the format: "Play {game_data['title']} - Free Online Game | Free Game Arcade".
        3.  **Meta Description:** Write a new, engaging `<meta name="description">` based on the provided description context.
        4.  **Canonical URL:** Set the `<link rel="canonical">` href to the new Canonical URL.
        5.  **Content:** Update the breadcrumb, the `<h1>` title, the `<iframe>` src and title, the `<h2>` title, and write a new "How to Play" section in fluent English based on the description context.
        6.  **Output:** Provide only the final, complete, raw HTML code. Do not add any comments, explanations, or markdown formatting like ```html.
        """
        
        response = model.generate_content(prompt)
        generated_html = response.text.strip()
        if generated_html.startswith('```html'):
            generated_html = generated_html[7:]
        if generated_html.endswith('```'):
            generated_html = generated_html[:-3]
        
        print(f"  -> 成功为 '{game_data['title']}' 生成HTML页面。")
        return generated_html.strip()

    except Exception as e:
        print(f"  -> 错误:调用 Gemini API 时出错: {e}")
        return None

# 新增函数：生成"猜你喜欢"部分的HTML
def generate_you_might_also_like_section(current_game, all_games):
    """为当前游戏生成"猜你喜欢"部分，随机选择4个不同的游戏"""
    # 创建一个不包含当前游戏的游戏列表
    other_games = [game for game in all_games if game['id'] != current_game['id']]
    
    # 如果游戏数量不足4个，则使用所有可用的游戏
    num_games_to_show = min(4, len(other_games))
    
    # 随机选择游戏
    selected_games = random.sample(other_games, num_games_to_show)
    
    # 生成HTML
    game_cards_html = ""
    for game in selected_games:
        # 获取游戏缩略图，如果没有则使用占位图
        thumbnail = game.get('thumbnail', '')
        if not thumbnail:
            thumbnail = f"https://placehold.co/300x200/E2E8F0/1d1d1f?text={game['title'].replace(' ', '+')}" 
        
        # 获取游戏简短描述，如果没有则使用默认文本
        short_desc = game.get('short_description', f"Play {game['title']} online for free!")
        
        # 生成游戏卡片HTML
        game_cards_html += f"""
        <div class="bg-white rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
            <a href="/game/{game['page_filename']}">
                <img src="{thumbnail}" alt="{game['title']}" onerror="this.onerror=null;this.src='https://placehold.co/300x200/E2E8F0/1d1d1f?text=Game+Image';" class="w-full h-40 object-cover">
                <div class="p-4">
                    <h3 class="text-lg font-semibold text-apple-text mb-1 truncate" title="{game['title']}">{game['title']}</h3>
                    <p class="text-xs text-apple-light-gray-text h-10 overflow-hidden">{short_desc[:100]}...</p>
                </div>
            </a>
        </div>
        """
    
    # 完整的"猜你喜欢"部分HTML
    you_might_also_like_html = f"""
    <!-- You Might Also Like Section -->
    <section class="mb-10">
        <h2 class="text-2xl sm:text-3xl font-bold text-apple-text mb-8 text-center">You Might Also Like</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {game_cards_html}
        </div>
    </section>
    """
    
    return you_might_also_like_html

def generate_pages():
    """读取存档，调用AI为每个游戏生成完整的HTML页面。"""
    print("\n开始生成网页...")
    
    # --- 关键修改: 确保 'game' 文件夹存在 ---
    os.makedirs(GAME_PAGE_DIR, exist_ok=True)
    print(f"确保输出目录存在: {GAME_PAGE_DIR}")

    if not os.path.exists(GAMES_ARCHIVE_FILE):
        print(f"警告: 未找到 {GAMES_ARCHIVE_FILE} 文件。将只生成一个空的主页。")
        all_games = []
    else:
        with open(GAMES_ARCHIVE_FILE, 'r', encoding='utf-8') as f:
            all_games = json.load(f)

    for game in all_games:
        # --- 关键修改: 文件路径现在指向 'game/' 文件夹 ---
        filepath = os.path.join(GAME_PAGE_DIR, game['page_filename'])
        
        print(f"-> 正在为AI生成页面: {game['title']}")
        page_html = generate_game_page_with_gemini(game)
        
        if page_html:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page_html)
            print(f"  -> 成功创建页面: {filepath}")
        else:
            print(f"  -> 跳过页面生成，因为AI调用失败: {game['title']}")
        
        time.sleep(2) 

    generate_homepage(all_games)


def generate_homepage(games):
    """根据所有游戏数据生成主页。"""
    print("\n正在生成主页 index.html...")
    # 对游戏进行反向排序，以便最新的游戏显示在最前面
    games_for_homepage = sorted(games, key=lambda x: x.get('id'), reverse=True)

    # 生成所有游戏卡片
    all_game_cards_html = ""
    for game in games_for_homepage:
        # 使用新抓取的 short_description 字段
        short_desc = game.get('short_description', 'Play this exciting game for free!')
        # --- 关键修改: 链接现在指向 './game/...' ---
        all_game_cards_html += f"""
                <div class="bg-white rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
                    <a href="./game/{game['page_filename']}">
                        <img src="{game['thumbnail']}" alt="{game['title']}" class="w-full h-48 object-cover" onerror="this.onerror=null;this.src='[https://placehold.co/400x300/f5f5f7/6e6e73?text=Image+Not+Found](https://placehold.co/400x300/f5f5f7/6e6e73?text=Image+Not+Found)';">
                        <div class="p-5">
                            <h3 class="text-xl font-semibold text-apple-text mb-2">{game['title']}</h3>
                            <p class="text-sm text-apple-light-gray-text">{short_desc}</p>
                        </div>
                    </a>
                </div>
        """

    # 主页HTML模板
    homepage_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q47TS07D8C"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());

        gtag('config', 'G-Q47TS07D8C');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Free Game Arcade - Play The Best Free Online Games</title>
    <meta name="description" content="Discover and play hundreds of free online games at Free Game Arcade. New HTML5 games added daily. No downloads, just instant fun!">
    <link rel="canonical" href="{SITE_BASE_URL}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'apple-bg': '#f5f5f7',
                        'apple-text': '#1d1d1f',
                        'apple-blue': '#007aff',
                        'apple-light-gray-text': '#6e6e73',
                    }}
                }},
                fontFamily: {{
                    sans: ['-apple-system', 'BlinkMacSystemFont', "Segoe UI", 'Roboto', "Helvetica Neue", 'Arial', "Noto Sans", 'sans-serif', "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"],
                }}
            }}
        }}
    </script>
    <style>
        html, body {{ height: 100%; }}
        body {{ display: flex; flex-direction: column; }}
        main {{ flex-grow: 1; }}
    </style>
</head>
<body class="bg-apple-bg text-apple-text antialiased">
    <header class="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <a href="#" class="text-2xl font-bold text-apple-blue">FGA</a>
            </div>
        </div>
    </header>
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <section class="text-center py-12 md:py-20 bg-white rounded-xl shadow-lg">
            <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold text-apple-text mb-6">
                Free Game Arcade: <span class="text-apple-blue">Your Ultimate Hub</span> for Online Games
            </h1>
            <p class="text-lg text-apple-light-gray-text mb-8 max-w-2xl mx-auto">
                Dive into a world of endless fun! Hundreds of free HTML5 games await, ready to play instantly on any device.
            </p>
            <a href="#all-games" class="bg-apple-blue text-white font-semibold px-8 py-3 rounded-lg text-lg hover:bg-opacity-90 transition duration-150 ease-in-out transform hover:scale-105">
                Play Now
            </a>
        </section>
        <section id="all-games" class="py-12">
            <h2 class="text-3xl font-bold text-apple-text mb-8 text-center">All Games</h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                {all_game_cards_html}
            </div>
        </section>
        <section class="py-12 mt-8">
            <div class="bg-white p-8 rounded-xl shadow-lg max-w-3xl mx-auto text-center">
                <h2 class="text-3xl font-bold text-apple-text mb-4">Welcome to FreeGameArcade.space</h2>
                <p class="text-apple-light-gray-text leading-relaxed">
                    FreeGameArcade.space is your premier destination for an extensive collection of free online HTML5 games. Our mission is to provide instant access to a diverse range of games that you can enjoy on any device – PC, tablet, or mobile – without the need for downloads or installations. From action-packed adventures and brain-teasing puzzles to classic arcade hits and competitive sports games, we've got something for everyone. New games are added regularly, so there's always something new to discover. Start playing and have fun!
                </p>
            </div>
        </section>
    </main>
    <footer class="bg-gray-800 text-gray-300 py-12 mt-auto">
        <div class="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
             <p class="text-sm">&copy; <span id="currentYear"></span> FreeGameArcade.space. All rights reserved.</p>
        </div>
    </footer>
    <script>
        document.getElementById('currentYear').textContent = new Date().getFullYear();
    </script>
</body>
</html>
    """
    # --- 关键修改: 主页文件现在生成在根目录 ---
    homepage_filepath = 'index.html'
    with open(homepage_filepath, 'w', encoding='utf-8') as f:
        f.write(homepage_html)
    print(f"主页 index.html 已成功生成/更新于: {homepage_filepath}")

if __name__ == '__main__':
    generate_pages()

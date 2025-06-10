# page_generator.py
import json
import os
import time
import google.generativeai as genai
import random  # 添加random模块用于随机选择游戏

# --- 配置 ---
# 使用当前脚本所在目录作为基础路径
BASE_DIR = os.path.dirname(__file__)
GAMES_ARCHIVE_FILE = os.path.join(BASE_DIR, 'games_archive.json')
# 游戏页面输出到game文件夹
GAME_OUTPUT_DIR = os.path.join(BASE_DIR, 'game')
# 主页输出到当前目录
INDEX_OUTPUT_DIR = BASE_DIR
SITE_BASE_URL = "https://your-username.github.io/your-repo-name" 

# --- Gemini API 调用函数 ---
def generate_game_page_with_gemini(game_data, all_games):
    """使用Gemini API为单个游戏生成完整的HTML页面。"""
    
    # 重要安全提示: 请勿在此处直接写入您的API密钥。
    # 这个脚本被设计为从一个名为 "GEMINI_API_KEY" 的环境变量中安全地读取密钥。
    # 请参考第四步中的说明，在您的GitHub仓库的 "Secrets" 中设置此密钥。
    api_key = "AIzaSyDVfAsLX3sjJiz8befufBfo0NhMEmIVpcM"
    if not api_key:
        print("  -> 警告: 未设置 GEMINI_API_KEY 环境变量。无法生成页面。")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-pro-preview-06-05')
        
        page_url = f"{SITE_BASE_URL}/{game_data['page_filename']}"
        
        # 生成"猜你喜欢"部分的HTML
        you_might_also_like_html = generate_you_might_also_like_section(game_data, all_games)
        
        # 将HTML模板作为F-string，以便嵌入占位符以供AI参考
        html_template = f"""
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
    <!-- SEO Meta Tags -->
    <title>Play Kick the Pirate - Free Online Game | Free Game Arcade</title>
    <meta name="description" content="Play Kick the Pirate for free at Free Game Arcade. Turn this grumpy pirate into your personal punching bag, unlock wacky weapons, and blow off some steam! No download required, play directly in your browser.">
    <link rel="canonical" href="https://freegamearcade.space/game/kick-the-pirate.html">

    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Custom Tailwind Config (Consistent with homepage) -->
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
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
        }}
        ::-webkit-scrollbar-thumb {{
            background: #007aff;
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: #005bb5;
        }}
        /* Ensure body takes full height for footer positioning */
        html {{
            height: 100%;
        }}
        body {{
            min-height: 100%;
            display: flex;
            flex-direction: column;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
        }}
        main {{
            flex-grow: 1;
        }}
        /* Style for the 16:9 iframe container */
        .aspect-16-9 {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* 9 / 16 = 0.5625 */
        }}
        .aspect-16-9 iframe {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }}
    </style>
</head>
<body class="bg-apple-bg text-apple-text antialiased">

    <!-- Header / Navbar (Same as index.html) -->
    <header class="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Logo -->
                <div class="flex-shrink-0">
                    <a href="../index.html" class="text-2xl font-bold text-apple-blue">FGA</a>
                </div>

                <!-- Desktop Navigation -->
                <nav class="hidden md:flex space-x-6">
                    <a href="/categories/action.html" class="text-gray-600 hover:text-apple-blue px-3 py-2 rounded-md text-sm font-medium">Action</a>
                    <a href="/categories/puzzle.html" class="text-gray-600 hover:text-apple-blue px-3 py-2 rounded-md text-sm font-medium">Puzzle</a>
                    <a href="/categories/strategy.html" class="text-gray-600 hover:text-apple-blue px-3 py-2 rounded-md text-sm font-medium">Strategy</a>
                    <a href="/categories/sports.html" class="text-gray-600 hover:text-apple-blue px-3 py-2 rounded-md text-sm font-medium">Sports</a>
                </nav>

                <!-- Search Bar -->
                <div class="hidden md:flex items-center">
                    <input type="search" placeholder="Search games..." class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-apple-blue focus:border-apple-blue">
                    <button class="ml-2 px-4 py-2 bg-apple-blue text-white rounded-md text-sm hover:bg-opacity-90">Search</button>
                </div>

                <!-- Mobile Menu Button -->
                <div class="md:hidden flex items-center">
                    <button id="mobile-menu-button" class="text-gray-600 hover:text-apple-blue focus:outline-none">
                        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7"></path></svg>
                    </button>
                </div>
            </div>
        </div>

        <!-- Mobile Menu -->
        <div id="mobile-menu" class="md:hidden hidden bg-white shadow-lg">
            <a href="/categories/action.html" class="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 hover:text-apple-blue">Action</a>
            <a href="/categories/puzzle.html" class="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 hover:text-apple-blue">Puzzle</a>
            <a href="/categories/strategy.html" class="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 hover:text-apple-blue">Strategy</a>
            <a href="/categories/sports.html" class="block px-4 py-3 text-sm text-gray-700 hover:bg-gray-100 hover:text-apple-blue">Sports</a>
            <div class="p-4">
                <input type="search" placeholder="Search games..." class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:ring-apple-blue focus:border-apple-blue">
                <button class="mt-2 w-full px-4 py-2 bg-apple-blue text-white rounded-md text-sm hover:bg-opacity-90">Search</button>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <!-- Breadcrumb Navigation -->
        <nav class="mb-6" aria-label="Breadcrumb">
            <ol class="flex items-center space-x-2 text-sm">
                <li>
                    <a href="../index.html" class="text-apple-light-gray-text hover:text-apple-blue">Home</a>
                </li>
                <li>
                    <span class="text-gray-400">/</span>
                </li>
                <li class="font-medium text-apple-text" aria-current="page">
                    Pac-Xon New Realms
                </li>
            </ol>
        </nav>

        <!-- Game Title -->
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-apple-text mb-6 text-center">Kick the Pirate</h1>

        <!-- Game Embed Area -->
        <section class="mb-10">
            <div id="game-embed-container" class="aspect-16-9 bg-black rounded-lg shadow-2xl overflow-hidden mx-auto max-w-4xl">
                <iframe 
                    id="game-iframe"
                    src="https://cloud.onlinegames.io/games/2022/construct/92/kick-the-pirate/index-og.html" 
                    title="Kick the Pirate" 
                    class="border-0"
                    allowfullscreen 
                    allow="fullscreen; accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    loading="lazy">
                </iframe>
            </div>
            <div class="mt-5 text-center">
                <button id="fullscreen-button" class="bg-apple-blue text-white font-semibold px-6 py-3 rounded-lg hover:bg-opacity-80 transition duration-150 ease-in-out text-sm sm:text-base">
                    Enter Full Screen
                </button>
            </div>
        </section>

        <!-- How to Play Section -->
        <section class="mb-10 bg-white p-6 sm:p-8 rounded-xl shadow-lg max-w-3xl mx-auto">
            <h2 class="text-2xl sm:text-3xl font-bold text-apple-text mb-4">How to Play Kick the Pirate</h2>
            <div class="text-apple-light-gray-text space-y-3 leading-relaxed text-sm sm:text-base">
                <p>Ahoy matey! In Kick the Pirate, your job is simple: turn this grumpy pirate into your personal punching bag. It's a stress-busting clicker game perfect for blowing off some steam!</p>
                <p><strong>Core Gameplay:</strong></p>
                <ul class="list-disc list-inside ml-4 space-y-1">
                    <li>Start by clicking or tapping the pirate as fast (or as furiously) as you like.</li>
                    <li>Each hit earns you coins, which you'll use to buy new, wacky weapons.</li>
                    <li>Your goal is to deplete the pirate's health bar (at the bottom) to complete each level.</li>
                    <li>As you progress, the levels get tougher, and the pirate gets sassier.</li>
                    <li>You can swap out the ship's background if you want a change of scene by clicking the button on the bottom left corner to shop for new backgrounds.</li>
                    <li>If you'd prefer less graphic visuals, use the drop icon in the corner to toggle off the blood splatter. Toggle other settings like sound in the top right.</li>
                </ul>
                <p><strong>Weapons to Try:</strong></p>
                <p>There are tons of wacky weapons to unlock, each more satisfying than the last. You can switch between weapons using the buttons at the top of the screen. Some examples include:</p>
                <ul class="list-disc list-inside ml-4 space-y-1">
                    <li><strong>Flintlock Pistol:</strong> Classic and simple.</li>
                    <li><strong>Bone Key Gun:</strong> Looks like it came straight out of a cursed treasure chest.</li>
                    <li><strong>Battle Axe:</strong> Heavy damage and major pirate pain.</li>
                    <li><strong>Ship Anchor:</strong> Watch him go flying.</li>
                    <li><strong>Cannon:</strong> Boom! Need we say more?</li>
                    <li><strong>TNT Barrel:</strong> Great for pirate control.</li>
                </ul>
                <p>This game was developed by FreezeNova. While it uses cartoon-style visuals, the core gameplay revolves around humorous violence. Recommended for players 10 and up, with parental guidance if needed.</p>
            </div>
        </section>

        <!-- You Might Also Like Section -->
        {you_might_also_like_html}

    </main>

    <!-- Footer (Same as index.html) -->
    <footer class="bg-gray-800 text-gray-300 py-12 mt-auto">
        <div class="container mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
                <div>
                    <h3 class="text-lg font-semibold text-white mb-3">FGA</h3>
                    <p class="text-sm">Your ultimate hub for free online games.</p>
                </div>
                <div>
                    <h3 class="text-lg font-semibold text-white mb-3">Quick Links</h3>
                    <ul class="space-y-2">
                        <li><a href="/about.html" class="hover:text-apple-blue">About Us</a></li>
                        <li><a href="/contact.html" class="hover:text-apple-blue">Contact Us</a></li>
                        <li><a href="/privacy.html" class="hover:text-apple-blue">Privacy Policy</a></li>
                        <li><a href="/terms.html" class="hover:text-apple-blue">Terms of Service</a></li>
                    </ul>
                </div>
                <div>
                    <h3 class="text-lg font-semibold text-white mb-3">Connect</h3>
                    <p class="text-sm">Follow us on social media!</p>
                    <div class="flex justify-center space-x-4 mt-2">
                        <!-- Example: <a href="#" class="hover:text-apple-blue">Facebook</a> -->
                    </div>
                </div>
            </div>
            <hr class="border-gray-700 my-8">
            <p class="text-sm">&copy; <span id="currentYear"></span> FreeGameArcade.space. All rights reserved.</p>
            <p class="text-xs mt-1">Designed with <span class="text-red-500">&hearts;</span> using HTML & Tailwind CSS.</p>
        </div>
    </footer>

    <script >


        /**
 * 网站功能脚本
 * 包含了移动端菜单切换、页脚年份更新以及游戏全屏功能。
 */

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
        你是一位精通谷歌 SEO 和 HTML&TAIlwind 语法的十年全栈工程师
        把用户所输入的在线游戏链接，按照模板代码输出一模一样的完整版的 HTML 和 CSS 代码，游戏标题，一句话介绍，在线游戏的 IFRAME 内容，游戏基本情况叙述，
        要求这个网站在 PC 和移动端适配性良好，配色采用苹果典型色系，包含一个一级 H1 标签和多个 H2 标签，有 canonical url，网站语言是地道英文

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
    if not os.path.exists(GAMES_ARCHIVE_FILE):
        print("未找到游戏存档文件。")
        return

    with open(GAMES_ARCHIVE_FILE, 'r', encoding='utf-8') as f:
        all_games = json.load(f)

    if not os.path.exists(GAME_OUTPUT_DIR):
        os.makedirs(GAME_OUTPUT_DIR)

    for game in all_games:
        filepath = os.path.join(GAME_OUTPUT_DIR, game['page_filename'])
        if os.path.exists(filepath):
            print(f"-> 页面已存在，跳过: {game['title']}")
            continue

        print(f"-> 正在为AI生成页面: {game['title']}")
        
        page_html = generate_game_page_with_gemini(game, all_games)  # 传递所有游戏数据
        
        if page_html:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page_html)
            print(f"  -> 成功创建页面: {filepath}")
        else:
            print(f"  -> 跳过页面生成，因为AI调用失败: {game['title']}")
        
        time.sleep(2) 

    generate_homepage(all_games)

def generate_homepage(games):
    """根据所有游戏数据生成主页，展示所有生成的页面。"""
    print("\n正在生成主页 index.html...")
    
    # 扫描game目录中的所有HTML文件
    all_html_files = []
    for filename in os.listdir(GAME_OUTPUT_DIR):
        if filename.endswith('.html') and filename != 'index.html':
            file_path = os.path.join(GAME_OUTPUT_DIR, filename)
            game_title = filename.replace('.html', '').title()
            
            # 尝试从games列表中找到对应的游戏数据
            game_data = None
            for game in games:
                if game['page_filename'] == filename:
                    game_data = game
                    break
            
            # 如果找到了游戏数据，使用其中的信息
            if game_data:
                all_html_files.append({
                    'filename': filename,
                    'title': game_data['title'],
                    'thumbnail': game_data.get('thumbnail', ''),
                    'short_description': game_data.get('short_description', '')
                })
            else:
                # 如果没有找到游戏数据，使用默认值
                all_html_files.append({
                    'filename': filename,
                    'title': game_title,
                    'thumbnail': '',
                    'short_description': f'Play {game_title} online for free!'
                })
    
    # 生成所有游戏卡片的HTML
    all_game_cards_html = ""
    for game in all_html_files:
        thumbnail = game['thumbnail'] if game['thumbnail'] else 'https://placehold.co/400x300/f5f5f7/6e6e73?text=Game+Image'
        all_game_cards_html += f"""
                <div class="bg-white rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
                    <a href="./game/{game['filename']}">
                        <img src="{thumbnail}" alt="{game['title']}" class="w-full h-48 object-cover" onerror="this.onerror=null;this.src='https://placehold.co/400x300/f5f5f7/6e6e73?text=Image+Not+Found';">
                        <div class="p-5">
                            <h3 class="text-xl font-semibold text-apple-text mb-2">{game['title']}</h3>
                            <p class="text-sm text-apple-light-gray-text">{game['short_description']}</p>
                        </div>
                    </a>
                </div>
        """
    
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
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Custom Tailwind Config -->
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
            <a href="#featured-games" class="bg-apple-blue text-white font-semibold px-8 py-3 rounded-lg text-lg hover:bg-opacity-90 transition duration-150 ease-in-out transform hover:scale-105">
                Play Now
            </a>
        </section>

        <section id="featured-games" class="py-12">
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
    with open(os.path.join(INDEX_OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(homepage_html)
    print("主页 index.html 已成功生成/更新。")

if __name__ == '__main__':
    generate_pages()

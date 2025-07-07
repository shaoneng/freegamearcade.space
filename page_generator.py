# page_generator.py
import json
import os
import time
import google.generativeai as genai
import random
from bs4 import BeautifulSoup

# --- 配置 (Configuration) ---
GAMES_ARCHIVE_FILE = 'games_archive.json'
GAME_PAGE_DIR = 'game'  
SITE_BASE_URL = "https://shaoneng.github.io/freegamearcade.space"

# --- Gemini API 调用函数 (Gemini API Call Function) ---
def generate_game_page_with_gemini(game_data, all_games):
    """
    使用Gemini API为单个游戏生成具备“Apple”风格外观的HTML页面。
    Uses the Gemini API to generate an "Apple" style HTML page for a single game.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("  -> 警告: 未设置 GEMINI_API_KEY 环境变量。")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        page_url = f"{SITE_BASE_URL}/game/{game_data['page_filename']}"
        you_might_also_like_html = generate_you_might_also_like_section(game_data, all_games)
        
        # **关键修改 (CRITICAL CHANGE)**: 使用了你提供的明亮风格HTML模板
        # Used the light-themed HTML template you provided
        html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q47TS07D8C"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());

        gtag('config', 'G-Q47TS07D8C');
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9886602787991072"
     crossorigin="anonymous"></script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Placeholder Title</title>
    <meta name="description" content="Placeholder description.">
    <link rel="canonical" href="{page_url}">
    <!--JSON-LD-PLACEHOLDER-->
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            theme: {{
                extend: {{
                    colors: {{
                        'apple-bg': '#f5f5f7', 'apple-text': '#1d1d1f', 'apple-blue': '#007aff', 
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
        html {{ height: 100%; }} body {{ min-height: 100%; display: flex; flex-direction: column; }} main {{ flex-grow: 1; }} .aspect-16-9 {{ position: relative; width: 100%; padding-bottom: 56.25%; }} .aspect-16-9 iframe {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; }}
        .game-card-thumbnail {{ aspect-ratio: 300 / 200; background-color: #f0f0f0; }}
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
        <nav class="mb-6" aria-label="Breadcrumb"><ol class="flex items-center space-x-2 text-sm"><li><a href="../index.html" class="text-apple-light-gray-text hover:text-apple-blue">Home</a></li><li><span class="text-gray-400">/</span></li><li class="font-medium text-apple-text" aria-current="page">Placeholder Game</li></ol></nav>
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-bold text-apple-text mb-6 text-center">Placeholder Title</h1>
        <section class="mb-10">
            <div id="game-embed-container" class="aspect-16-9 bg-black rounded-lg shadow-2xl overflow-hidden mx-auto max-w-4xl"><iframe id="game-iframe" src="" title="Placeholder" class="border-0" allowfullscreen loading="lazy"></iframe></div>
            <div class="mt-5 text-center">
                <button id="fullscreen-button" class="bg-blue-500 hover:bg-blue-600 text-white font-semibold px-6 py-3 rounded-lg transition duration-150 ease-in-out text-sm sm:text-base">Enter Full Screen</button>
            </div>
        </section>
        <section class="mb-10 bg-white p-6 sm:p-8 rounded-xl shadow-lg max-w-3xl mx-auto"><h2 class="text-2xl sm:text-3xl font-bold text-apple-text mb-4">How to Play</h2><div class="text-apple-light-gray-text space-y-3 leading-relaxed text-sm sm:text-base"><p>Placeholder how-to-play content...</p></div></section>
        {you_might_also_like_html}
    </main>
    <footer class="bg-gray-800 text-gray-300 py-12 mt-auto"><div class="container mx-auto px-4 sm:px-6 lg:px-8 text-center"><p class="text-sm">&copy; <span id="currentYear"></span> FreeGameArcade.space. All rights reserved.</p></div></footer>
    <script src="../scripts.js"></script>
</body>
</html>
"""
        # **关键修改 (CRITICAL CHANGE)**: Prompt也改回更通用的版本
        prompt = f"""
        You are an expert content creator for a gaming website, skilled in writing engaging and SEO-friendly content.
        Your task is to populate the provided HTML template for the game "{game_data['title']}".

        **Game Data for Context:**
        - Title: "{game_data['title']}"
        - Iframe URL: "{game_data['iframe_url']}"
        - Canonical URL: "{page_url}"
        - Original Description (for inspiration): "{game_data.get('description', 'A fun and exciting game.')}"

        **HTML Template to use:**
        ```html
        {html_template}
        ```

        **Your Content Generation Instructions:**

        1.  **SEO Title (`<title>`)**: Use this exact format: "Play {game_data['title']} - Free Online Game | Free Game Arcade".

        2.  **Meta Description (`<meta name="description">`)**:
            - Write a clear and concise summary of the game (80-120 words).
            - Naturally include keywords like "free browser game" and "play online for free".
            - The goal is to inform the user what the game is about.

        3.  **Canonical URL (`<link rel="canonical">`)**: Ensure the `href` attribute is set to: `{page_url}`.

        4.  **Page Content**:
            -   **Breadcrumb**: Update the last item to be the game's title: `{game_data['title']}`.
            -   **Main Title (`<h1>`)**: Use the game's title: `{game_data['title']}`.
            -   **Iframe**: Set the `src` to `{game_data['iframe_url']}` and the `title` to `{game_data['title']}`.
            -   **How to Play Section**:
                -   Set the `<h2>` title to "How to Play {game_data['title']}".
                -   Based on the original description, write a simple and clear "How to Play" guide in English using paragraphs (`<p>`).

        5.  **Final Output**:
            -   Populate the entire HTML template with the new content.
            -   Provide ONLY the final, complete, raw HTML code.
        """
        
        response = model.generate_content(prompt)
        generated_html_raw = response.text.strip()
        
        generated_html = generated_html_raw
        if generated_html.startswith('```html'):
            generated_html = generated_html[7:]
        if generated_html.endswith('```'):
            generated_html = generated_html[:-3]
        
        soup = BeautifulSoup(generated_html, 'html.parser')
        
        meta_description_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description_content = ""
        if meta_description_tag:
            meta_description_content = meta_description_tag.get('content', '')

        json_ld_data = {
          "@context": "https://schema.org",
          "@type": "VideoGame",
          "name": game_data['title'],
          "url": page_url,
          "image": game_data['thumbnail'],
          "description": meta_description_content,
          "gamePlatform": "PC",
          "operatingSystem": "Any",
          "applicationCategory": "Game",
          "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
          }
        }

        json_ld_script_string = f'<script type="application/ld+json">{json.dumps(json_ld_data, indent=2)}</script>'
        final_html = generated_html.replace('<!--JSON-LD-PLACEHOLDER-->', json_ld_script_string)
        
        print(f"  -> Successfully generated HTML and injected structured data for '{game_data['title']}'.")
        return final_html.strip()

    except Exception as e:
        print(f"  -> ERROR: An error occurred when calling Gemini API or processing HTML: {e}")
        return None

def generate_you_might_also_like_section(current_game, all_games):
    """Generates the 'You Might Also Like' section with corrected relative paths and light theme styling."""
    other_games = [game for game in all_games if game['id'] != current_game['id']]
    num_games_to_show = min(4, len(other_games))
    if num_games_to_show < 1:
        return ""
        
    selected_games = random.sample(other_games, num_games_to_show)
    
    game_cards_html = ""
    for game in selected_games:
        thumbnail_path = game.get('thumbnail', '')
        if thumbnail_path.startswith("assets/"):
            thumbnail_path = f"../{thumbnail_path}"

        short_desc = game.get('short_description', f"Play {game['title']} online for free!")
        
        game_cards_html += f"""
        <div class="bg-white rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
            <a href="../game/{game['page_filename']}" class="game-card-thumbnail">
                <img src="{thumbnail_path}" alt="{game['title']}" onerror="this.onerror=null;this.src='https://placehold.co/300x200/f5f5f7/1d1d1f?text=Game+Image';" class="w-full h-40 object-cover" loading="lazy" width="300" height="200">
                <div class="p-4">
                    <h3 class="text-lg font-semibold text-apple-text mb-1 truncate" title="{game['title']}">{game['title']}</h3>
                    <p class="text-xs text-apple-light-gray-text h-10 overflow-hidden">{short_desc[:100]}...</p>
                </div>
            </a>
        </div>
        """
    
    return f"""
    <section class="mb-10">
        <h2 class="text-2xl sm:text-3xl font-bold text-apple-text mb-8 text-center">You Might Also Like</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {game_cards_html}
        </div>
    </section>
    """

def generate_pages():
    """Reads the archive and calls the AI to generate a complete HTML page for each game."""
    print("\nStarting to generate web pages...")

    if not os.path.exists(GAMES_ARCHIVE_FILE):
        print(f"ERROR: Archive file {GAMES_ARCHIVE_FILE} not found. Please run scraper.py first.")
        return

    with open(GAMES_ARCHIVE_FILE, 'r', encoding='utf-8') as f:
        all_games = json.load(f)

    os.makedirs(GAME_PAGE_DIR, exist_ok=True)
    
    print("Regenerating all game pages to apply latest optimizations...")
    
    for game in all_games:
        game_id = str(game.get('id'))
        if not game_id:
            print(f"WARNING: Game '{game.get('title', 'Unknown')}' is missing 'id', skipping.")
            continue

        print(f"-> Generating page for game: {game['title']} (ID: {game_id})")
        
        filepath = os.path.join(GAME_PAGE_DIR, game['page_filename'])
        page_html = generate_game_page_with_gemini(game, all_games)

        if page_html:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(page_html)
            print(f"  -> Successfully created/updated page: {filepath}")
        else:
            print(f"  -> Page generation failed for: {game['title']}")

        time.sleep(1)

    print("\nAll game pages have been regenerated.")
    generate_homepage(all_games)

def generate_homepage(games):
    """Generates the homepage with a light, Apple-like theme."""
    print("\nGenerating homepage index.html...")
    games_for_homepage = sorted(games, key=lambda x: str(x.get('id', '')), reverse=True)
    games_json_string = json.dumps(games_for_homepage)

    homepage_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-Q47TS07D8C"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){{dataLayer.push(arguments);}}
        gtag('js', new Date());

        gtag('config', 'G-Q47TS07D8C');
    </script>
    <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9886602787991072"
     crossorigin="anonymous"></script>
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
        html, body {{ height: 100%; }} body {{ display: flex; flex-direction: column; }} main {{ flex-grow: 1; }}
        .game-card-thumbnail {{ aspect-ratio: 300 / 200; background-color: #f0f0f0; }}
    </style>
</head>
<body class="bg-apple-bg text-apple-text antialiased">
    <header class="bg-white/80 backdrop-blur-md shadow-sm sticky top-0 z-50">
        <div class="container mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <a href="/" class="text-2xl font-bold text-apple-blue">FGA</a>
            </div>
        </div>
    </header>
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <section class="text-center py-12 md:py-20 bg-white rounded-xl shadow-lg">
            <h1 class="text-4xl sm:text-5xl md:text-6xl font-bold text-apple-text mb-6">Free Game Arcade: <span class="text-apple-blue">Your Ultimate Hub</span> for Online Games</h1>
            <p class="text-lg text-apple-light-gray-text mb-8 max-w-2xl mx-auto">Dive into a world of endless fun! Hundreds of free HTML5 games await, ready to play instantly on any device.</p>
            <a href="#all-games" class="bg-apple-blue text-white font-semibold px-8 py-3 rounded-lg text-lg hover:bg-opacity-90 transition duration-150 ease-in-out transform hover:scale-105">Play Now</a>
        </section>
        <section id="all-games" class="py-12">
            <h2 class="text-3xl font-bold text-apple-text mb-8 text-center">All Games</h2>
            <div id="game-grid" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                <!-- Game cards will be dynamically loaded here by JavaScript -->
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
    <script>
        window.GAMES_DATA = {games_json_string};
    </script>
    <script src="homepage.js"></script>
</body>
</html>
    """
    homepage_filepath = 'index.html'
    with open(homepage_filepath, 'w', encoding='utf-8') as f:
        f.write(homepage_html)
    print(f"Homepage index.html has been successfully generated/updated.")

if __name__ == '__main__':
    generate_pages()

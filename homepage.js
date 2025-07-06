// homepage.js

document.addEventListener('DOMContentLoaded', function() {
    const gameGrid = document.getElementById('game-grid');
    const sentinel = document.createElement('div');
    sentinel.id = 'sentinel';

    // **关键修改**: 检查数据是否存在，如果不存在则显示错误
    if (!gameGrid || typeof window.GAMES_DATA === 'undefined') {
        if (gameGrid) {
            gameGrid.innerHTML = '<p class="text-center col-span-full">Could not load games data. An error occurred.</p>';
        }
        console.error("GAMES_DATA is not defined. Check page_generator.py");
        return;
    }

    const allGames = window.GAMES_DATA; // **关键修改**: 直接从全局变量获取数据
    let currentPage = 0;
    const gamesPerPage = 16;
    let isLoading = false;

    // 创建游戏卡片的函数 (保持不变)
    function createGameCard(game) {
        const short_desc = game.short_description || 'Play this exciting game for free!';
        const imageErrorHandling = `this.onerror=null;this.src='https://placehold.co/400x300/f5f5f7/6e6e73?text=Image+Not+Found';`;
        
        return `
            <div class="bg-white rounded-xl shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
                <a href="./game/${game.page_filename}">
                    <img src="${game.thumbnail}" alt="${game.title}" class="w-full h-48 object-cover" loading="lazy" width="300" height="200" onerror="${imageErrorHandling}">
                    <div class="p-5">
                        <h3 class="text-xl font-semibold text-apple-text mb-2">${game.title}</h3>
                        <p class="text-sm text-apple-light-gray-text">${short_desc}</p>
                    </div>
                </a>
            </div>
        `;
    }

    // 渲染游戏的函数 (保持不变)
    function renderGames() {
        if (isLoading) return;
        isLoading = true;

        const start = currentPage * gamesPerPage;
        const end = start + gamesPerPage;
        const gamesToRender = allGames.slice(start, end);

        if (gamesToRender.length === 0 && currentPage === 0) {
            gameGrid.innerHTML = '<p class="text-center col-span-full">No games found.</p>';
            isLoading = false;
            return;
        }

        gamesToRender.forEach(game => {
            gameGrid.innerHTML += createGameCard(game);
        });

        currentPage++;
        isLoading = false;

        if (currentPage * gamesPerPage >= allGames.length) {
            if (sentinel.parentNode) {
                observer.unobserve(sentinel);
                sentinel.remove();
            }
        }
    }

    // 设置 Intersection Observer (保持不变)
    const observer = new IntersectionObserver(entries => {
        if (entries[0].isIntersecting && !isLoading) {
            renderGames();
        }
    }, {
        rootMargin: '0px 0px 200px 0px'
    });

    // 启动流程
    gameGrid.after(sentinel);
    observer.observe(sentinel);
});
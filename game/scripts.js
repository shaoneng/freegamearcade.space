/**
 * 网站功能脚本
 * 包含了移动端菜单切换、页脚年份更新以及游戏全屏功能。
 */

// 当整个HTML文档加载完成后执行
        // Mobile menu toggle
        const mobileMenuButton = document.getElementById('mobile-menu-button');
        const mobileMenu = document.getElementById('mobile-menu');
        if (mobileMenuButton && mobileMenu) {
            mobileMenuButton.addEventListener('click', () => {
                mobileMenu.classList.toggle('hidden');
            });
        }

        // Set current year in footer
        const currentYearSpan = document.getElementById('currentYear');
        if (currentYearSpan) {
            currentYearSpan.textContent = new Date().getFullYear();
        }

        // Fullscreen functionality
        const fullscreenButton = document.getElementById('fullscreen-button');
        const gameIframe = document.getElementById('game-iframe'); // Target the iframe itself

        if (fullscreenButton && gameIframe) {
            fullscreenButton.addEventListener('click', () => {
                if (!document.fullscreenElement) {
                    // Try to make the iframe fullscreen
                    if (gameIframe.requestFullscreen) {
                        gameIframe.requestFullscreen().catch(err => console.error("Error attempting to enable full-screen mode:", err));
                    } else if (gameIframe.mozRequestFullScreen) { /* Firefox */
                        gameIframe.mozRequestFullScreen();
                    } else if (gameIframe.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
                        gameIframe.webkitRequestFullscreen();
                    } else if (gameIframe.msRequestFullscreen) { /* IE/Edge */
                        gameIframe.msRequestFullscreen();
                    }
                } else {
                    if (document.exitFullscreen) {
                        document.exitFullscreen().catch(err => console.error("Error attempting to disable full-screen mode:", err));
                    }
                }
            });

            document.addEventListener('fullscreenchange', () => {
                // Check if the iframe is the fullscreen element
                if (document.fullscreenElement === gameIframe) {
                    fullscreenButton.textContent = '退出全屏'; // Exit Fullscreen in Chinese
                } else {
                    fullscreenButton.textContent = '进入全屏'; // Enter Fullscreen in Chinese
                }
            });
            
        }
        
        // --- New Script to Load Component ---
        // This script runs after the main document has been loaded
        document.addEventListener('DOMContentLoaded', function() {
            // Fetch the content of the component file
            fetch('Like.html')
                .then(response => {
                    // Check if the request was successful
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.text();
                })
                .then(data => {
                    // Insert the fetched HTML content into the placeholder div
                    document.getElementById('related-games-placeholder').innerHTML = data;
                })
                .catch(error => {
                    // Log an error to the console if fetching fails
                    console.error('Error loading the related games component:', error);
                    // Optionally, display a message to the user in the placeholder
                    document.getElementById('related-games-placeholder').textContent = 'Could not load related games.';
                });
        });
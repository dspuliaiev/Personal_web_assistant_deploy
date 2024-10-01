// auto_refresh.js

// Function for updating news via AJAX
function updateNews() {
    var keyword = document.querySelector('input[name="keyword"]').value;
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/news/?keyword=' + encodeURIComponent(keyword), true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var newsList = JSON.parse(xhr.responseText);
            var newsContainer = document.querySelector('#news-container');
            newsContainer.innerHTML = ''; // Clearing the container before adding new news
            newsList.forEach(function(newsItem) {
                var newsElement = document.createElement('div');
                newsElement.innerHTML = `
                    <h2>${decodeURIComponent(newsItem.title)}</h2>
                    <p>${decodeURIComponent(newsItem.description)}</p>
                    <a href="${decodeURIComponent(newsItem.link)}">Read more</a>
                `;
                newsContainer.appendChild(newsElement);
            });
        }
    };
    xhr.send();
}

// Call the news update function every 10 minutes (600000 milliseconds)
setInterval(updateNews, 600000);
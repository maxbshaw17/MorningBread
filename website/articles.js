console.log("Before fetch");
fetch('http://127.0.0.1:5000/articles_tickers_api/articles_api')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    return response.json();
  })
  .then(articles => {
    console.log("After fetch");
    const dynamicArticlesContainer = document.getElementById('dynamic-articles');

    articles.forEach(article => {
      const articleElement = document.createElement('div');
      articleElement.classList.add('featured-article');

      articleElement.innerHTML = `
        <h1>${article.headline}</h1>
        <div class="article-preview">
          <img src="placeholder_image.png" alt="Article Image">
          <div>
            <p class="article-summary">${article.summary}</p>
            <a href="#" class="article-link">Link...</a>
            <a class="read-more-link">Show Summary</a>
          </div>
        </div>
      `;

      dynamicArticlesContainer.appendChild(articleElement);
    });
  })
  .catch(error => {
    console.error('Error fetching articles:', error);
    const errorMessage = document.createElement('div');
    errorMessage.textContent = 'Error fetching articles. Please try again later.';
    errorMessage.classList.add('error-message');
    dynamicArticlesContainer.appendChild(errorMessage);
  });
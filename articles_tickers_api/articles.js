fetch('/articles_tickers_api/articles_api')
  .then(response => response.json())
  .then(articles => {
    const dynamicArticlesContainer = document.getElementById('dynamic-articles');

    // Loop through the articles and display them on the page
    articles.forEach(article => {
      const articleElement = document.createElement('div');
      articleElement.classList.add('article-preview'); // Add a class for styling
      articleElement.innerHTML = `
        <h1>${article.headline}</h1>
        <p>${article.summary}</p>
      `;
      dynamicArticlesContainer.appendChild(articleElement);
    });
  })
  .catch(error => console.error('Error fetching articles:', error));
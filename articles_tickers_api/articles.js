fetch('/articles_tickers_api/articles_api')
  .then(response => response.json())
  .then(articles => {
    // Loop through the articles and display them on the page
    articles.forEach(article => {
      const articleElement = document.createElement('div');
      articleElement.innerHTML = `
        <h2>${article.headline}</h2>
        <p>${article.summary}</p>
      `;
      document.body.appendChild(articleElement);
    });
  })
  .catch(error => console.error('Error fetching articles:', error));
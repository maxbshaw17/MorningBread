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

    articles.forEach((article, index) => {
      // Create the featured article element
      const featuredArticleElement = document.createElement('div');
      featuredArticleElement.classList.add('featured-article');
      if (index === 0) {
        featuredArticleElement.classList.add('first-article');
      }
      featuredArticleElement.innerHTML = `
        <h1>${article.headline}</h1>
        <div class="article-preview">
          <img src="placeholder_image.png" alt="Article Image">
          <div>
            <p class="article-summary">Summary</p>
            <a href="#" class="article-link">Link...</a>
            <a class="read-more-link">Show Summary</a>
          </div>
        </div>
      `;

      // Create the secondary articles element
      const secondaryArticleElement = document.createElement('div');
      secondaryArticleElement.classList.add('secondary-articles');
      secondaryArticleElement.innerHTML = `
        <h1>${article.headline}</h1>
        <div class="article-preview">
          <img src="placeholder_image.png" alt="Article Image">
          <div>
            <p class="article-summary">Summary</p>
            <a href="#" class="article-link">Link...</a>
            <a class="read-more-link">Show Summary</a>
          </div>
        </div>
      `;

      // Append the elements to the container
      dynamicArticlesContainer.appendChild(featuredArticleElement);
      dynamicArticlesContainer.appendChild(secondaryArticleElement);
    });

    // Add click event listener to each "Read More" link
    const readMoreLinks = document.querySelectorAll('.read-more-link');

    readMoreLinks.forEach(link => {
      const articleSummary = link.parentNode.querySelector('.article-summary');
      const articleLink = link.parentNode.querySelector('.article-link');
    
      // Initially, set the summary and link to be hidden
      articleSummary.style.display = 'none';
      articleLink.style.display = 'none';
    
      link.addEventListener('click', () => {
        articleSummary.style.display = articleSummary.style.display === 'none' ? 'block' : 'none';
        articleLink.style.display = articleLink.style.display === 'none' ? 'inline' : 'none';
        link.textContent = articleSummary.style.display === 'none' ? 'Show Summary' : 'Hide Summary';
      });
    });
  })
  .catch(error => {
    console.error('Error fetching articles:', error);
    const errorMessage = document.createElement('div');
    errorMessage.textContent = 'Error fetching articles. Please try again later.';
    errorMessage.classList.add('error-message');
    dynamicArticlesContainer.appendChild(errorMessage);
  });
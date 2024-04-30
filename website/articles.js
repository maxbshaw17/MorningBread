console.log("Before fetch");
fetch('http://127.0.0.1:5000/dynamic_api/articles_api')
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    return response.json();
  })
  .then(articles => {
    console.log("After fetch");
    const dynamicArticlesContainer = document.getElementById('dynamic-articles');

    // Create the featured article section
    const featuredArticleSection = document.createElement('div');
    featuredArticleSection.classList.add('featured-article-section');

    // Create the secondary articles section
    const secondaryArticlesSection = document.createElement('div');
    secondaryArticlesSection.classList.add('secondary-articles-section');

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
            <a href="${article.link}" class="article-link" target="_blank">Original Article</a>
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
            <a href="${article.link}" class="article-link" target="_blank">Original Article</a>
            <a class="read-more-link">Show Summary</a>
          </div>
        </div>
      `;

      // Append the featured article to the featured article section
      featuredArticleSection.appendChild(featuredArticleElement);

      // Append the secondary article to the secondary articles section
      secondaryArticlesSection.appendChild(secondaryArticleElement);
    });

    // Append the sections to the container
    dynamicArticlesContainer.appendChild(featuredArticleSection);
    dynamicArticlesContainer.appendChild(secondaryArticlesSection);

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
console.log("Before fetch");
fetch('http://127.0.0.1:5000/dynamic_api/articles_api')
  .then(response => {
    console.log(`Response status: ${response.status}`);
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    return response.json();
  })
  .then(articles => {
    console.log("After fetch");
    console.log("Fetched articles:", articles);
    const dynamicArticlesContainer = document.getElementById('dynamic-articles');

    // Create the featured article section
    const featuredArticleSection = document.createElement('div');
    featuredArticleSection.classList.add('featured-article-section');

    // Create the secondary articles section
    const secondaryArticlesSection = document.createElement('div');
    secondaryArticlesSection.classList.add('secondary-articles-section');

    const displayedArticles = new Set();

    articles.forEach((article, index) => {
      // Check if the article has already been displayed
      if (displayedArticles.has(article.summarized_headline)) {
        return; // Skip this article
      }
      displayedArticles.add(article.summarized_headline);

      console.log('Creating featured article element:', article.summarized_headline);
      const featuredArticleElement = document.createElement('div');
      featuredArticleElement.classList.add('featured-article');
      if (index === 0) {
        featuredArticleElement.classList.add('first-article');
      }
      featuredArticleElement.innerHTML = `
        <h1>${article.summarized_headline}</h1>
        <div class="article-preview">
          <img src="web_pages/morningbread.png" alt="Article Image">
          <div>
            <a href="${article.link}" class="article-link" target="_blank">Original Article</a>
          </div>
        </div>
      `;

      console.log('Creating secondary article element:', article.summarized_headline);
      const secondaryArticleElement = document.createElement('div');
      secondaryArticleElement.classList.add('secondary-articles');
      secondaryArticleElement.innerHTML = `
        <h1>${article.summarized_headline}</h1>
        <div class="article-preview">
          <img src="web_pages/morningbread.png" alt="Article Image">
          <div>
            <a href="${article.link}" class="article-link" target="_blank">Original Article</a>
          </div>
        </div>
      `;

      // Append the featured article to the featured article section
      featuredArticleSection.appendChild(featuredArticleElement);

      // Append the secondary article to the secondary articles section
      secondaryArticlesSection.appendChild(secondaryArticleElement);
    });

    // Append the sections to the container
    console.log('Appending featured article section to container');
    dynamicArticlesContainer.appendChild(featuredArticleSection);
    console.log('Appending secondary article section to container');
    dynamicArticlesContainer.appendChild(secondaryArticlesSection);
  })
  .catch(error => {
    console.error('Error fetching articles:', error);
    const errorMessage = document.createElement('div');
    errorMessage.textContent = 'Error fetching articles. Please try again later.';
    errorMessage.classList.add('error-message');
    dynamicArticlesContainer.appendChild(errorMessage);
  });
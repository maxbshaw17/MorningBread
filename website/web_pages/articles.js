console.log("Before fetch");
fetch('http://127.0.0.1:5000/dynamic_api/articles_api')
  .then(response => {
    console.log(`Response status: ${response.status}`);
    console.log(`Response status: ${response.status}`);
    if (!response.ok) {
      throw new Error(`HTTP error ${response.status}`);
    }
    return response.json();
  })
  .then(articles => {
    console.log("After fetch");
    console.log("Fetched articles:", articles);
    console.log("Fetched articles:", articles);
    const dynamicArticlesContainer = document.getElementById('dynamic-articles');
    // Group articles by group_id
    const groupedArticles = {};
    articles.forEach(article => {
      const groupId = article.group_id;
      if (!groupedArticles[groupId]) {
        groupedArticles[groupId] = [];
      }
      groupedArticles[groupId].push(article);
    });
    // Create article sections for each group
    Object.entries(groupedArticles).forEach(([groupId, groupArticles]) => {
      const articleSection = document.createElement('div');
      articleSection.classList.add('article-section');
      // Group articles by headline within each group
      const headlineGroups = {};
      groupArticles.forEach(article => {
        const headline = article.summarized_headline;
        if (!headlineGroups[headline]) {
          headlineGroups[headline] = [];
        }
        headlineGroups[headline].push(article);
      });
      // Create article elements for each headline group
      Object.entries(headlineGroups).forEach(([headline, articlesWithSameHeadline]) => {
        const articleElement = document.createElement('div');
        articleElement.classList.add('featured-article');
        articleElement.innerHTML = `
          <h1>${headline}</h1>
          <div class="article-preview">
            <img src="morningbread.png" alt="Article Image">
            <div>
              <p class="article-summary" style="display: none;">Summary</p>
              <div class="links-container">
                ${createLinkColumns(articlesWithSameHeadline)}
              </div>
            </div>
          </div>
        `;
        articleSection.appendChild(articleElement);
      });
      dynamicArticlesContainer.appendChild(articleSection);
    });
  })
  .catch(error => {
    console.error('Error fetching articles:', error);
    const errorMessage = document.createElement('div');
    errorMessage.textContent = 'Error fetching articles. Please try again later.';
    errorMessage.classList.add('error-message');
    dynamicArticlesContainer.appendChild(errorMessage);
  });

function createLinkColumns(articles) {
  const linksContainer = document.createElement('div');
  linksContainer.classList.add('links-columns');

  const columnSize = 3;
  const numColumns = Math.ceil(articles.length / columnSize);

  for (let i = 0; i < numColumns; i++) {
    const column = document.createElement('div');
    column.classList.add('links-column');

    for (let j = i * columnSize; j < (i + 1) * columnSize && j < articles.length; j++) {
      const article = articles[j];
      const linkUrl = new URL(article.link);
      const hostname = linkUrl.hostname;
      const websiteName = hostname.split('.')[1] || hostname;
      const linkElement = document.createElement('a');
      linkElement.href = article.link;
      linkElement.textContent = ` ${websiteName} `; // Add spaces around the website name
      linkElement.target = '_blank';
      linkElement.classList.add('orange-link'); // Add a class for styling
      column.appendChild(linkElement);
    }

    linksContainer.appendChild(column);
  }

  return linksContainer.outerHTML;
}
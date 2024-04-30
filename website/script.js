// Function to update the current time
function updateTime() {
    var currentTimeElement = document.getElementById('currentTime');
    var currentTime = new Date();
    var options = { hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true };
    currentTimeElement.innerText = currentTime.toLocaleTimeString(undefined, options);
}

// Search function
const searchInput = document.getElementById('searchInput');
const articleContainer = document.getElementById('dynamic-articles');
const markInstance = new Mark(articleContainer);

searchInput.addEventListener('input', () => {
  const searchTerm = searchInput.value.trim();

  if (searchTerm) {
    markInstance.unmark();
    markInstance.mark(searchTerm, {
      separateWordSearch: false,
      accuracy: 'exactly',
      className: 'highlighted'
    });
  } else {
    markInstance.unmark();
  }
});

// Call updateTime function nearly immediately
setInterval(updateTime, 0);

// Update the current date
var currentDateElement = document.getElementById('currentDate');
var currentDate = new Date();
var options = { year: 'numeric', month: 'long', day: 'numeric' };
currentDateElement.innerText = currentDate.toLocaleDateString(undefined, options);

// Get all "Read More" links
const readMoreLinks = document.querySelectorAll('.read-more-link');

// Add click event listener to each link
readMoreLinks.forEach(link => {
    link.addEventListener('click', () => {
        // Get the article summary element
        const articleSummary = link.parentNode.querySelector('.article-summary');
        // Get the article link element
        const articleLink = link.parentNode.querySelector('.article-link');

        // Toggle the display of the article summary and link
        articleSummary.style.display = articleSummary.style.display === 'none' ? 'block' : 'none';
        articleLink.style.display = articleLink.style.display === 'none' ? 'inline' : 'none';

        // Update the link text
        link.textContent = articleSummary.style.display === 'none' ? 'Show Summary' : 'Hide Summary';
    });
});
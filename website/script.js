// Function to update the current time
function updateTime() {
    var currentTimeElement = document.getElementById('currentTime');
    var currentTime = new Date();
    var options = { hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true };
    currentTimeElement.innerText = currentTime.toLocaleTimeString(undefined, options);
}

// Call updateTime function nearly immediately
setInterval(updateTime, 0);

// Update the current date
var currentDateElement = document.getElementById('currentDate');
var currentDate = new Date();
var options = { year: 'numeric', month: 'long', day: 'numeric' };
currentDateElement.innerText = currentDate.toLocaleDateString(undefined, options);

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
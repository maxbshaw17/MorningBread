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

function updateNYSEStatus() {
  const nyseStatus = document.getElementById('nyse-status');
  const currentTime = new Date();
  const currentHour = currentTime.getHours();
  const currentDay = currentTime.getDay(); // 0 = Sunday, 1 = Monday, ..., 6 = Saturday

  // Check if it's a weekend
  const isWeekend = currentDay === 0 || currentDay === 6;

  // NYSE is open from 9:30 AM to 4:00 PM on weekdays
  const isOpen = !isWeekend && currentHour >= 9 && currentHour < 16;

  nyseStatus.innerHTML = 'The New York Stock Exchange is';

  const statusText = document.createElement('span');
  statusText.textContent = isOpen ? 'OPEN' : 'CLOSED';
  statusText.classList.add('status-text', isOpen ? 'open' : 'closed');

  nyseStatus.appendChild(statusText);
}

// Call the function initially and then update every minute
updateNYSEStatus();
setInterval(updateNYSEStatus, 60 * 1000);
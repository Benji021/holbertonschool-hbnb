// Part 1: DOM initialisation
document.addEventListener('DOMContentLoaded', () => {
    // Simulates data retrieved from an API
    const place = {
      id: 1,
      name: "Villa by the sea",
      host: "Jean Dupont",
      price_per_night: 120,
      description: "Charming villa overlooking the Mediterranean Sea, ideal for relaxing",
      amenities: ["Wi-Fi", "Swimming pool", "Fully equipped kitchen", "Air-conditioning"]
  };

  const reviews = [
      {
          user: "Alice",
          comment: "Wonderful place, very friendly host!",
          rating: 5
      },
      {
          user: "Bob",
          comment: "Great stay but a bit noisy in the evening",
          rating: 4
      }
  ];

  // Display the place details and reviews
  displayPlaceDetails(place);
  displayReviews(reviews);

  // Add event listener for login form
  const loginForm = document.getElementById('login-form');
  if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
          event.preventDefault();
          await handleLoginFormSubmission();
      });
  }
});

// Part 2: Displaying location details and notices
function displayPlaceDetails(place) {
  const section = document.getElementById("place-details");
  section.classList.add("place-details");

  section.innerHTML = `
      <h2>${place.name}</h2>
      <div class="place-info">
          <p><strong>Hôte :</strong> ${place.host}</p>
          <p><strong>Prix by night :</strong> ${place.price_per_night}€</p>
          <p><strong>Description :</strong> ${place.description}</p>
          <p><strong>Amenities :</strong> ${place.amenities.join(", ")}</p>
      </div>
  `;
}

function displayReviews(reviews) {
  const section = document.getElementById("reviews");
  section.innerHTML = ""; // empty the existing one

  if (reviews.length === 0) {
      section.innerHTML = "<p>No reviews yet.</p>";
      return;
  }

  reviews.forEach((review) => {
      const card = document.createElement("article");
      card.className = "review-card";
      card.innerHTML = `
          <p><strong>${review.user}</strong> - Note : ${"★".repeat(review.rating)}${"☆".repeat(5 - review.rating)}</p>
          <p>${review.comment}</p>
      `;
      section.appendChild(card);
  });
}

// Part 3 : Connection logic
async function handleLoginFormSubmission() {
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();

  if (!email || !password) {
      alert('Please fill in all fields.');
      return;
  }

  try {
      const loginSuccess = await loginUser(email, password);
      if (loginSuccess) {
          window.location.href = 'index.html'; // Redirection on success
      } else {
          alert('Connection failed.');
      }
  } catch (error) {
      console.error('Connection attempt error', error);
      alert('Connection error. Please try again later.');
  }
}

async function loginUser(email, password) {
  const response = await fetch('http://localhost:5000/api/v1/login', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password })
  });

  if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`; // Storing the token in a cookie
      return true;
  } else {
      const errorData = await response.json();
      console.error('Erreur API:', errorData);
      return false;
  }
}

// Function to retrieve a cookie by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';')[0];
    return null;
}

// Hide/show login link depending on token presence
function checkAuthenticationAndInit() {
    const token = getCookie('token');
    const loginLink = document.querySelector('.login-button');

    if (!token) {
        loginLink.style.display = 'inline';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

// Retrieving locations from the API
async function fetchPlaces(token) {
    try {
        const response = await fetch('http://localhost:5000/api/v1/places', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) throw new Error('Fetch error');

        const places = await response.json();
        window.placesData = places; // global stock to filter
        displayPlaces(places);
    } catch (error) {
        console.error('Site recovery error :', error);
    }
}

// Dynamically generate location maps
function displayPlaces(places) {
    const section = document.getElementById('places-list');
    section.innerHTML = '<h2>Places</h2>'; // reset

    places.forEach(place => {
        const card = document.createElement('div');
        card.className = 'place-card';
        card.setAttribute('data-price', place.price_per_night);
        card.innerHTML = `
            <h3>${place.name}</h3>
            <p>Price : ${place.price_per_night}€ by night</p>
            <a href="place.html?id=${place.id}" class="details-button">Details</a>
        `;
        section.appendChild(card);
    });
}

// Filter locations by max price
function setupPriceFilter() {
    const filter = document.getElementById('price-filter');
    filter.addEventListener('change', () => {
        const max = parseFloat(filter.value);
        document.querySelectorAll('.place-card').forEach(card => {
            const price = parseFloat(card.getAttribute('data-price'));
            card.style.display = price <= max ? 'block' : 'none';
        });
    });
}

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    checkAuthenticationAndInit();
    setupPriceFilter();
});

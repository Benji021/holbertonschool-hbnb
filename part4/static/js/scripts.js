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

// Part 1 : Login

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

// Part 2 : Index

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

// Part 3: Place Details

function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    const params = new URLSearchParams(window.location.search);
    return params.get('place_id');
}
// Calls the function and checks whether the place_id is present
const place_id = getPlaceIdFromURL();
    if (place_id) {
    console.log("Place ID found :", place_Id);
}   else {
    console.warn("place_id not found in URL");
}

// Check User Authentication
function checkAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        // Store the token for later use
        fetchPlaceDetails(token, placeId);
    }
}

function getCookie(name) {
    // Function to get a cookie value by its name
    const cookies = document.cookies.split(';');
    for (let cookie of cookies) {
        // Delete spaces
        cookies = cookie.trim();
        // Check if the cookie starts with the name
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
}

// Fetch place details

async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details and Include the token in the Authorization header
    try {
        const response = await fetch(`http://localhost:5000/api/places/${placeId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            throw new Error('Error retrieving location details');
        }

        const data = await response.json();
        displayPlaceDetails(data); // Calling up the display function
    } catch (error) {
        console.error('Erreur :', error.message);
    }
}

    // Handle the response and pass the data to displayPlaceDetails function
function displayPlaceDetails(place) {
    const container = document.getElementById('place-details');
    container.innerHTML = ''; // Clear previous content

    // Name
    const name = document.createElement('h2');
    name.textContent = place.name;

    // Description
    const description = document.createElement('p');
    description.textContent = place.description;

    // Price
    const price = document.createElement('p');
    price.textContent = `Price: ${place.price_per_night}€ by night`;

    // Amenities
    const amenities = document.createElement('h3');
    amenities.textContent = 'Amenities:';

    const amenitiesList = document.createElement('ul');
    place.amenities.forEach(amenity => {
        const item = document.createElement('li');
        item.textContent = amenity;
        amenitiesList.appendChild(item);
    })

    // Reviews
    const reviews = document.createElement('h3');
    reviews.textContent = 'Reviews:';

    const reviewsList = document.createElement('ul');
    place.reviews.forEach(review => {
        const item = document.createElement('li');
        item.textContent = `${review.user_name}: ${review.text}`;
        reviewsList.appendChild(item);
    });

    // Append all elements to the container
    container.appendChild(name);
    container.appendChild(description);
    container.appendChild(price);
    container.appendChild(amenities);
    container.appendChild(amenitiesList);
    container.appendChild(reviews);
    container.appendChild(reviewsList);
}

// Part 4 : Add Review

// Check User Authentication
function checkAuthentication() {
    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
    }
    return token;
}

function getCookie(name) {
    // Function to get a cookie value by its name
    const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
    if (match) {
        return match[2];  // Return Cookie Value
    }
    return null;  // If the cookie does not exist, returns null
}

// Get place ID from URL
function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    const params = new URLSearchParams(window.location.search);
    return params.get('place_Id');  // Returns the value of the 'placeId' parameter
}

// Setup event listener for review form
document.addEventListener('DOMContentLoaded', () => {
    const reviewForm = document.getElementById('review-form');
    const token = checkAuthentication();
    const placeId = getPlaceIdFromURL();

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // Get review text from form
            const reviewText = document.getElementById('review-text').value;

            // Préparer les données à envoyer dans la requête
            const reviewData = {
                review: reviewText,
                placeId: placeId,
            };

            try {
                // Make AJAX request to submit review
                const response = await fetch('/api/reviews', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`,
                    },
                    body: JSON.stringify(reviewData),
                });

                // Handle the response
                if (response.ok) {
                    const data = await response.json();
                    console.log('Review submitted:', data);
                } else {
                    console.error('Failed to submit review');
                }
            } catch (error) {
                console.error('Error during submission:', error);
            }
        });
    }
});

// Make AJAX request to submit review
async function submitReview(token, placeId, reviewText) {
    // Make a POST request to submit review data
    // Include the token in the Authorization header
    // Send placeId and reviewText in the request body
    try {
        const response = await fetch('YOUR_ENDPOINT_URL', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`  // Add JWT token to Authorization header
            },
            body: JSON.stringify({
                place_id: placeId,
                review_text: reviewText
            })
        });

        // Handle the response
        if (!response.ok) {
            throw new Error('Failed to submit review');
        }

        const result = await response.json();  // Processing the response in JSON
        console.log('Review submitted successfully:', result);
    } catch (error) {
        console.error('Error submitting review:', error);
    }
}

// Handle API response
function handleResponse(response) {
    if (response.ok) {
        alert('Review submitted successfully!');
        // Clear the form
    } else {
        alert('Failed to submit review');
    }
}
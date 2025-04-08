/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    // Simulates data retrieved from an API
    const place = {
      id: 1,
      name: "Villa au bord de mer",
      host: "Jean Dupont",
      price_per_night: 120,
      description: "Charming villa overlooking the Mediterranean Sea, ideal for relaxing",
      amenities: ["Wi-Fi", "Piscine", "Cuisine équipée", "Climatisation"]
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

  displayPlaceDetails(place);
  displayReviews(reviews);
});

function displayPlaceDetails(place) {
  const section = document.getElementById("place-details");
  section.classList.add("place-details");

  section.innerHTML = `
      <h2>${place.name}</h2>
      <div class="place-info">
          <p><strong>Hôte :</strong> ${place.host}</p>
          <p><strong>Prix par nuit :</strong> ${place.price_per_night}€</p>
          <p><strong>Description :</strong> ${place.description}</p>
          <p><strong>Commodités :</strong> ${place.amenities.join(", ")}</p>
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
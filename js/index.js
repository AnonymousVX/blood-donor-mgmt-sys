
// ==============================
// FAQ toggle functionality
// ==============================
document.querySelectorAll('.faq-question').forEach(button => {
  button.addEventListener('click', () => {
    const answer = button.nextElementSibling;

    // Toggle visibility
    answer.style.display = (answer.style.display === 'block') ? 'none' : 'block';
  });
});

// ==============================
// Donor search functionality
// ==============================
document.addEventListener("DOMContentLoaded", function () {
  const searchForm = document.getElementById("searchForm");
  const searchResults = document.getElementById("searchResults");

  searchForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const bloodGroup = searchForm.bloodGroup.value;
    const location = searchForm.location.value;

    if (!bloodGroup || !location) {
      searchResults.innerHTML = "<p>Please select a blood group and enter a location.</p>";
      return;
    }

    // ✅ Call backend API on Render
    fetch(`https://blood-donor-mgmt-sys.onrender.com/api/donors?city=${encodeURIComponent(location)}`)
      .then(res => res.json())
      .then(data => {
        // Filter results by blood group
        const filtered = data.filter(donor => donor.bloodgroup === bloodGroup);

        if (filtered.length === 0) {
          searchResults.innerHTML = "<p>No matching donors found.</p>";
          return;
        }

        // Display results
        searchResults.innerHTML = "<h3>Matching Donors</h3>";
        filtered.forEach(donor => {
          const donorCard = document.createElement("div");
          donorCard.classList.add("donor-card");
          donorCard.innerHTML = `
            <p><strong>Name:</strong> ${donor.name}</p>
            <p><strong>Blood Group:</strong> ${donor.bloodgroup}</p>
            <p><strong>Contact:</strong> ${donor.contact}</p>
          `;
          searchResults.appendChild(donorCard);
        });
      })
      .catch(err => {
        console.error("Error fetching donors:", err);
        searchResults.innerHTML = "<p>❌ Error fetching donors. Please try again later.</p>";
      });
  });
});


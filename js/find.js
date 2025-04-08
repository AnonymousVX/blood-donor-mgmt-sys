
// js/find.js

document.addEventListener('DOMContentLoaded', () => {
  const citySelect = document.getElementById('citySelect');
  const donorResults = document.getElementById('donorResults');

  // Load cities from backend
  fetch('https://blood-donor-mgmt-sys.onrender.com/api/cities')   
    .then(res => res.json())
    .then(cities => {
      cities.forEach(city => {
        const option = document.createElement('option');
        option.value = city;
        option.textContent = city;
        citySelect.appendChild(option);
      });
    });

  // Fetch donors when city changes
  citySelect.addEventListener('change', () => {
    const selectedCity = citySelect.value;
    if (!selectedCity) {
      donorResults.innerHTML = '';
      return;
    }

    fetch(`https://blood-donor-mgmt-sys.onrender.com/api/donors?city=${encodeURIComponent(selectedCity)}`)      
      .then(res => res.json())
      .then(donors => {
        donorResults.innerHTML = '<h3>Matching Donors:</h3>';
        if (donors.length === 0) {
          donorResults.innerHTML += '<p>No donors found for this city.</p>';
        } else {
          donors.forEach(donor => {
            donorResults.innerHTML += `
              <div class="donor-card">
                <p><strong>Name:</strong> ${donor.name}</p>
                <p><strong>Blood Group:</strong> ${donor.bloodgroup}</p>
                <p><strong>Contact:</strong> ${donor.contact}</p>
              </div>
            `;
          });
        }
      });
  });
});

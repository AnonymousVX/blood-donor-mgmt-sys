
document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');

  form.addEventListener('submit', (e) => {
    e.preventDefault(); // Stop form from submitting normally

    const name = form.name.value.trim();
    const age = form.age.value.trim();
    const gender = form.gender.value;
    const bloodGroup = form.bloodGroup.value; // ✅ FIXED this line
    const contact = form.contact.value.trim();
    const city = form.city.value.trim();

    // Validate fields
    if (!name || !age || !gender || !bloodGroup || !contact || !city) {
      alert("❌ Please fill in all the fields.");
      return;
    }

    if (isNaN(age) || age < 18 || age > 65) {
      alert("⚠️ Age must be a number between 18 and 65.");
      return;
    }

    if (!/^\d{10}$/.test(contact)) {
      alert("📱 Contact number must be 10 digits.");
      return;
    }

    // Send data to Flask API
    
fetch('https://blood-donor-mgmt-sys.onrender.com/register', {

      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: name,
        age: parseInt(age), // ✅ convert to number before sending
        gender: gender,
        bloodgroup: bloodGroup, // ✅ This should match your Flask field
        contact: contact,
        city: city
      })
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Server returned an error!');
        }
        return response.json();
      })
      .then(data => {
        alert(`✅ Thank you, ${name}! Your details have been recorded.`);
        form.reset(); // Clear form on success
      })
      .catch(error => {
        console.error('Error submitting form:', error);
        alert("❌ Failed to submit data. Please try again later.");
      });
  });
});


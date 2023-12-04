var currentTab = 0;

showTab(currentTab);

function showTab(n) {
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";

  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == x.length - 1) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  fixStepIndicator(n);
}

// healthform.js

function next(n) {
  var x = document.getElementsByClassName("tab");

  // Assuming you have form elements with specific IDs
  var gender = $("#gender").val();
  var age = $("#age").val();
  var country = $("#country").val();
  var allergies = $("#allergies").val();
  var likes = $("#likes").val();

  // Assuming you have a CSRF token in your form
  var csrf_token = $("input[name=csrf_token]").val();

  // You can add more form data as needed

  // Create an object to store the form data
  var formData = {
    gender: gender,
    age: age,
    country: country,
    allergies: allergies,
    likes: likes,
    // csrf_token: csrf_token,
  };

  // Assuming you have a CSRF token in your form
  // var csrf_token = $("input[name=csrf_token]").val();

  // Create an object to store all user data
  var userData = {
    gender: gender,
    age: age,
    country: country,
    allergies: allergies,
    likes: likes,
    csrf_token: csrf_token,
  };

  x[currentTab].style.display = "none";

  currentTab = currentTab + n;

  if (currentTab >= x.length) {
    // Check if the current tab is the last one
    // If true, send the AJAX request
    if (n === 1) {
      // Make a POST request using jQuery AJAX
      $.ajax({
        type: "POST",
        url: "/setPreferences", // Update the URL to your actual endpoint
        data: JSON.stringify({ userData: userData }),
        contentType: "application/json; charset=utf-8",
        success: function (response) {
          // Handle success (if needed)
          console.log(userData);

          console.log("Form submitted successfully");

          // Redirect to the new page
          window.location.href = "/dashboard"; // Update the URL to your desired page
        },
        error: function (error) {
          // Handle error (if needed)
          console.log(userData);
          console.error("Error submitting form", error);
        },
      });
    }
    return false;
  }

  showTab(currentTab);
}

function fixStepIndicator(n) {
  var i,
    x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }

  x[n].className += " active";
}

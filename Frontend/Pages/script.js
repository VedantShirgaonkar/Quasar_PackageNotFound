function toggleForm() {
  document.getElementById("login-card").classList.toggle("hidden");
  document.getElementById("signup-card").classList.toggle("hidden");
}

function closeContainer() {
  document.getElementById("auth-container").style.display = "none";
}

function validateForm() {
  let valid = true;
  document.getElementById("nameError").innerText = "";
  document.getElementById("passwordError").innerText = "";
  document.getElementById("confirmpasswordError").innerText = "";

  const name = document.getElementById("signup-username").value;

  const password = document.getElementById("signup-password").value;
  const confirmpassword = document.getElementById("signup-confirm-password").value;
  document.getElementById("signup-password").classList.add("input-error");
  valid = false;

  if (name.length < 3 || name.length > 25) {
    document.getElementById("nameError").innerText =
      "Username must be between 3 and 25 characters.";
    valid = false;

    document.getElementById("signup-username").style.border = "1px solid red";
  } else {
    document.getElementById("signup-username").style.border = "1px solid green";
  }

  const pw = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[\W_]).{8,}$/;

  if (!pw.test(password)) {
    document.getElementById("passwordError").innerText =
      "Password must be at least 8 characters that include atleast 1 lowercase character, 1 uppercase character, 1 number and 1 special character(!@#$%^&*).";
    valid = false;
    document.getElementById("signup-password").style.border = "1px solid red";
  } else {
    document.getElementById("signup-password").style.border = "1px solid green";
  }

  if (confirmpassword != password || confirmpassword == "") {
    document.getElementById("confirmpasswordError").innerText =
      "Please enter the password again.";
    valid = false;
    document.getElementById("signup-confirm-password").style.border = "1px solid red";
  } else {
    document.getElementById("signup-confirm-password").style.border = "1px solid green";
  }

  return valid;
}

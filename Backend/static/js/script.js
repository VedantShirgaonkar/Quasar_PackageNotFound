function toggleForm() {
  document.getElementById("login-card").classList.toggle("hidden");
  document.getElementById("signup-card").classList.toggle("hidden");
}

function closeContainer() {
  document.getElementById("auth-container").style.display = "none";
}

function validate_submitForm() {
  let valid = true;
  document.getElementById("nameError").innerText = "";
  document.getElementById("passwordError").innerText = "";
  document.getElementById("confirmpasswordError").innerText = "";

  const name = document.getElementById("signup-username").value.toLowerCase();

  const password = document.getElementById("signup-password").value;
  const confirmpassword = document.getElementById("signup-confirm-password").value;
  const role = document.querySelector('input[name="role"]:checked').value;
  document.getElementById("signup-password").classList.add("input-error");
  

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

  if (role == "") {
    document.getElementById("roleError").innerText = "Please select a role.";
    valid = false;
  }

  if (valid) {
    signup(name, password, confirmpassword, role);
  }
  else{
    return false;
  }

}

const signup = async (username, password, confirmPassword, role) => {
  const apiUrl = "http://127.0.0.1:3000/signup";

  const requestBody = {
      username,
      password,
      confirmPassword,
      role
  };

  try {
      const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify(requestBody)
      });

      const result = await response.json();

      if (response.ok) {
          console.log("Signup successful:", result);
          alert('Sigup SUccessful, Please login to continue');
          window.location.href = "/";
      } else {
          console.error("Signup failed:", result);
          alert("Signup Failure, user id already exist. Please try again later");
      }
  } catch (error) {
      console.error("Error during signup:", error);
  }
};

function validate_login() {
  let valid = true;
  document.getElementById("nameError").innerText = "";
  document.getElementById("passwordError").innerText = "";


  const name = document.getElementById("login-username").value.toLowerCase();

  const password = document.getElementById("login-password").value;
  document.getElementById("login-password").classList.add("input-error");
  

  if (name.length < 3 || name.length > 25) {
    document.getElementById("nameError").innerText =
      "Username must be between 3 and 25 characters.";
    valid = false;

    document.getElementById("login-username").style.border = "1px solid red";
  } else {
    document.getElementById("login-username").style.border = "1px solid green";
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


  if (valid) {
    login(name, password);
  }
  else{
    return false;
  }

}

const login = async (username, password) => {
  const apiUrl = "http://127.0.0.1:3000/login";

  const requestBody = {
      username,
      password
  };

  try {
      const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify(requestBody)
      });

      const result = await response.json();

      if (response.ok) {
          console.log("Login successful:", result);
          alert("Login Successful, Redirecting...");

          window.location.href = "/Student_dashboard?rnd=" 
      } else {
          console.error("Login failed:", result);
          alert("Login Failed, Invalid Credentials. Please try again.");
      }
  } catch (error) {
      console.error("Error during login:", error);
  }
};








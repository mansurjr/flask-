console.log("JavaScript is loaded!");

document.addEventListener("DOMContentLoaded", function() {
    let toggleButton = document.getElementById("togglePassword");
    let passwordField = document.getElementById("password");

    if (toggleButton && passwordField) {
        toggleButton.addEventListener("click", function() {
            if (passwordField.type === "password") {
                passwordField.type = "text";
                this.innerHTML = "🙈"; 
            } else {
                passwordField.type = "password";
                this.innerHTML = "🙉"; 
            }
        });
    } else {
        console.error("Element not found: Check if the IDs are correct.");
    }
});

document.getElementById("togglePassword").addEventListener("click", function() {
    let passwordField = document.getElementById("password");
    if (passwordField.type === "password") {
        passwordField.type = "text";
        this.innerHTML = "🙈"; 
    } else {
        passwordField.type = "password";
        this.innerHTML = "🙉"; 
    }
});

const messege = document.getElementById("id")


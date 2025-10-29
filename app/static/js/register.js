document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");
    const errorMsg = document.getElementById("errorMsg");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        errorMsg.textContent = "";

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const passwordRepeat = document.getElementById("passwordRepeat").value;

        if (password !== passwordRepeat) {
            errorMsg.textContent = "Пароли не совпадают!";
            return;
        }

        try {
            const response = await fetch("/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (!response.ok) {
                errorMsg.textContent = data.detail || "Ошибка регистрации";
            } else {
                alert("Регистрация успешна! Войдите.");
                window.location.href = "/login";
            }
        } catch (err) {
            errorMsg.textContent = "Ошибка сети";
            console.error(err);
        }
    });
});
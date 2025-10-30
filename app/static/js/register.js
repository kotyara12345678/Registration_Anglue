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
                credentials: "include", // важно для работы с куки
                body: JSON.stringify({
                    email,
                    password,
                    password_repeat: passwordRepeat
                })
            });

            const data = await response.json();

            if (!response.ok) {

                if (typeof data.detail === "object") {
                    errorMsg.textContent = JSON.stringify(data.detail);
                } else {
                    errorMsg.textContent = data.detail || "Ошибка регистрации";
                }
            } else {
                alert("Регистрация успешна! Теперь можно войти.");
                window.location.href = "/";
            }
        } catch (err) {
            errorMsg.textContent = "Ошибка сети";
            console.error(err);
        }
    });
});
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const errorMsg = document.getElementById("errorMsg");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        errorMsg.textContent = "";

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                credentials: "include",
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();

            if (!response.ok) {

                if (typeof data.detail === "object") {
                    errorMsg.textContent = JSON.stringify(data.detail);
                } else {
                    errorMsg.textContent = data.detail || "Ошибка входа";
                }
            } else {

                window.location.href = "/protected";
            }
        } catch (err) {
            errorMsg.textContent = "Ошибка сети";
            console.error(err);
        }
    });
});
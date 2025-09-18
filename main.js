document.getElementById("feedbackForm").addEventListener("submit", async function(e) {
  e.preventDefault(); // не перезагружаем страницу сразу

  const message = document.getElementById("message").value.trim();

  if (!message) {
    alert("Please write something before sending.");
    return;
  }

  try {
    // отправляем POST-запрос на сервер
    const response = await fetch("http://127.0.0.1:5000/process-message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: message })
    });

    const data = await response.json(); // читаем JSON {emotion: "...", prompt: "..."}

    // сохраняем в localStorage, чтобы показать на ready.html
    localStorage.setItem("emotion", data.emotion);
    localStorage.setItem("prompt", data.prompt);


    // переход на страницу с результатом
    window.location.href = "ready.html";

  } catch (error) {
    console.error("Error:", error);
    alert("Something went wrong. Please try again later.");
  }
});

// ===== Enter вместо кнопки Send =====
const textarea = document.getElementById("message");
const sendBtn = document.querySelector(".send-btn");

textarea.addEventListener("keydown", function(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault(); // отменяем перенос строки
    
    // анимация кнопки Send
    sendBtn.classList.add("active");
    setTimeout(() => sendBtn.classList.remove("active"), 150);

    // отправка формы
    document.getElementById("feedbackForm").dispatchEvent(
      new Event("submit", { cancelable: true, bubbles: true })
    );
  }
});

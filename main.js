document.getElementById("feedbackForm").addEventListener("submit", async function(e) {
  e.preventDefault(); // не перезагружаем страницу сразу

  const message = document.getElementById("message").value.trim();

  if (!message) {
    alert("Please write something before sending.");
    return;
  }

  try {
    // отправляем POST-запрос на сервер
    await fetch("/process-message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ text: message })
    });

    // если всё ок → переходим на другую страницу
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

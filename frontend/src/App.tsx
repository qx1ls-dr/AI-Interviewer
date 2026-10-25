import { useEffect, useState } from "react";

// Стартовая страница: проверяет, что сервер отвечает.
// Чат респондента, конструктор опроса и дашборд появятся на этапе «Рабочий проект».
export default function App() {
  const [status, setStatus] = useState("проверяем…");

  useEffect(() => {
    fetch("/api/health")
      .then((response) => response.json())
      .then((data) => setStatus(`работает, версия ${data.version}`))
      .catch(() => setStatus("не отвечает"));
  }, []);

  return (
    <main className="main">
      <h1>AI-интервьюер</h1>
      <p>Платформа динамических опросов студентов.</p>
      <p className="muted">Сервер: {status}</p>
    </main>
  );
}

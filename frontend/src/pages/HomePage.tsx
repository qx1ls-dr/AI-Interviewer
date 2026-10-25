import { useEffect, useState } from "react";
import { getHealth, type Health } from "../api/client";

export default function HomePage() {
  const [health, setHealth] = useState<Health | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getHealth().then(setHealth).catch((e: Error) => setError(e.message));
  }, []);

  return (
    <section>
      <h1>Платформа динамических опросов</h1>
      <p>Каркас приложения. Вход организатора и конструктор опроса появятся на этапе 3.1–3.3.</p>
      <p className="muted">
        Сервер:{" "}
        {health
          ? `работает, версия ${health.version}${health.dev_mode ? ", режим разработки" : ""}`
          : (error ?? "проверяем…")}
      </p>
    </section>
  );
}

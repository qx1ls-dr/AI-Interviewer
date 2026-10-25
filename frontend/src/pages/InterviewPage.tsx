import { useParams } from "react-router-dom";

export default function InterviewPage() {
  const { token } = useParams();
  return (
    <section>
      <h1>Интервью</h1>
      <p>Здесь будет согласие на обработку ПДн и чат с интервьюером.</p>
      <p className="muted">Приглашение: {token}</p>
    </section>
  );
}

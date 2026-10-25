import { Link, Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import InterviewPage from "./pages/InterviewPage";
import DashboardPage from "./pages/DashboardPage";

export default function App() {
  return (
    <>
      <header className="header">
        <Link to="/">AI-интервьюер</Link>
        <nav>
          <Link to="/dashboard">Дашборд (демо)</Link>
        </nav>
      </header>
      <main className="main">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/i/:token" element={<InterviewPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </main>
    </>
  );
}

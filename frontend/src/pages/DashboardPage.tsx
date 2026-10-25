import ReactECharts from "echarts-for-react";

// Синтетические данные для макета. Реальные числа считает сервер запросами к БД.
const themes = [
  { name: "Сроки выдачи заданий", share: 0.62 },
  { name: "Качество лекций", share: 0.48 },
  { name: "Обратная связь по работам", share: 0.35 },
  { name: "Прочее", share: 0.12 },
];

export default function DashboardPage() {
  const option = {
    grid: { left: 200, right: 24, top: 16, bottom: 24 },
    xAxis: { type: "value", max: 1, axisLabel: { formatter: (v: number) => `${v * 100}%` } },
    yAxis: { type: "category", data: themes.map((t) => t.name).reverse() },
    series: [{ type: "bar", data: themes.map((t) => t.share).reverse() }],
    tooltip: { trigger: "axis" },
  };

  return (
    <section>
      <h1>Дашборд опроса (демо)</h1>
      <p className="muted">Доля уникальных респондентов по темам, синтетические данные.</p>
      <ReactECharts option={option} style={{ height: 280 }} />
    </section>
  );
}

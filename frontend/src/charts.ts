// Подключаем только нужные части ECharts, а не всю библиотеку: так бандл в разы меньше.
// Новый тип графика или компонент регистрируйте здесь.
import * as echarts from "echarts/core";
import { BarChart } from "echarts/charts";
import { GridComponent, TooltipComponent } from "echarts/components";
import { CanvasRenderer } from "echarts/renderers";

echarts.use([BarChart, GridComponent, TooltipComponent, CanvasRenderer]);

export { echarts };

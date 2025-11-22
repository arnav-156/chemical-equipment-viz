import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Bar, Line, Pie } from 'react-chartjs-2';
import './Charts.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Tooltip,
  Legend
);

const Charts = ({ summary, equipmentData }) => {
  if (!summary || !equipmentData) {
    return null;
  }

  // Equipment Type Distribution (Bar Chart)
  const typeDistribution = summary.type_distribution || {};
  const typeChartData = {
    labels: Object.keys(typeDistribution),
    datasets: [
      {
        label: 'Equipment Count',
        data: Object.values(typeDistribution),
        backgroundColor: 'rgba(102, 126, 234, 0.8)',
        borderColor: 'rgba(102, 126, 234, 1)',
        borderWidth: 2,
      },
    ],
  };

  // Parameter Trends (Line Chart)
  const parameterData = {
    labels: equipmentData.map((item) => item.name),
    datasets: [
      {
        label: 'Flowrate',
        data: equipmentData.map((item) => item.flowrate),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.4,
      },
      {
        label: 'Pressure',
        data: equipmentData.map((item) => item.pressure),
        borderColor: 'rgb(255, 159, 64)',
        backgroundColor: 'rgba(255, 159, 64, 0.2)',
        tension: 0.4,
      },
      {
        label: 'Temperature',
        data: equipmentData.map((item) => item.temperature),
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        tension: 0.4,
      },
    ],
  };

  // Type Distribution Pie Chart
  const pieChartData = {
    labels: Object.keys(typeDistribution),
    datasets: [
      {
        data: Object.values(typeDistribution),
        backgroundColor: [
          'rgba(102, 126, 234, 0.8)',
          'rgba(118, 75, 162, 0.8)',
          'rgba(75, 192, 192, 0.8)',
          'rgba(255, 159, 64, 0.8)',
          'rgba(255, 99, 132, 0.8)',
          'rgba(54, 162, 235, 0.8)',
          'rgba(153, 102, 255, 0.8)',
        ],
        borderColor: [
          'rgba(102, 126, 234, 1)',
          'rgba(118, 75, 162, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(255, 159, 64, 1)',
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(153, 102, 255, 1)',
        ],
        borderWidth: 2,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
    },
  };

  return (
    <div className="charts-container">
      <div className="chart-box">
        <h3>📊 Equipment Type Distribution</h3>
        <div className="chart-wrapper">
          <Bar data={typeChartData} options={chartOptions} />
        </div>
      </div>

      <div className="chart-box">
        <h3>📈 Parameter Trends</h3>
        <div className="chart-wrapper">
          <Line data={parameterData} options={chartOptions} />
        </div>
      </div>

      <div className="chart-box">
        <h3>🥧 Type Distribution (Pie)</h3>
        <div className="chart-wrapper">
          <Pie data={pieChartData} options={chartOptions} />
        </div>
      </div>
    </div>
  );
};

export default Charts;

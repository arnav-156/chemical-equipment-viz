import React from 'react';
import './SummaryCards.css';

const SummaryCards = ({ summary }) => {
  if (!summary) {
    return null;
  }

  const cards = [
    {
      title: 'Total Equipment',
      value: summary.total_count,
      icon: '📦',
      color: '#667eea',
    },
    {
      title: 'Avg Flowrate',
      value: summary.avg_flowrate?.toFixed(2),
      range: `${summary.min_flowrate?.toFixed(1)} - ${summary.max_flowrate?.toFixed(1)}`,
      icon: '💧',
      color: '#4caf50',
    },
    {
      title: 'Avg Pressure',
      value: summary.avg_pressure?.toFixed(2),
      range: `${summary.min_pressure?.toFixed(1)} - ${summary.max_pressure?.toFixed(1)}`,
      icon: '⚡',
      color: '#ff9800',
    },
    {
      title: 'Avg Temperature',
      value: summary.avg_temperature?.toFixed(2),
      range: `${summary.min_temperature?.toFixed(1)} - ${summary.max_temperature?.toFixed(1)}`,
      icon: '🌡️',
      color: '#f44336',
    },
  ];

  return (
    <div className="summary-cards">
      {cards.map((card, index) => (
        <div key={index} className="summary-card" style={{ borderTopColor: card.color }}>
          <div className="card-icon" style={{ color: card.color }}>
            {card.icon}
          </div>
          <div className="card-content">
            <h3>{card.title}</h3>
            <p className="card-value">{card.value}</p>
            {card.range && <p className="card-range">Range: {card.range}</p>}
          </div>
        </div>
      ))}
    </div>
  );
};

export default SummaryCards;

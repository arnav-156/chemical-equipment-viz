import React from 'react';
import './AuroraSimple.css';

const AuroraSimple = ({ colorStops = ["#3A29FF", "#FF94B4", "#FF3232"] }) => {
  return (
    <div className="aurora-simple">
      <div className="aurora-gradient" style={{
        background: `linear-gradient(45deg, ${colorStops[0]}, ${colorStops[1]}, ${colorStops[2]})`
      }}></div>
      <div className="aurora-gradient aurora-gradient-2" style={{
        background: `linear-gradient(-45deg, ${colorStops[2]}, ${colorStops[1]}, ${colorStops[0]})`
      }}></div>
      <div className="aurora-gradient aurora-gradient-3" style={{
        background: `linear-gradient(90deg, ${colorStops[1]}, ${colorStops[0]}, ${colorStops[2]})`
      }}></div>
    </div>
  );
};

export default AuroraSimple;

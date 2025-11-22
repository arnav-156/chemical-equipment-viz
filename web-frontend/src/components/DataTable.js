import React from 'react';
import './DataTable.css';

const DataTable = ({ equipmentData }) => {
  if (!equipmentData || equipmentData.length === 0) {
    return null;
  }

  return (
    <div className="data-table-container">
      <h3>📋 Equipment Details</h3>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              <th>Equipment Name</th>
              <th>Type</th>
              <th>Flowrate</th>
              <th>Pressure</th>
              <th>Temperature</th>
            </tr>
          </thead>
          <tbody>
            {equipmentData.map((item, index) => (
              <tr key={item.id || index}>
                <td>{item.name}</td>
                <td>
                  <span className="type-badge">{item.type}</span>
                </td>
                <td>{item.flowrate.toFixed(2)}</td>
                <td>{item.pressure.toFixed(2)}</td>
                <td>{item.temperature.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataTable;

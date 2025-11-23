import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './EquipmentNetworkGraph.css';

const EquipmentNetworkGraph = ({ equipmentData }) => {
  const svgRef = useRef(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [hoveredNode, setHoveredNode] = useState(null);

  useEffect(() => {
    if (!equipmentData || equipmentData.length === 0) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = svgRef.current.clientWidth;
    const height = svgRef.current.clientHeight;

    // Create nodes from equipment data
    const nodes = equipmentData.map((item, i) => ({
      id: item.id || i,
      name: item.equipment_name,
      type: item.equipment_type,
      flowrate: item.flowrate || 0,
      pressure: item.pressure || 0,
      temperature: item.temperature || 0,
      efficiency: item.efficiency || 0,
      x: width / 2 + Math.random() * 100 - 50,
      y: height / 2 + Math.random() * 100 - 50
    }));

    // Create links based on equipment type relationships
    const links = [];
    nodes.forEach((source, i) => {
      nodes.forEach((target, j) => {
        if (i < j && Math.random() > 0.7) { // Random connections for demo
          links.push({
            source: source.id,
            target: target.id,
            value: Math.random() * 5 + 1
          });
        }
      });
    });

    // Color scale for equipment types
    const colorScale = d3.scaleOrdinal()
      .domain(['Reactor', 'Heat Exchanger', 'Pump', 'Distillation Column', 'Compressor'])
      .range(['#00FFA3', '#FF6B9D', '#FFD93D', '#6BCF7F', '#FF9F1C']);

    // Size scale based on flowrate
    const sizeScale = d3.scaleLinear()
      .domain([0, d3.max(nodes, d => d.flowrate)])
      .range([8, 25]);

    // Create force simulation
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(d => sizeScale(d.flowrate) + 5));

    // Create container group
    const g = svg.append('g');

    // Add zoom behavior
    const zoom = d3.zoom()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Draw links
    const link = g.append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('class', 'network-link')
      .attr('stroke', 'rgba(0, 255, 163, 0.2)')
      .attr('stroke-width', d => d.value);

    // Draw nodes
    const node = g.append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')
      .attr('class', 'network-node')
      .call(d3.drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended));

    // Node circles
    node.append('circle')
      .attr('r', d => sizeScale(d.flowrate))
      .attr('fill', d => colorScale(d.type))
      .attr('stroke', '#0A0E27')
      .attr('stroke-width', 2)
      .style('filter', 'drop-shadow(0 0 10px rgba(0, 255, 163, 0.5))');

    // Node labels
    node.append('text')
      .text(d => d.name)
      .attr('x', 0)
      .attr('y', d => sizeScale(d.flowrate) + 15)
      .attr('text-anchor', 'middle')
      .attr('class', 'node-label')
      .style('fill', '#8B95C9')
      .style('font-size', '11px')
      .style('font-family', 'Inter, sans-serif')
      .style('pointer-events', 'none');

    // Node interactions
    node.on('mouseenter', function(event, d) {
      setHoveredNode(d);
      d3.select(this).select('circle')
        .transition()
        .duration(200)
        .attr('r', sizeScale(d.flowrate) * 1.3)
        .style('filter', 'drop-shadow(0 0 20px rgba(0, 255, 163, 0.8))');

      // Highlight connected links
      link.style('stroke', l => 
        (l.source.id === d.id || l.target.id === d.id) 
          ? 'rgba(0, 255, 163, 0.8)' 
          : 'rgba(0, 255, 163, 0.1)'
      ).style('stroke-width', l =>
        (l.source.id === d.id || l.target.id === d.id) 
          ? l.value * 2 
          : l.value
      );
    });

    node.on('mouseleave', function(event, d) {
      setHoveredNode(null);
      d3.select(this).select('circle')
        .transition()
        .duration(200)
        .attr('r', sizeScale(d.flowrate))
        .style('filter', 'drop-shadow(0 0 10px rgba(0, 255, 163, 0.5))');

      // Reset links
      link.style('stroke', 'rgba(0, 255, 163, 0.2)')
        .style('stroke-width', l => l.value);
    });

    node.on('click', function(event, d) {
      setSelectedNode(d);
    });

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node.attr('transform', d => `translate(${d.x},${d.y})`);
    });

    // Drag functions
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    return () => {
      simulation.stop();
    };
  }, [equipmentData]);

  return (
    <div className="network-graph-container">
      <div className="network-graph-header">
        <h3>🕸️ Equipment Network</h3>
        <p className="network-hint">Drag nodes • Scroll to zoom • Click to select</p>
      </div>
      
      <svg ref={svgRef} className="network-graph-svg"></svg>

      {hoveredNode && (
        <div className="network-tooltip">
          <h4>{hoveredNode.name}</h4>
          <div className="tooltip-grid">
            <span className="tooltip-label">Type:</span>
            <span className="tooltip-value">{hoveredNode.type}</span>
            <span className="tooltip-label">Flowrate:</span>
            <span className="tooltip-value">{hoveredNode.flowrate.toFixed(2)}</span>
            <span className="tooltip-label">Pressure:</span>
            <span className="tooltip-value">{hoveredNode.pressure.toFixed(2)}</span>
            <span className="tooltip-label">Temp:</span>
            <span className="tooltip-value">{hoveredNode.temperature.toFixed(2)}°C</span>
          </div>
        </div>
      )}

      {selectedNode && (
        <div className="network-details">
          <button 
            className="close-details"
            onClick={() => setSelectedNode(null)}
          >
            ✕
          </button>
          <h4>📊 {selectedNode.name}</h4>
          <div className="details-content">
            <div className="detail-item">
              <span className="detail-label">Equipment Type</span>
              <span className="detail-value">{selectedNode.type}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Flowrate</span>
              <span className="detail-value">{selectedNode.flowrate.toFixed(2)} m³/h</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Pressure</span>
              <span className="detail-value">{selectedNode.pressure.toFixed(2)} bar</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Temperature</span>
              <span className="detail-value">{selectedNode.temperature.toFixed(2)}°C</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Efficiency</span>
              <span className="detail-value">{selectedNode.efficiency.toFixed(1)}%</span>
            </div>
          </div>
        </div>
      )}

      <div className="network-legend">
        <h5>Equipment Types</h5>
        <div className="legend-item">
          <span className="legend-dot" style={{background: '#00FFA3'}}></span>
          <span>Reactor</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot" style={{background: '#FF6B9D'}}></span>
          <span>Heat Exchanger</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot" style={{background: '#FFD93D'}}></span>
          <span>Pump</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot" style={{background: '#6BCF7F'}}></span>
          <span>Distillation Column</span>
        </div>
        <div className="legend-item">
          <span className="legend-dot" style={{background: '#FF9F1C'}}></span>
          <span>Compressor</span>
        </div>
      </div>
    </div>
  );
};

export default EquipmentNetworkGraph;

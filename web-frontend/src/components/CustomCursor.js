import { useEffect, useRef, useState } from 'react';
import './CustomCursor.css';

const CustomCursor = () => {
  const cursorRef = useRef(null);
  const trailRef = useRef([]);
  const [cursorType, setCursorType] = useState('default');
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const cursor = cursorRef.current;
    if (!cursor) return;

    let mouseX = 0;
    let mouseY = 0;
    let cursorX = 0;
    let cursorY = 0;

    const handleMouseMove = (e) => {
      mouseX = e.clientX;
      mouseY = e.clientY;

      // Check context for cursor type
      const target = e.target;
      if (target.closest('.upload-zone')) {
        setCursorType('upload');
      } else if (target.closest('button, a, .clickable')) {
        setCursorType('pointer');
      } else if (target.closest('.data-point, canvas')) {
        setCursorType('crosshair');
      } else {
        setCursorType('default');
      }
    };

    const handleMouseEnter = () => setIsVisible(true);
    const handleMouseLeave = () => setIsVisible(false);

    const animateCursor = () => {
      // Smooth follow
      cursorX += (mouseX - cursorX) * 0.2;
      cursorY += (mouseY - cursorY) * 0.2;

      cursor.style.transform = `translate(${cursorX}px, ${cursorY}px)`;

      // Trail effect
      trailRef.current.push({ x: cursorX, y: cursorY, opacity: 1 });
      if (trailRef.current.length > 10) {
        trailRef.current.shift();
      }

      requestAnimationFrame(animateCursor);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseenter', handleMouseEnter);
    document.addEventListener('mouseleave', handleMouseLeave);
    
    animateCursor();

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseenter', handleMouseEnter);
      document.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  if (!isVisible) return null;

  return (
    <>
      <div 
        ref={cursorRef}
        className={`custom-cursor custom-cursor-${cursorType}`}
      >
        <div className="cursor-core"></div>
        <div className="cursor-ring"></div>
        {cursorType === 'upload' && (
          <div className="cursor-icon">↑</div>
        )}
        {cursorType === 'crosshair' && (
          <>
            <div className="crosshair-h"></div>
            <div className="crosshair-v"></div>
          </>
        )}
      </div>
    </>
  );
};

export default CustomCursor;

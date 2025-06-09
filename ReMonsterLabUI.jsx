import React, { useState, useEffect, useRef, useReducer } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Label } from '@/components/ui/label';
import { motion, AnimatePresence } from 'framer-motion';
import * as d3 from 'd3';
import { Loader2, AlertCircle } from 'lucide-react';

// CIE 1976 LAB color space calculations
const cie1976 = {
  // Constants
  Xn: 0.95047, // D65 illuminant
  Yn: 1.00000,
  Zn: 1.08883,
  k: 24389/27,
  e: 216/24389,

  // Helper function for f(t)
  f(t) {
    return t > this.e ? Math.pow(t, 1/3) : (this.k * t + 16) / 116;
  },

  // Convert XYZ to LAB
  xyzToLab(x, y, z) {
    const fx = this.f(x / this.Xn);
    const fy = this.f(y / this.Yn);
    const fz = this.f(z / this.Zn);

    const L = 116 * fy - 16;
    const a = 500 * (fx - fy);
    const b = 200 * (fy - fz);

    return { L, a, b };
  },

  // Convert LAB to XYZ
  labToXyz(L, a, b) {
    const fy = (L + 16) / 116;
    const fx = a / 500 + fy;
    const fz = fy - b / 200;

    const x = this.Xn * (fx > this.e ? Math.pow(fx, 3) : (116 * fx - 16) / this.k);
    const y = this.Yn * (fy > this.e ? Math.pow(fy, 3) : (116 * fy - 16) / this.k);
    const z = this.Zn * (fz > this.e ? Math.pow(fz, 3) : (116 * fz - 16) / this.k);

    return { x, y, z };
  },

  // Calculate chroma
  calculateChroma(a, b) {
    return Math.sqrt(a * a + b * b);
  },

  // Calculate hue angle
  calculateHueAngle(a, b) {
    return Math.atan2(b, a) * (180 / Math.PI);
  }
};

// State reducer
const reducer = (state, action) => {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, isLoading: true, error: null };
    case 'SET_ERROR':
      return { ...state, isLoading: false, error: action.payload };
    case 'SET_ANALYSIS':
      return { ...state, isLoading: false, error: null, analysis: action.payload };
    case 'SET_COLOR_SPACE':
      return { ...state, activeColorSpace: action.payload };
    default:
      return state;
  }
};

// Color space conversion utilities
const colorUtils = {
  labToHex: (L, a, b) => {
    const { x, y, z } = cie1976.labToXyz(L, a, b);
    return d3.rgb(
      d3.lab(L, a, b).rgb().r,
      d3.lab(L, a, b).rgb().g,
      d3.lab(L, a, b).rgb().b
    ).formatHex();
  },
  cmykToHex: (c, m, y, k) => {
    const r = 255 * (1 - c) * (1 - k);
    const g = 255 * (1 - m) * (1 - k);
    const b = 255 * (1 - y) * (1 - k);
    return d3.rgb(r, g, b).formatHex();
  }
};

export default function ReMonsterLabUI() {
  const [input, setInput] = useState('');
  const svgRef = useRef(null);
  
  const [state, dispatch] = useReducer(reducer, {
    isLoading: false,
    error: null,
    analysis: null,
    activeColorSpace: 'LAB'
  });

  const analyzeText = async () => {
    if (!input.trim()) {
      dispatch({ type: 'SET_ERROR', payload: 'Voer eerst tekst in' });
      return;
    }

    dispatch({ type: 'SET_LOADING' });
    
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000);

      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: input }),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      
      if (!validateAnalysisData(data)) {
        throw new Error('Invalid response data format');
      }
      
      dispatch({ type: 'SET_ANALYSIS', payload: data });
    } catch (error) {
      dispatch({ 
        type: 'SET_ERROR', 
        payload: error.name === 'AbortError' 
          ? 'Request timeout' 
          : error.message 
      });
    }
  };

  const validateAnalysisData = (data) => {
    return (
      data &&
      typeof data.rainbow_vector === 'string' &&
      data.rainbow_vector_lab &&
      typeof data.rainbow_vector_lab.L === 'number' &&
      typeof data.rainbow_vector_lab.a === 'number' &&
      typeof data.rainbow_vector_lab.b === 'number' &&
      Array.isArray(data.cmyk_vector) &&
      data.cmyk_vector.length === 4 &&
      data.cmyk_vector.every(v => typeof v === 'number') &&
      typeof data.dominant_emotions === 'object' &&
      typeof data.strategy === 'string'
    );
  };

  useEffect(() => {
    if (state.analysis && svgRef.current) {
      const svg = d3.select(svgRef.current);
      svg.selectAll('*').remove();

      const width = 300;
      const height = 300;
      const margin = { top: 20, right: 20, bottom: 30, left: 30 };
      const innerWidth = width - margin.left - margin.right;
      const innerHeight = height - margin.top - margin.bottom;

      const g = svg.append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

      if (state.activeColorSpace === 'LAB') {
        // LAB space visualization
        const x = d3.scaleLinear()
          .domain([-100, 100])
          .range([0, innerWidth]);
        const y = d3.scaleLinear()
          .domain([-100, 100])
          .range([innerHeight, 0]);

        // Add axes
        g.append('g')
          .attr('transform', `translate(0,${innerHeight})`)
          .call(d3.axisBottom(x).ticks(5))
          .append('text')
          .attr('x', innerWidth / 2)
          .attr('y', 25)
          .attr('fill', 'currentColor')
          .text('a* (green-red)');

        g.append('g')
          .call(d3.axisLeft(y).ticks(5))
          .append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', -25)
          .attr('x', -innerHeight / 2)
          .attr('fill', 'currentColor')
          .text('b* (blue-yellow)');

        // Draw LAB space grid with tooltips
        for (let a = -100; a <= 100; a += 5) {
          for (let b = -100; b <= 100; b += 5) {
            const color = colorUtils.labToHex(65, a, b);
            const chroma = cie1976.calculateChroma(a, b);
            const hueAngle = cie1976.calculateHueAngle(a, b);
            
            g.append('rect')
              .attr('x', x(a))
              .attr('y', y(b))
              .attr('width', 5)
              .attr('height', 5)
              .attr('fill', color)
              .append('title')
              .text(`L: 65, a: ${a}, b: ${b}\nChroma: ${chroma.toFixed(2)}\nHue: ${hueAngle.toFixed(2)}°`);
          }
        }

        // Plot current LAB dot
        const lab = state.analysis.rainbow_vector_lab;
        const chroma = cie1976.calculateChroma(lab.a, lab.b);
        const hueAngle = cie1976.calculateHueAngle(lab.a, lab.b);
        
        g.append('circle')
          .attr('cx', x(lab.a))
          .attr('cy', y(lab.b))
          .attr('r', 8)
          .attr('fill', colorUtils.labToHex(lab.L, lab.a, lab.b))
          .attr('stroke', '#000')
          .attr('stroke-width', 1.5)
          .append('title')
          .text(`Current:\nL: ${lab.L.toFixed(2)}\na: ${lab.a.toFixed(2)}\nb: ${lab.b.toFixed(2)}\nChroma: ${chroma.toFixed(2)}\nHue: ${hueAngle.toFixed(2)}°`);

        // Add chroma circles
        const chromaScale = d3.scaleLinear()
          .domain([0, 100])
          .range([0, innerWidth/2]);

        [25, 50, 75].forEach(c => {
          g.append('circle')
            .attr('cx', x(0))
            .attr('cy', y(0))
            .attr('r', chromaScale(c))
            .attr('fill', 'none')
            .attr('stroke', '#ccc')
            .attr('stroke-dasharray', '2,2')
            .append('title')
            .text(`Chroma: ${c}`);
        });
      } else {
        // CMYK space visualization
        const x = d3.scaleLinear()
          .domain([0, 1])
          .range([0, innerWidth]);
        const y = d3.scaleLinear()
          .domain([0, 1])
          .range([innerHeight, 0]);

        // Add axes
        g.append('g')
          .attr('transform', `translate(0,${innerHeight})`)
          .call(d3.axisBottom(x).ticks(5))
          .append('text')
          .attr('x', innerWidth / 2)
          .attr('y', 25)
          .attr('fill', 'currentColor')
          .text('Cyan');

        g.append('g')
          .call(d3.axisLeft(y).ticks(5))
          .append('text')
          .attr('transform', 'rotate(-90)')
          .attr('y', -25)
          .attr('x', -innerHeight / 2)
          .attr('fill', 'currentColor')
          .text('Magenta');

        // Draw CMYK space grid with tooltips
        for (let c = 0; c <= 1; c += 0.1) {
          for (let m = 0; m <= 1; m += 0.1) {
            const color = colorUtils.cmykToHex(c, m, state.analysis.cmyk_vector[2], state.analysis.cmyk_vector[3]);
            g.append('rect')
              .attr('x', x(c))
              .attr('y', y(m))
              .attr('width', innerWidth/10)
              .attr('height', innerHeight/10)
              .attr('fill', color)
              .append('title')
              .text(`C: ${c.toFixed(2)}, M: ${m.toFixed(2)}, Y: ${state.analysis.cmyk_vector[2].toFixed(2)}, K: ${state.analysis.cmyk_vector[3].toFixed(2)}`);
          }
        }

        // Plot current CMYK dot
        const cmyk = state.analysis.cmyk_vector;
        g.append('circle')
          .attr('cx', x(cmyk[0]))
          .attr('cy', y(cmyk[1]))
          .attr('r', 8)
          .attr('fill', colorUtils.cmykToHex(cmyk[0], cmyk[1], cmyk[2], cmyk[3]))
          .attr('stroke', '#000')
          .attr('stroke-width', 1.5)
          .append('title')
          .text(`Current:\nC: ${cmyk[0].toFixed(2)}\nM: ${cmyk[1].toFixed(2)}\nY: ${cmyk[2].toFixed(2)}\nK: ${cmyk[3].toFixed(2)}`);
      }
    }
  }, [state.analysis, state.activeColorSpace]);

  // Keyboard shortcut handler
  useEffect(() => {
    const handleKeyPress = (e) => {
      if (e.ctrlKey && e.key === 'Enter') {
        analyzeText();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [input]);

  return (
    <div className="p-6 space-y-6 max-w-3xl mx-auto">
      <Card className="shadow-xl">
        <CardContent className="p-4 space-y-4">
          <Label htmlFor="input">Geef emotionele tekstinput:</Label>
          <div className="relative">
            <Input
              id="input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Bijv: Ik voel me verward en eenzaam..."
              className={state.error ? 'border-red-500' : ''}
              disabled={state.isLoading}
            />
            {state.error && (
              <div className="absolute right-2 top-1/2 -translate-y-1/2 text-red-500">
                <AlertCircle className="w-5 h-5" />
              </div>
            )}
          </div>
          <div className="flex gap-4">
            <Button 
              onClick={analyzeText}
              disabled={state.isLoading}
            >
              {state.isLoading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Analyseren...
                </>
              ) : (
                'Analyseer & Visualiseer'
              )}
            </Button>
            <Button 
              variant="outline" 
              onClick={() => dispatch({ 
                type: 'SET_COLOR_SPACE', 
                payload: state.activeColorSpace === 'LAB' ? 'CMYK' : 'LAB' 
              })}
              disabled={state.isLoading}
            >
              Wissel naar {state.activeColorSpace === 'LAB' ? 'CMYK' : 'LAB'}
            </Button>
          </div>
          {state.error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-red-500 text-sm"
            >
              {state.error}
            </motion.div>
          )}
        </CardContent>
      </Card>

      <AnimatePresence>
        {state.analysis && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
          >
            <Card className="shadow-md">
              <CardContent className="p-4 space-y-6">
                <h3 className="text-lg font-semibold">
                  {state.activeColorSpace === 'LAB' ? 'CIELAB Kleurruimte' : 'CMYK Kleurruimte'}
                </h3>
                <div className="flex flex-col md:flex-row gap-6 items-center">
                  <svg ref={svgRef} width={360} height={360} className="border rounded" />
                  <div className="flex flex-col items-center gap-4">
                    <div
                      className="w-32 h-32 rounded-full border shadow"
                      style={{
                        backgroundColor: state.analysis.rainbow_vector,
                      }}
                    ></div>
                    <div className="text-sm text-center">
                      {state.activeColorSpace === 'LAB' ? (
                        <>
                          <p><strong>L:</strong> {state.analysis.rainbow_vector_lab.L.toFixed(2)}</p>
                          <p><strong>a:</strong> {state.analysis.rainbow_vector_lab.a.toFixed(2)}</p>
                          <p><strong>b:</strong> {state.analysis.rainbow_vector_lab.b.toFixed(2)}</p>
                          <p><strong>Chroma:</strong> {cie1976.calculateChroma(
                            state.analysis.rainbow_vector_lab.a,
                            state.analysis.rainbow_vector_lab.b
                          ).toFixed(2)}</p>
                          <p><strong>Hue:</strong> {cie1976.calculateHueAngle(
                            state.analysis.rainbow_vector_lab.a,
                            state.analysis.rainbow_vector_lab.b
                          ).toFixed(2)}°</p>
                        </>
                      ) : (
                        <>
                          <p><strong>C:</strong> {state.analysis.cmyk_vector[0].toFixed(2)}</p>
                          <p><strong>M:</strong> {state.analysis.cmyk_vector[1].toFixed(2)}</p>
                          <p><strong>Y:</strong> {state.analysis.cmyk_vector[2].toFixed(2)}</p>
                          <p><strong>K:</strong> {state.analysis.cmyk_vector[3].toFixed(2)}</p>
                        </>
                      )}
                      <p><strong>Hex:</strong> {state.analysis.rainbow_vector}</p>
                    </div>
                  </div>
                </div>
                
                <div className="mt-6">
                  <h4 className="font-semibold mb-2">Dominante Emoties:</h4>
                  <div className="grid grid-cols-2 gap-2">
                    {Object.entries(state.analysis.dominant_emotions)
                      .sort(([,a], [,b]) => b - a)
                      .map(([emotion, score]) => (
                        <div key={emotion} className="flex justify-between">
                          <span>{emotion}:</span>
                          <span>{score.toFixed(2)}</span>
                        </div>
                    ))}
                  </div>
                </div>
                
                <div className="mt-4">
                  <h4 className="font-semibold mb-2">Strategie:</h4>
                  <p>{state.analysis.strategy}</p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
} 
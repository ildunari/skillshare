<!-- Deep reference: data visualization. Not auto-loaded. -->
<!-- Access via: grep -A N "SECTION_HEADER" references/deep/data-viz.md -->
# Data Visualization Design

## 1. Custom d3.js Visualization Patterns with React

### Overview

d3.js remains the foundation for custom visualizations, but modern React integration has evolved significantly. The key insight: **use d3 for calculations, React for rendering**.

### visx (Airbnb) — Production-Grade Primitives

**Repository:** https://github.com/airbnb/visx
**Stars:** 20,597
**Philosophy:** Un-opinionated, composable, React-first

visx splits d3 functionality into modular packages:
- `@visx/scale` — Scale utilities
- `@visx/shape` — SVG shape primitives
- `@visx/axis` — Axis components
- `@visx/grid` — Grid components
- `@visx/hierarchy` — Tree, cluster, pack layouts
- `@visx/network` — Force-directed graphs

**Key advantages:**
1. **Bundle size optimization** — import only what you need
2. **No internal state management** — bring your own (Redux, Zustand, etc.)
3. **CSS-in-JS agnostic** — works with any styling solution
4. **TypeScript-first** — full type safety

### Force Graph Pattern (visx + d3-force)

```tsx
import { Group } from '@visx/group';
import { scaleOrdinal } from '@visx/scale';
import { schemeCategory10 } from 'd3-scale-chromatic';
import { forceSimulation, forceLink, forceManyBody, forceCenter } from 'd3-force';
import { useMemo, useEffect, useState } from 'react';

interface Node {
  id: string;
  group: number;
  x?: number;
  y?: number;
  vx?: number;
  vy?: number;
}

interface Link {
  source: string | Node;
  target: string | Node;
  value: number;
}

interface ForceGraphProps {
  width: number;
  height: number;
  nodes: Node[];
  links: Link[];
}

export default function ForceGraph({ width, height, nodes, links }: ForceGraphProps) {
  const [simulationNodes, setSimulationNodes] = useState<Node[]>(nodes);
  const [simulationLinks, setSimulationLinks] = useState<Link[]>(links);

  const colorScale = useMemo(
    () => scaleOrdinal({ domain: [0, 1, 2, 3, 4], range: schemeCategory10 }),
    []
  );

  useEffect(() => {
    const simulation = forceSimulation(nodes)
      .force('link', forceLink(links).id((d: any) => d.id).distance(100))
      .force('charge', forceManyBody().strength(-300))
      .force('center', forceCenter(width / 2, height / 2))
      .on('tick', () => {
        setSimulationNodes([...simulation.nodes()]);
        setSimulationLinks([...links]);
      });

    return () => simulation.stop();
  }, [nodes, links, width, height]);

  return (
    <svg width={width} height={height}>
      <Group>
        {simulationLinks.map((link, i) => {
          const source = link.source as Node;
          const target = link.target as Node;
          return (
            <line
              key={`link-${i}`}
              x1={source.x}
              y1={source.y}
              x2={target.x}
              y2={target.y}
              stroke="#999"
              strokeOpacity={0.6}
              strokeWidth={Math.sqrt(link.value)}
            />
          );
        })}
        {simulationNodes.map((node, i) => (
          <circle
            key={`node-${node.id}`}
            cx={node.x}
            cy={node.y}
            r={8}
            fill={colorScale(node.group)}
            stroke="#fff"
            strokeWidth={2}
          />
        ))}
      </Group>
    </svg>
  );
}
```

**Performance considerations:**
- Use `React.memo()` for node/link components with large datasets
- Implement quadtree collision detection for 500+ nodes
- Consider WebGL via `pixi.js` or `three.js` for 10,000+ nodes

### Sankey Diagram Pattern (visx + d3-sankey)

```tsx
import { Group } from '@visx/group';
import { sankey, sankeyLinkHorizontal } from 'd3-sankey';
import { scaleOrdinal } from '@visx/scale';
import { schemePastel1 } from 'd3-scale-chromatic';

interface SankeyNode {
  name: string;
  category?: string;
}

interface SankeyLink {
  source: number;
  target: number;
  value: number;
}

interface SankeyData {
  nodes: SankeyNode[];
  links: SankeyLink[];
}

export default function SankeyDiagram({
  width,
  height,
  data
}: {
  width: number;
  height: number;
  data: SankeyData
}) {
  const margin = { top: 10, right: 10, bottom: 10, left: 10 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  const sankeyGenerator = sankey()
    .nodeWidth(15)
    .nodePadding(10)
    .extent([[0, 0], [innerWidth, innerHeight]]);

  const { nodes, links } = sankeyGenerator(data as any);

  const colorScale = scaleOrdinal({
    domain: nodes.map(d => d.name),
    range: schemePastel1
  });

  return (
    <svg width={width} height={height}>
      <Group left={margin.left} top={margin.top}>
        {/* Links (flows) */}
        {links.map((link, i) => (
          <path
            key={`link-${i}`}
            d={sankeyLinkHorizontal()(link) || ''}
            fill="none"
            stroke={colorScale((link.source as any).name)}
            strokeOpacity={0.3}
            strokeWidth={Math.max(1, link.width || 0)}
          />
        ))}

        {/* Nodes */}
        {nodes.map((node, i) => {
          const nodeHeight = node.y1! - node.y0!;
          // Only render a label if the node is tall enough to separate it visually
          // from adjacent node labels. At 14px font-size, 20px is the practical minimum.
          const showLabel = nodeHeight >= 20;
          return (
            <g key={`node-${i}`}>
              <rect
                x={node.x0}
                y={node.y0}
                width={node.x1! - node.x0!}
                height={nodeHeight}
                fill={colorScale(node.name)}
                stroke="#fff"
                strokeWidth={2}
              />
              {showLabel && (
                <text
                  x={node.x0! < innerWidth / 2 ? node.x1! + 6 : node.x0! - 6}
                  y={(node.y1! + node.y0!) / 2}
                  dy="0.35em"
                  textAnchor={node.x0! < innerWidth / 2 ? 'start' : 'end'}
                  fontSize={12}
                  fill="#333"
                >
                  {node.name}
                </text>
              )}
            </g>
          );
        })}
      </Group>
    </svg>
  );
}
```

**Use cases:**
- Energy flow diagrams
- Customer journey funnels
- Budget allocation visualizations
- Supply chain flows

### Treemap Pattern (visx + d3-hierarchy)

```tsx
import { Treemap, hierarchy } from '@visx/hierarchy';
import { stratify } from 'd3-hierarchy';
import { scaleLinear } from '@visx/scale';
import { interpolateViridis } from 'd3-scale-chromatic';

interface TreemapData {
  id: string;
  parent: string | null;
  size: number;
  name: string;
}

export default function TreemapChart({
  width,
  height,
  data
}: {
  width: number;
  height: number;
  data: TreemapData[]
}) {
  const root = stratify<TreemapData>()
    .id(d => d.id)
    .parentId(d => d.parent)(data)
    .sum(d => d.size || 0)
    .sort((a, b) => (b.value || 0) - (a.value || 0));

  const colorScale = scaleLinear({
    domain: [0, Math.max(...data.map(d => d.size))],
    range: [0, 1]
  });

  return (
    <svg width={width} height={height}>
      <Treemap
        root={root}
        size={[width, height]}
        tile={() => {}}
        round
      >
        {treemap => (
          <g>
            {treemap.descendants().map((node, i) => {
              const nodeWidth = node.x1 - node.x0;
              const nodeHeight = node.y1 - node.y0;

              return (
                <g key={`node-${i}`}>
                  <rect
                    x={node.x0}
                    y={node.y0}
                    width={nodeWidth}
                    height={nodeHeight}
                    fill={interpolateViridis(colorScale(node.value || 0))}
                    stroke="#fff"
                    strokeWidth={2}
                  />
                  {nodeWidth > 50 && nodeHeight > 30 && (
                    <text
                      x={node.x0 + nodeWidth / 2}
                      y={node.y0 + nodeHeight / 2}
                      textAnchor="middle"
                      fill="#fff"
                      fontSize={12}
                      fontWeight="bold"
                    >
                      {node.data.name}
                    </text>
                  )}
                </g>
              );
            })}
          </g>
        )}
      </Treemap>
    </svg>
  );
}
```

**Best for:**
- Portfolio composition
- File system visualization
- Market share breakdowns
- Hierarchical budget displays

### Observable Notebooks — Rapid Prototyping

**URL:** https://observablehq.com
Observable notebooks (by Mike Bostock, d3 creator) provide interactive d3 examples:
- Live code execution
- Instant visual feedback
- Community gallery of 10,000+ examples
- Export to React-compatible code

**Workflow:**
1. Prototype visualization in Observable
2. Extract d3 logic (scales, layouts, generators)
3. Wrap in React component using visx primitives
4. Add interaction with React state

---

## 2. Recharts Deep Customization

**Repository:** https://github.com/recharts/recharts
**Stars:** 26,596
**Current Version:** 3.7.0 (2024)

Recharts is the most popular composable charting library for React, built on SVG + d3 submodules.

### Custom Shape Example — Gradient Area Chart

```tsx
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const data = [
  { month: 'Jan', revenue: 4000, profit: 2400 },
  { month: 'Feb', revenue: 3000, profit: 1398 },
  { month: 'Mar', revenue: 9800, profit: 9800 },
  // ...
];

export default function GradientAreaChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <AreaChart data={data} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
        <defs>
          <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
          </linearGradient>
          <linearGradient id="colorProfit" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#82ca9d" stopOpacity={0}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
        <XAxis dataKey="month" stroke="#94a3b8" />
        <YAxis stroke="#94a3b8" />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            border: '1px solid #e2e8f0',
            borderRadius: '8px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
          }}
        />
        <Area
          type="monotone"
          dataKey="revenue"
          stroke="#8884d8"
          strokeWidth={2}
          fill="url(#colorRevenue)"
          animationDuration={1000}
        />
        <Area
          type="monotone"
          dataKey="profit"
          stroke="#82ca9d"
          strokeWidth={2}
          fill="url(#colorProfit)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}
```

### Custom Tooltip with Rich Formatting

```tsx
import { TooltipProps } from 'recharts';

const CustomTooltip = ({ active, payload, label }: TooltipProps<number, string>) => {
  if (!active || !payload?.length) return null;

  return (
    <div className="bg-white/95 border border-slate-200 rounded-lg shadow-lg p-4 backdrop-blur-sm">
      <p className="font-semibold text-slate-900 mb-2">{label}</p>
      {payload.map((entry, index) => (
        <div key={index} className="flex items-center gap-2 mb-1">
          <div
            className="w-3 h-3 rounded-full"
            style={{ backgroundColor: entry.color }}
          />
          <span className="text-sm text-slate-600">{entry.name}:</span>
          <span className="text-sm font-medium text-slate-900">
            ${entry.value?.toLocaleString()}
          </span>
        </div>
      ))}
    </div>
  );
};

// Usage in chart
<Tooltip content={<CustomTooltip />} />
```

### Responsive Sizing Pattern

```tsx
import { ResponsiveContainer } from 'recharts';
import { useEffect, useRef, useState } from 'react';

export default function ResponsiveChart({ children }: { children: React.ReactNode }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

  useEffect(() => {
    const observer = new ResizeObserver(entries => {
      if (entries[0]) {
        const { width, height } = entries[0].contentRect;
        setDimensions({ width, height });
      }
    });

    if (containerRef.current) {
      observer.observe(containerRef.current);
    }

    return () => observer.disconnect();
  }, []);

  return (
    <div ref={containerRef} style={{ width: '100%', height: '100%' }}>
      <ResponsiveContainer width="100%" height="100%">
        {children}
      </ResponsiveContainer>
    </div>
  );
}
```

### Dark Mode Theming

```tsx
import { LineChart, Line, XAxis, YAxis } from 'recharts';

const darkTheme = {
  background: '#0f172a',
  grid: '#1e293b',
  text: '#94a3b8',
  line: '#3b82f6'
};

const lightTheme = {
  background: '#ffffff',
  grid: '#f1f5f9',
  text: '#64748b',
  line: '#2563eb'
};

export default function ThemedChart({ isDark = false }) {
  const theme = isDark ? darkTheme : lightTheme;

  // IMPORTANT: Never use hardcoded width/height on charts that live inside
  // layout containers. ResponsiveContainer measures the actual available space
  // after surrounding UI chrome (headers, sidebars, legends) is laid out.
  return (
    <div style={{ backgroundColor: theme.background, width: '100%', height: 300 }}>
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data}>
          <CartesianGrid stroke={theme.grid} />
          <XAxis stroke={theme.text} />
          <YAxis stroke={theme.text} />
          <Line type="monotone" dataKey="value" stroke={theme.line} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
```

### Custom Legend with Interactive Filtering

```tsx
import { useState } from 'react';
import { LineChart, Line, Legend } from 'recharts';

export default function InteractiveLegendChart() {
  const [hiddenLines, setHiddenLines] = useState<Set<string>>(new Set());

  const handleLegendClick = (dataKey: string) => {
    setHiddenLines(prev => {
      const newSet = new Set(prev);
      if (newSet.has(dataKey)) {
        newSet.delete(dataKey);
      } else {
        newSet.add(dataKey);
      }
      return newSet;
    });
  };

  const CustomLegend = ({ payload }: any) => (
    <div className="flex gap-4 justify-center mt-4">
      {payload.map((entry: any) => (
        <button
          key={entry.value}
          onClick={() => handleLegendClick(entry.value)}
          className={`flex items-center gap-2 px-3 py-1 rounded transition-opacity ${
            hiddenLines.has(entry.value) ? 'opacity-30' : 'opacity-100'
          }`}
        >
          <div className="w-4 h-1" style={{ backgroundColor: entry.color }} />
          <span className="text-sm">{entry.value}</span>
        </button>
      ))}
    </div>
  );

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        {!hiddenLines.has('revenue') && (
          <Line dataKey="revenue" stroke="#8884d8" />
        )}
        {!hiddenLines.has('profit') && (
          <Line dataKey="profit" stroke="#82ca9d" />
        )}
        <Legend content={<CustomLegend />} />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

---

## 3. Sparklines and Inline Data Visualization

Sparklines are compact, word-sized visualizations designed by Edward Tufte to show trends inline with text.

### Lightweight Sparkline Component (Pure SVG)

```tsx
interface SparklineProps {
  data: number[];
  width?: number;
  height?: number;
  color?: string;
  showDots?: boolean;
  showArea?: boolean;
}

export default function Sparkline({
  data,
  width = 100,
  height = 30,
  color = '#3b82f6',
  showDots = false,
  showArea = true
}: SparklineProps) {
  const max = Math.max(...data);
  const min = Math.min(...data);
  const range = max - min || 1;

  const points = data.map((value, index) => ({
    x: (index / (data.length - 1)) * width,
    y: height - ((value - min) / range) * height
  }));

  const pathData = points
    .map((point, i) => `${i === 0 ? 'M' : 'L'} ${point.x},${point.y}`)
    .join(' ');

  const areaPathData = `${pathData} L ${width},${height} L 0,${height} Z`;

  return (
    <svg width={width} height={height} className="inline-block align-middle">
      {showArea && (
        <path
          d={areaPathData}
          fill={color}
          fillOpacity={0.2}
        />
      )}
      <path
        d={pathData}
        fill="none"
        stroke={color}
        strokeWidth={1.5}
        strokeLinejoin="round"
      />
      {showDots && points.map((point, i) => (
        <circle
          key={i}
          cx={point.x}
          cy={point.y}
          r={1.5}
          fill={color}
        />
      ))}
    </svg>
  );
}

// Usage in text
<div className="text-sm">
  Revenue is trending <Sparkline data={[4, 6, 5, 8, 9, 10, 12]} color="#10b981" /> upward
</div>
```

### Bar Sparkline for Comparisons

```tsx
export default function BarSparkline({
  data,
  width = 80,
  height = 24
}: {
  data: number[];
  width?: number;
  height?: number;
}) {
  const max = Math.max(...data);
  const barWidth = width / data.length - 1;

  return (
    <svg width={width} height={height} className="inline-block align-middle">
      {data.map((value, i) => {
        const barHeight = (value / max) * height;
        return (
          <rect
            key={i}
            x={i * (barWidth + 1)}
            y={height - barHeight}
            width={barWidth}
            height={barHeight}
            fill={value === max ? '#ef4444' : '#94a3b8'}
            rx={1}
          />
        );
      })}
    </svg>
  );
}
```

### Trending Indicator with Delta

```tsx
interface TrendIndicatorProps {
  current: number;
  previous: number;
  data: number[];
  format?: (n: number) => string;
}

export default function TrendIndicator({
  current,
  previous,
  data,
  format = (n) => n.toFixed(0)
}: TrendIndicatorProps) {
  const delta = current - previous;
  const percentChange = ((delta / previous) * 100).toFixed(1);
  const isPositive = delta > 0;

  return (
    <div className="flex items-center gap-3">
      <div className="text-2xl font-bold">{format(current)}</div>
      <Sparkline data={data} width={60} height={20} color={isPositive ? '#10b981' : '#ef4444'} />
      <div className={`flex items-center gap-1 text-sm font-medium ${
        isPositive ? 'text-green-600' : 'text-red-600'
      }`}>
        {isPositive ? '↑' : '↓'} {Math.abs(Number(percentChange))}%
      </div>
    </div>
  );
}
```

### Small Multiples Pattern

```tsx
const metrics = [
  { name: 'Revenue', data: [4, 6, 5, 8, 9, 10, 12], current: 12000 },
  { name: 'Users', data: [100, 120, 115, 130, 140, 155, 160], current: 160 },
  { name: 'Conversions', data: [2.1, 2.3, 2.0, 2.5, 2.7, 2.8, 3.0], current: 3.0 }
];

export default function SmallMultiples() {
  return (
    <div className="grid grid-cols-3 gap-4">
      {metrics.map(metric => (
        <div key={metric.name} className="bg-white p-4 rounded-lg border">
          <div className="text-sm text-slate-500 mb-1">{metric.name}</div>
          <div className="text-2xl font-bold mb-2">{metric.current.toLocaleString()}</div>
          <Sparkline data={metric.data} width={200} height={40} />
        </div>
      ))}
    </div>
  );
}
```

**Best practices:**
- Keep sparklines simple (no axes, minimal labels)
- Use consistent scales for comparisons
- Show 10-30 data points typically
- Integrate inline with typography (18-24px height)

---

## 4. Radial/Gauge Charts with Animation

Circular progress indicators, speedometer gauges, and donut charts provide intuitive progress visualization.

### Animated Progress Ring

```tsx
import { useEffect, useState } from 'react';

interface ProgressRingProps {
  progress: number; // 0-100
  size?: number;
  strokeWidth?: number;
  color?: string;
  backgroundColor?: string;
  showLabel?: boolean;
}

export default function ProgressRing({
  progress,
  size = 120,
  strokeWidth = 8,
  color = '#3b82f6',
  backgroundColor = '#e2e8f0',
  showLabel = true
}: ProgressRingProps) {
  const [animatedProgress, setAnimatedProgress] = useState(0);

  useEffect(() => {
    const timer = setTimeout(() => setAnimatedProgress(progress), 50);
    return () => clearTimeout(timer);
  }, [progress]);

  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (animatedProgress / 100) * circumference;

  return (
    <div className="relative inline-flex items-center justify-center">
      <svg width={size} height={size} className="transform -rotate-90">
        {/* Background circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={backgroundColor}
          strokeWidth={strokeWidth}
        />
        {/* Progress circle */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          strokeLinecap="round"
          style={{
            transition: 'stroke-dashoffset 1s ease-in-out'
          }}
        />
      </svg>
      {showLabel && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-2xl font-bold">{animatedProgress}%</span>
        </div>
      )}
    </div>
  );
}
```

### Speedometer Gauge Chart

```tsx
export default function SpeedometerGauge({
  value,
  min = 0,
  max = 100,
  size = 200
}: {
  value: number;
  min?: number;
  max?: number;
  size?: number;
}) {
  const percentage = ((value - min) / (max - min)) * 100;
  const angle = (percentage / 100) * 180 - 90; // -90 to 90 degrees

  const radius = size / 2;
  const centerX = radius;
  const centerY = radius;
  const needleLength = radius * 0.7;

  // Calculate needle endpoint
  const radians = (angle * Math.PI) / 180;
  const needleX = centerX + needleLength * Math.cos(radians);
  const needleY = centerY + needleLength * Math.sin(radians);

  return (
    <svg width={size} height={size / 2 + 20} className="overflow-visible">
      {/* Colored arcs for zones */}
      <path
        d={`M ${radius * 0.3},${radius} A ${radius * 0.7},${radius * 0.7} 0 0,1 ${radius},${radius * 0.3}`}
        fill="none"
        stroke="#ef4444"
        strokeWidth={20}
        opacity={0.3}
      />
      <path
        d={`M ${radius},${radius * 0.3} A ${radius * 0.7},${radius * 0.7} 0 0,1 ${radius + radius * 0.495},${radius * 0.495}`}
        fill="none"
        stroke="#f59e0b"
        strokeWidth={20}
        opacity={0.3}
      />
      <path
        d={`M ${radius + radius * 0.495},${radius * 0.495} A ${radius * 0.7},${radius * 0.7} 0 0,1 ${radius * 1.7},${radius}`}
        fill="none"
        stroke="#10b981"
        strokeWidth={20}
        opacity={0.3}
      />

      {/* Needle */}
      <line
        x1={centerX}
        y1={centerY}
        x2={needleX}
        y2={needleY}
        stroke="#1e293b"
        strokeWidth={3}
        strokeLinecap="round"
        style={{
          transition: 'all 0.8s cubic-bezier(0.4, 0, 0.2, 1)'
        }}
      />

      {/* Center dot */}
      <circle cx={centerX} cy={centerY} r={8} fill="#1e293b" />

      {/* Value label */}
      <text
        x={centerX}
        y={centerY + 30}
        textAnchor="middle"
        className="text-2xl font-bold"
        fill="#0f172a"
      >
        {value}
      </text>
    </svg>
  );
}
```

### Multi-Ring Donut Chart

```tsx
import { scaleOrdinal } from '@visx/scale';
import { Pie } from '@visx/shape';
import { Group } from '@visx/group';

interface DonutData {
  label: string;
  value: number;
}

export default function MultiRingDonut({
  innerData,
  outerData,
  size = 300
}: {
  innerData: DonutData[];
  outerData: DonutData[];
  size?: number;
}) {
  const colorScale = scaleOrdinal({
    domain: [...innerData.map(d => d.label), ...outerData.map(d => d.label)],
    range: ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#06b6d4']
  });

  return (
    <svg width={size} height={size}>
      <Group top={size / 2} left={size / 2}>
        {/* Inner ring */}
        <Pie
          data={innerData}
          pieValue={d => d.value}
          outerRadius={size / 4}
          innerRadius={size / 8}
          cornerRadius={3}
          padAngle={0.02}
        >
          {pie => pie.arcs.map((arc, i) => (
            <g key={`inner-arc-${i}`}>
              <path
                d={pie.path(arc) || ''}
                fill={colorScale(arc.data.label)}
              />
            </g>
          ))}
        </Pie>

        {/* Outer ring */}
        <Pie
          data={outerData}
          pieValue={d => d.value}
          outerRadius={size / 2.2}
          innerRadius={size / 3.5}
          cornerRadius={3}
          padAngle={0.02}
        >
          {pie => pie.arcs.map((arc, i) => (
            <g key={`outer-arc-${i}`}>
              <path
                d={pie.path(arc) || ''}
                fill={colorScale(arc.data.label)}
                opacity={0.7}
              />
            </g>
          ))}
        </Pie>
      </Group>
    </svg>
  );
}
```

**Animation best practices:**
- Use `cubic-bezier(0.4, 0, 0.2, 1)` for smooth easing
- Delay initial animation 50-100ms to ensure mount
- Prefer CSS transitions over JS animation when possible
- Cap animation duration at 1s for progress indicators

---

## 5. Geographic Visualizations

### react-simple-maps — Lightweight Map Solution

**Repository:** https://github.com/zcreativelabs/react-simple-maps
**Key features:**
- Built on d3-geo + topojson
- No heavy dependencies (no Mapbox, no Leaflet)
- Declarative React API
- SVG-based (scalable, styleable)

### Choropleth Map Pattern

```tsx
import { ComposableMap, Geographies, Geography } from 'react-simple-maps';
import { scaleQuantize } from 'd3-scale';
import { csv } from 'd3-fetch';
import { useEffect, useState } from 'react';

const geoUrl = 'https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json';

interface CountyData {
  id: string;
  unemployment: number;
}

export default function ChoroplethMap() {
  const [data, setData] = useState<Map<string, number>>(new Map());

  useEffect(() => {
    csv('/unemployment.csv').then(rows => {
      const dataMap = new Map();
      rows.forEach(d => dataMap.set(d.id, +d.rate));
      setData(dataMap);
    });
  }, []);

  const colorScale = scaleQuantize({
    domain: [0, 10],
    range: ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b']
  });

  return (
    <ComposableMap projection="geoAlbersUsa">
      <Geographies geography={geoUrl}>
        {({ geographies }) =>
          geographies.map(geo => {
            const cur = data.get(geo.id);
            return (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                fill={cur ? colorScale(cur) : '#EEE'}
                stroke="#FFF"
                strokeWidth={0.5}
              />
            );
          })
        }
      </Geographies>
    </ComposableMap>
  );
}
```

### Point Map with Custom Markers

```tsx
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';

const cities = [
  { name: 'New York', coordinates: [-74.006, 40.7128], population: 8336000 },
  { name: 'Los Angeles', coordinates: [-118.2437, 34.0522], population: 3979000 },
  { name: 'Chicago', coordinates: [-87.6298, 41.8781], population: 2693000 }
];

export default function PointMap() {
  return (
    <ComposableMap projection="geoAlbersUsa">
      <Geographies geography={geoUrl}>
        {({ geographies }) =>
          geographies.map(geo => (
            <Geography
              key={geo.rsmKey}
              geography={geo}
              fill="#DDD"
              stroke="#FFF"
            />
          ))
        }
      </Geographies>
      {cities.map(city => (
        <Marker key={city.name} coordinates={city.coordinates}>
          <circle
            r={Math.sqrt(city.population) / 200}
            fill="#F53"
            fillOpacity={0.6}
            stroke="#FFF"
            strokeWidth={1}
          />
          {/* SPATIAL NOTE: All labels are offset to y={-12} (above the marker).
              For dense city clusters this will cause overlap. Two strategies:
              1. Pre-filter to show only cities above a population threshold
              2. Use a tooltip on hover instead of persistent labels for crowded maps.
              For sparse city sets (< 20 markers visible), y={-12} is fine.
              For dense maps, suppress labels and rely on tooltips instead. */}
          <text
            textAnchor="middle"
            y={-12}
            style={{ fontSize: '10px', fill: '#333' }}
          >
            {city.name}
          </text>
        </Marker>
      ))}
    </ComposableMap>
  );
}
```

### Lightweight Alternative: SVG World Map

For simpler use cases, use static SVG with CSS:

```tsx
export default function SimpleWorldMap({
  highlightedCountries = []
}: {
  highlightedCountries?: string[]
}) {
  return (
    <svg viewBox="0 0 1000 500" className="w-full">
      <g className="countries">
        {/* Simplified country paths */}
        <path
          d="M 100,100 L 150,80 L 180,120 L 140,140 Z"
          className={highlightedCountries.includes('USA') ? 'fill-blue-500' : 'fill-gray-300'}
        />
        {/* More paths... */}
      </g>
    </svg>
  );
}
```

**Performance tips:**
- Use TopoJSON instead of GeoJSON (10x smaller)
- Simplify geometries with mapshaper.org
- Lazy load map data with dynamic imports
- Consider static image + SVG overlay for complex maps

---

## 6. Real-Time Data Streaming UIs

### WebSocket + Chart Update Pattern

```tsx
import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis } from 'recharts';

export default function LiveChart() {
  const [data, setData] = useState<Array<{ time: string; value: number }>>([]);
  const maxPoints = 50; // Keep last 50 points

  useEffect(() => {
    const ws = new WebSocket('wss://api.example.com/live');

    ws.onmessage = (event) => {
      const newPoint = JSON.parse(event.data);

      setData(prev => {
        const updated = [...prev, {
          time: new Date().toLocaleTimeString(),
          value: newPoint.value
        }];

        // Keep only last N points
        return updated.slice(-maxPoints);
      });
    };

    return () => ws.close();
  }, []);

  return (
    // Disable animation for real-time — it causes artifacts when data shifts constantly.
    // ResponsiveContainer lets the chart fill its parent without hardcoded pixel assumptions.
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="time" />
        <YAxis />
        <Line
          type="monotone"
          dataKey="value"
          stroke="#3b82f6"
          isAnimationActive={false} // Disable for real-time
          dot={false} // Remove dots for performance
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
```

### Optimistic Rendering Pattern

```tsx
import { useCallback, useRef } from 'react';

export default function OptimisticLiveChart() {
  const dataRef = useRef<number[]>([]);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const updateChart = useCallback((newValue: number) => {
    // Optimistic update - don't wait for state
    dataRef.current = [...dataRef.current.slice(-49), newValue];

    // Direct canvas manipulation for 60fps
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.beginPath();
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 2;

    dataRef.current.forEach((value, i) => {
      const x = (i / 50) * canvas.width;
      const y = canvas.height - (value / 100) * canvas.height;

      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });

    ctx.stroke();
  }, []);

  useEffect(() => {
    const ws = new WebSocket('wss://api.example.com/live');
    ws.onmessage = (event) => {
      const { value } = JSON.parse(event.data);
      updateChart(value);
    };
    return () => ws.close();
  }, [updateChart]);

  return (
    // Use a wrapper div and read canvas dimensions from it — never hardcode canvas size.
    <div style={{ width: '100%', height: 300, position: 'relative' }}>
      <canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} />
    </div>
  );
}
```

### Live Activity Feed

```tsx
interface Activity {
  id: string;
  user: string;
  action: string;
  timestamp: Date;
}

export default function ActivityFeed() {
  const [activities, setActivities] = useState<Activity[]>([]);
  const maxActivities = 20;

  useEffect(() => {
    const ws = new WebSocket('wss://api.example.com/activity');

    ws.onmessage = (event) => {
      const activity = JSON.parse(event.data);

      setActivities(prev => [
        { ...activity, timestamp: new Date() },
        ...prev.slice(0, maxActivities - 1)
      ]);
    };

    return () => ws.close();
  }, []);

  return (
    <div className="space-y-2 h-96 overflow-y-auto">
      {activities.map(activity => (
        <div
          key={activity.id}
          className="bg-white border rounded-lg p-3 animate-slide-in"
        >
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="font-medium">{activity.user}</span>
            <span className="text-sm text-slate-500">{activity.action}</span>
          </div>
          <div className="text-xs text-slate-400 mt-1">
            {activity.timestamp.toLocaleTimeString()}
          </div>
        </div>
      ))}
    </div>
  );
}

// Tailwind animation
// @keyframes slide-in {
//   from { transform: translateX(-100%); opacity: 0; }
//   to { transform: translateX(0); opacity: 1; }
// }
```

### Ticker Display Component

```tsx
export default function Ticker({
  items
}: {
  items: Array<{ label: string; value: number; change: number }>
}) {
  return (
    <div className="flex overflow-x-auto gap-4 py-2 scrollbar-hide">
      {items.map(item => (
        <div key={item.label} className="flex-shrink-0 bg-slate-900 text-white px-4 py-2 rounded">
          <div className="text-xs text-slate-400">{item.label}</div>
          <div className="flex items-baseline gap-2">
            <div className="text-xl font-bold tabular-nums">{item.value}</div>
            <div className={`text-sm ${item.change >= 0 ? 'text-green-400' : 'text-red-400'}`}>
              {item.change >= 0 ? '+' : ''}{item.change.toFixed(2)}%
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
```

**Best practices:**
- Disable animations for real-time charts (set `isAnimationActive={false}`)
- Use canvas for 60fps updates (100+ data points/sec)
- Implement circular buffer to cap memory usage
- Add connection status indicator
- Throttle updates to 16ms (60fps) with `requestAnimationFrame`

---

## 7. Dashboard Composition Principles

Based on research from UXPin, Pencil & Paper, and real-world examples (Vercel, Linear, Stripe).

### Information Hierarchy Framework

**Tufte's Data-Ink Ratio:**
> Maximize the ratio of data-ink to total ink used in the graphic.

**Application:**
1. Remove non-essential gridlines
2. Eliminate decorative elements (3D effects, shadows)
3. Use whitespace to separate, not borders
4. Label directly on charts, not in legends when possible

### Dashboard Layout Grid System

```tsx
// Tailwind + CSS Grid approach
export default function DashboardGrid({ children }: { children: React.ReactNode }) {
  return (
    <div className="grid grid-cols-12 gap-4 p-4">
      {/* KPI cards - 3 columns each */}
      <div className="col-span-12 lg:col-span-4">
        <KPICard title="Revenue" value="$45.2K" change={8.3} />
      </div>
      <div className="col-span-12 lg:col-span-4">
        <KPICard title="Users" value="12.5K" change={-2.1} />
      </div>
      <div className="col-span-12 lg:col-span-4">
        <KPICard title="Conversion" value="3.2%" change={0.4} />
      </div>

      {/* Main chart - 8 columns */}
      <div className="col-span-12 lg:col-span-8">
        <ChartCard title="Revenue Trend">
          <LineChart {...props} />
        </ChartCard>
      </div>

      {/* Side metrics - 4 columns */}
      <div className="col-span-12 lg:col-span-4">
        <MetricsList items={topProducts} />
      </div>

      {/* Footer row - 6 columns each */}
      <div className="col-span-12 lg:col-span-6">
        <TableCard title="Recent Orders" />
      </div>
      <div className="col-span-12 lg:col-span-6">
        <MapCard title="Traffic by Region" />
      </div>
    </div>
  );
}
```

### Progressive Disclosure Pattern

```tsx
import { useState } from 'react';

export default function ExpandableWidget({ title, summary, details }: {
  title: string;
  summary: React.ReactNode;
  details: React.ReactNode;
}) {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white border rounded-lg">
      <div className="p-4">
        <div className="flex items-center justify-between mb-2">
          <h3 className="font-semibold">{title}</h3>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-sm text-blue-600 hover:text-blue-800"
          >
            {isExpanded ? 'Show less' : 'Show more'}
          </button>
        </div>

        {/* Always visible summary */}
        <div>{summary}</div>

        {/* Expandable details */}
        {isExpanded && (
          <div className="mt-4 pt-4 border-t">
            {details}
          </div>
        )}
      </div>
    </div>
  );
}
```

### Data Density vs Clarity Tradeoffs

**High density (analyst dashboards):**
- Small multiples (Tufte)
- Compact tables with inline sparklines
- Heatmaps for correlation matrices
- Target: 5-7 widgets per screen

**Low density (executive dashboards):**
- Large KPI numbers (48-72px)
- Single primary chart
- 2-3 data points visible at once
- Target: 3-4 widgets per screen

### Widget Grouping Strategy

```tsx
// Semantic grouping example
export default function DashboardSections() {
  return (
    <div className="space-y-6">
      {/* Section: Overview */}
      <section>
        <h2 className="text-xl font-bold mb-4">Overview</h2>
        <div className="grid grid-cols-3 gap-4">
          <KPICard />
          <KPICard />
          <KPICard />
        </div>
      </section>

      {/* Section: Performance */}
      <section>
        <h2 className="text-xl font-bold mb-4">Performance</h2>
        <div className="grid grid-cols-2 gap-4">
          <LineChart />
          <BarChart />
        </div>
      </section>

      {/* Section: Activity */}
      <section>
        <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
        <ActivityTable />
      </section>
    </div>
  );
}
```

### Real-World Examples Analysis

**Vercel Analytics:**
- Minimalist: white background, blue accent
- Curve-fitted smoothing for noisy data
- Time range selector prominent
- Inline metric comparisons (vs previous period)

**Linear:**
- Dark theme with neon accents
- Velocity charts for team performance
- Cycle time breakdown
- Embedded issue list in dashboard

**Stripe Dashboard:**
- Revenue as hero metric (large, centered)
- Inline filtering (date, payment method)
- Payment flow Sankey diagram
- Density toggles (compact/comfortable)

---

## 8. Color in Data Visualization

### ColorBrewer — Research-Backed Palettes

**URL:** https://colorbrewer2.org
ColorBrewer provides scientifically tested color schemes for maps and data viz.

**Palette types:**

#### Sequential (single-hue)
For ordered data from low to high:
```javascript
import { schemeBlues, schemeGreens, schemeReds } from 'd3-scale-chromatic';

// 9-step blue scale
const blues = schemeBlues[9];
// ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b']
```

**Use when:** showing magnitude, density, or progression

#### Sequential (multi-hue)
For emphasis on low/high extremes:
```javascript
import { schemeYlGnBu, schemeYlOrRd } from 'd3-scale-chromatic';

const ylGnBu = schemeYlGnBu[9];
// Yellow → Green → Blue
```

**Use when:** temperature maps, elevation, risk scores

#### Diverging
For data with critical midpoint:
```javascript
import { schemeRdBu, schemeRdYlGn } from 'd3-scale-chromatic';

const rdBu = schemeRdBu[11];
// Red ← White → Blue
```

**Use when:** profit/loss, above/below average, sentiment

#### Categorical
For distinct, unordered groups:
```javascript
import { schemeCategory10, schemeTableau10, schemePaired } from 'd3-scale-chromatic';

const category10 = schemeCategory10;
// ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', ...]
```

**Use when:** product lines, countries, user segments

### Colorblind-Safe Palettes

**Viridis family** (designed for colorblind accessibility):
```javascript
import { interpolateViridis, interpolateCividis, interpolatePlasma } from 'd3-scale-chromatic';
import { scaleSequential } from 'd3-scale';

const viridisScale = scaleSequential(interpolateViridis).domain([0, 100]);
viridisScale(50); // Returns color for value 50

// Cividis - optimized for CVD (color vision deficiency)
const cividisScale = scaleSequential(interpolateCividis).domain([0, 100]);
```

**Testing for colorblindness:**
- Use Chrome DevTools: Rendering → Emulate vision deficiencies
- Online: https://www.color-blindness.com/coblis-color-blindness-simulator/
- Ensure 4.5:1 contrast ratio (WCAG AA)

### Implementing Themed Color Scales

```tsx
import { scaleOrdinal, scaleSequential } from 'd3-scale';
import { interpolateViridis } from 'd3-scale-chromatic';

// Theme-aware color utility
export const useChartColors = (theme: 'light' | 'dark' = 'light') => {
  const categoricalColors = theme === 'light'
    ? ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981']
    : ['#60a5fa', '#a78bfa', '#f472b6', '#fbbf24', '#34d399'];

  const sequentialScale = scaleSequential(interpolateViridis)
    .domain([0, 100]);

  const categoricalScale = scaleOrdinal()
    .domain(['A', 'B', 'C', 'D', 'E'])
    .range(categoricalColors);

  return { categoricalScale, sequentialScale, categoricalColors };
};

// Usage
export default function ThemedChart() {
  const { categoricalScale } = useChartColors('light');

  return (
    <BarChart data={data}>
      {categories.map((cat, i) => (
        <Bar
          key={cat}
          dataKey={cat}
          fill={categoricalScale(cat)}
        />
      ))}
    </BarChart>
  );
}
```

### Color Best Practices

1. **Limit palette size:**
   - Categorical: max 5-7 distinct colors
   - Sequential: 5-9 steps optimal
   - Diverging: 7-11 steps

2. **Semantic color usage:**
   - Red: error, negative, danger
   - Green: success, positive, growth
   - Blue: neutral, information, primary
   - Yellow/Orange: warning, attention

3. **Accessibility checklist:**
   - [ ] 4.5:1 contrast for text on colored backgrounds
   - [ ] Don't rely on color alone (use icons, patterns)
   - [ ] Test with grayscale conversion
   - [ ] Provide alternative color schemes

4. **Dynamic color assignment:**
```tsx
import { color } from 'd3-color';

// Lighten/darken programmatically
const baseColor = color('#3b82f6');
const lighterColor = baseColor.brighter(0.5).toString();
const darkerColor = baseColor.darker(0.5).toString();

// For hover states
<Bar
  fill="#3b82f6"
  onMouseEnter={(e) => e.target.setAttribute('fill', lighterColor)}
  onMouseLeave={(e) => e.target.setAttribute('fill', '#3b82f6')}
/>
```

---

## Label Placement & Spatial Integrity

LLMs generate layout in a single pass with no render feedback. Every coordinate is a prediction, not a measurement. These rules prevent the most common class of chart defects: element overlap.

### Rule 1: Always use responsive containers for Recharts

Never pass hardcoded `width` and `height` to Recharts charts directly. Hardcoded dimensions assume surrounding UI chrome (sidebars, headers, legends, padding) doesn't exist.

```tsx
// BAD — assumes the chart is 600px wide regardless of its actual container
<LineChart width={600} height={300} data={data} />

// GOOD — measures the actual available space after all surrounding layout is resolved
<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data} />
</ResponsiveContainer>
```

### Rule 2: Canvas charts must use ResizeObserver, not hardcoded width/height

```tsx
// BAD
return <canvas ref={canvasRef} width={800} height={400} />;

// GOOD — let the container determine the size, read it with ResizeObserver
const containerRef = useRef<HTMLDivElement>(null);
useEffect(() => {
  const draw = () => {
    const { width, height } = containerRef.current!.getBoundingClientRect();
    canvas.width = width;
    canvas.height = height;
    // ... draw
  };
  const observer = new ResizeObserver(draw);
  observer.observe(containerRef.current!);
  return () => observer.disconnect();
}, [data]);
return <div ref={containerRef} style={{ width: '100%', height: 400 }}><canvas ref={canvasRef} /></div>;
```

### Rule 3: Gate labels by parent element size

Render text labels only when the parent element is large enough to contain them without overlapping adjacent elements.

```tsx
// Treemap — already gated (minimum 50px × 30px)
{nodeWidth > 50 && nodeHeight > 30 && <text>{node.data.name}</text>}

// Sankey — gate labels by node height (minimum 20px for 12px font)
{(node.y1! - node.y0!) >= 20 && <text>{node.name}</text>}

// Pie/donut arcs — gate labels by arc span (minimum 15° for readable labels)
const arcSpan = arc.endAngle - arc.startAngle; // in radians
{arcSpan >= 0.26 && <text>{arc.data.label}</text>} // ~15°
```

### Rule 4: Separate spatial lanes for independent label systems

When a chart has multiple categories of text (axis labels, annotation labels, tick numbers, category names), each must occupy a distinct spatial "lane" with ≥20px separation.

```tsx
// BAD — two label systems at similar radii will collide on dense pies
outerRadius={size / 2}
labelRadius={size / 2 + 10}  // annotation labels
tickRadius={size / 2 + 12}   // tick labels — WILL OVERLAP

// GOOD — distinct radii with meaningful separation
labelRadius={outerRadius + 14}    // category labels
valueRadius={outerRadius + 36}    // value labels — 22px separation
```

### Rule 5: Tooltip-first for dense or variable-density datasets

When label count is unpredictable (user data, API responses), default to showing labels on hover via tooltip rather than persistent inline labels. This eliminates collision as a failure mode entirely.

```tsx
// For maps with variable city density
// DON'T: render labels for every marker
// DO: show a tooltip on hover, suppress persistent labels

<Tooltip content={<CityTooltip />} />
// And remove the <text> elements from each marker
```

### Rule 6: Post-render collision detection for complex layouts

For force-directed graphs, scatter plots with labels, and tree diagrams, add a collision resolution pass after initial rendering:

```tsx
useEffect(() => {
  // After simulation stabilizes, check label bboxes for overlap
  const labelElements = svgRef.current?.querySelectorAll('text.node-label');
  if (!labelElements) return;

  const bboxes: DOMRect[] = [];
  labelElements.forEach((el, i) => {
    const bbox = (el as SVGTextElement).getBBox();
    // Hide if it overlaps any previously placed label
    const overlaps = bboxes.some(prev =>
      !(bbox.right < prev.left || bbox.left > prev.right ||
        bbox.bottom < prev.top || bbox.top > prev.bottom)
    );
    (el as SVGTextElement).style.display = overlaps ? 'none' : '';
    if (!overlaps) bboxes.push(bbox);
  });
}, [simulationNodes]);
```

---



| Library | Stars | Bundle Size | Strengths | Weaknesses |
|---------|-------|-------------|-----------|------------|
| **Recharts** | 26.6K | ~100KB | Composable, declarative, great docs | Limited customization depth |
| **visx** | 20.6K | ~30KB (modular) | Full d3 power, TypeScript, flexible | Steeper learning curve |
| **Nivo** | 13K | ~200KB | Beautiful defaults, rich animations | Large bundle, opinionated |
| **Victory** | 11K | ~150KB | Formidable quality, mobile-first | Bundle size, React Native focus |
| **shadcn/ui charts** | N/A | ~50KB | Copy-paste, Tailwind integration | Limited to Recharts patterns |
| **Tremor** | N/A | ~80KB | Dashboard-specific, templates | Less flexible for custom viz |

### Recommendation Matrix

**Choose Recharts if:** You want quick, production-ready charts with minimal setup
**Choose visx if:** You need custom visualizations or advanced d3 patterns
**Choose Nivo if:** Design quality is paramount and bundle size isn't critical
**Choose shadcn/ui if:** You're using Tailwind and want copy-paste components
**Choose Tremor if:** Building dashboards and need prebuilt templates

---

## Performance Considerations for Large Datasets

### 1. Virtualization for Tables

```tsx
import { useVirtualizer } from '@tanstack/react-virtual';
import { useRef } from 'react';

export default function VirtualizedTable({ data }: { data: any[] }) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: data.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 50, // Row height
    overscan: 5
  });

  return (
    <div ref={parentRef} style={{ height: '400px', overflow: 'auto' }}>
      <div style={{ height: `${virtualizer.getTotalSize()}px`, position: 'relative' }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.index}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualRow.size}px`,
              transform: `translateY(${virtualRow.start}px)`
            }}
          >
            <TableRow data={data[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 2. Data Aggregation

```tsx
// Reduce 10,000 points to 100 for display
function aggregateData(data: number[], targetPoints: number = 100) {
  const bucketSize = Math.ceil(data.length / targetPoints);
  const aggregated = [];

  for (let i = 0; i < data.length; i += bucketSize) {
    const bucket = data.slice(i, i + bucketSize);
    const avg = bucket.reduce((sum, val) => sum + val, 0) / bucket.length;
    aggregated.push(avg);
  }

  return aggregated;
}
```

### 3. Canvas Rendering for 10,000+ Points

```tsx
import { useEffect, useRef } from 'react';

export default function CanvasLineChart({ data }: { data: number[] }) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    const draw = () => {
      // Always read dimensions from the actual rendered container,
      // never hardcode canvas width/height — the parent determines the space.
      const { width, height } = container.getBoundingClientRect();
      canvas.width = width;
      canvas.height = height;

      const ctx = canvas.getContext('2d')!;
      const max = Math.max(...data);

      ctx.clearRect(0, 0, width, height);
      ctx.beginPath();
      ctx.strokeStyle = '#3b82f6';
      ctx.lineWidth = 2;

      data.forEach((value, i) => {
        const x = (i / data.length) * width;
        const y = height - (value / max) * height;

        if (i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });

      ctx.stroke();
    };

    // Draw initially and whenever container size changes (responsive resize)
    const observer = new ResizeObserver(draw);
    observer.observe(container);
    draw();

    return () => observer.disconnect();
  }, [data]);

  return (
    <div ref={containerRef} style={{ width: '100%', height: 400, position: 'relative' }}>
      <canvas ref={canvasRef} style={{ width: '100%', height: '100%' }} />
    </div>
  );
}
```

### 4. Debounced Interactions

```tsx
import { useMemo } from 'react';
import debounce from 'lodash.debounce';

export default function InteractiveChart({ data }: { data: any[] }) {
  const handleHover = useMemo(
    () => debounce((index: number) => {
      // Expensive tooltip computation
      console.log('Hovered:', index);
    }, 100),
    []
  );

  return (
    <BarChart data={data}>
      <Bar onMouseEnter={(_, index) => handleHover(index)} />
    </BarChart>
  );
}
```

---

## Production Stack Recommendation (2025)

**For dashboard applications:**
```
- Base charts: Recharts 3.7+
- Custom viz: visx primitives
- Colors: d3-scale-chromatic (Viridis, ColorBrewer)
- Animation: Framer Motion
- Responsive: react-use dimensions hook
- Tables: TanStack Table + Virtual
```

**For real-time applications:**
```
- Canvas rendering: custom with requestAnimationFrame
- WebSocket: native or Socket.io
- State: Zustand or Jotai (lightweight)
- Performance: React.memo, useMemo, useCallback
```

**For geographic applications:**
```
- Simple maps: react-simple-maps
- Complex maps: Mapbox GL (with react-map-gl)
- Choropleth: d3-geo + TopoJSON
```

### Common Pitfalls to Avoid

1. **Overloading with data** — Show 5-7 metrics max per view
2. **Ignoring accessibility** — Always test colorblind simulation
3. **Animating real-time data** — Disable for >1 update/sec
4. **Not aggregating** — Reduce 10K+ points before rendering
5. **Using 3D charts** — They distort perception and add no value
6. **Color without meaning** — Use semantic color assignments
7. **Neglecting mobile** — Design responsive from day one

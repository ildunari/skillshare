# D3.js Visualisation Patterns

This reference provides detailed code patterns for common d3.js visualisation types.

## Hierarchical visualisations

### Tree diagram

```javascript
useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const tree = d3.tree().size([height - 100, width - 200]);
  
  const root = d3.hierarchy(data);
  tree(root);
  
  const g = svg.append("g")
    .attr("transform", "translate(100,50)");
  
  // Links
  g.selectAll("path")
    .data(root.links())
    .join("path")
    .attr("d", d3.linkHorizontal()
      .x(d => d.y)
      .y(d => d.x))
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-width", 2);
  
  // Nodes
  const node = g.selectAll("g")
    .data(root.descendants())
    .join("g")
    .attr("transform", d => `translate(${d.y},${d.x})`);
  
  node.append("circle")
    .attr("r", 6)
    .attr("fill", d => d.children ? "#555" : "#999");
  
  node.append("text")
    .attr("dy", "0.31em")
    .attr("x", d => d.children ? -8 : 8)
    .attr("text-anchor", d => d.children ? "end" : "start")
    .text(d => d.data.name)
    .style("font-size", "12px");
    
}, [data]);
```

### Treemap

```javascript
useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);
  
  d3.treemap()
    .size([width, height])
    .padding(2)
    .round(true)(root);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const cell = svg.selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr("transform", d => `translate(${d.x0},${d.y0})`);
  
  cell.append("rect")
    .attr("width", d => d.x1 - d.x0)
    .attr("height", d => d.y1 - d.y0)
    .attr("fill", d => colourScale(d.parent.data.name))
    .attr("stroke", "white")
    .attr("stroke-width", 2);
  
  cell.append("text")
    .attr("x", 4)
    .attr("y", 16)
    .text(d => d.data.name)
    .style("font-size", "12px")
    .style("fill", "white");
    
}, [data]);
```

### Sunburst diagram

**Layout note**: Always compute sunburst radius from available space *after* subtracting all UI chrome (header, breadcrumb, legend). Use flow layout for surrounding elements so they claim real space. Never use `position: absolute` for chart chrome that might overlap the SVG.

```javascript
// GOOD: compute size from remaining space
const headerH = document.querySelector('.header').getBoundingClientRect().height;
const breadcrumbH = document.querySelector('.breadcrumb')?.getBoundingClientRect().height || 0;
const padding = 32;
const availableH = window.innerHeight - headerH - breadcrumbH - padding;
const size = Math.min(window.innerWidth - 32, availableH);
const radius = size / 2;

// CSS: use flow layout, not absolute positioning
// .header { padding: 28px 32px 4px; }
// .breadcrumb { padding: 8px 32px; }  /* in flow, not absolute */
// #chart { flex: 1; min-height: 0; }

useEffect(() => {
  if (!data) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 600;
  const height = 600;
  const radius = Math.min(width, height) / 2;
  
  const root = d3.hierarchy(data)
    .sum(d => d.value)
    .sort((a, b) => b.value - a.value);
  
  const partition = d3.partition()
    .size([2 * Math.PI, radius]);
  
  partition(root);
  
  const arc = d3.arc()
    .startAngle(d => d.x0)
    .endAngle(d => d.x1)
    .innerRadius(d => d.y0)
    .outerRadius(d => d.y1);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);
  
  g.selectAll("path")
    .data(root.descendants())
    .join("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(d.depth))
    .attr("stroke", "white")
    .attr("stroke-width", 1);
    
}, [data]);
```

### Chord diagram

```javascript
function drawChordDiagram(data) {
  // data format: array of objects with source, target, and value
  // Example: [{ source: 'A', target: 'B', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 600;
  const height = 600;
  const innerRadius = Math.min(width, height) * 0.3;
  const outerRadius = innerRadius + 30;

  // Label radii — separate lanes to prevent overlap
  const tickLabelOffset = 6;       // ticks hug the arc edge
  const nameLabelRadius = outerRadius + 34; // names in outer lane, 20px+ clear of ticks

  // Minimum arc thresholds for label rendering
  const MIN_ARC_FOR_TICKS = 0.3;      // radians — skip ticks on small arcs
  const MIN_ARC_FOR_TICK_TEXT = 0.5;   // radians — skip tick numbers on medium arcs

  // Create matrix from data
  const nodes = Array.from(new Set(data.flatMap(d => [d.source, d.target])));
  const matrix = Array.from({ length: nodes.length }, () => Array(nodes.length).fill(0));

  data.forEach(d => {
    const i = nodes.indexOf(d.source);
    const j = nodes.indexOf(d.target);
    matrix[i][j] += d.value;
    matrix[j][i] += d.value;
  });

  // Create chord layout
  const chord = d3.chord()
    .padAngle(0.05)
    .sortSubgroups(d3.descending);

  const arc = d3.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

  const ribbon = d3.ribbon()
    .source(d => d.source)
    .target(d => d.target);

  const colourScale = d3.scaleOrdinal(d3.schemeCategory10)
    .domain(nodes);

  const g = svg.append("g")
    .attr("transform", `translate(${width / 2},${height / 2})`);

  const chords = chord(matrix);

  // Draw ribbons
  g.append("g")
    .attr("fill-opacity", 0.67)
    .selectAll("path")
    .data(chords)
    .join("path")
    .attr("d", ribbon)
    .attr("fill", d => colourScale(nodes[d.source.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.source.index])).darker());

  // Draw groups (arcs)
  const group = g.append("g")
    .selectAll("g")
    .data(chords.groups)
    .join("g");

  group.append("path")
    .attr("d", arc)
    .attr("fill", d => colourScale(nodes[d.index]))
    .attr("stroke", d => d3.rgb(colourScale(nodes[d.index])).darker());

  // Name labels — outer lane, gated by minimum arc size
  group.append("text")
    .each(d => { d.angle = (d.startAngle + d.endAngle) / 2; })
    .filter(d => (d.endAngle - d.startAngle) > 0.08) // skip labels for tiny arcs
    .attr("dy", "0.31em")
    .attr("transform", d => `rotate(${(d.angle * 180 / Math.PI) - 90})translate(${nameLabelRadius})${d.angle > Math.PI ? "rotate(180)" : ""}`)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text((d, i) => nodes[d.index])
    .style("font-size", "12px");

  // Tick marks — only on arcs wide enough to accommodate them
  const ticks = group.filter(d => (d.endAngle - d.startAngle) > MIN_ARC_FOR_TICKS)
    .append("g")
    .selectAll("g")
    .data(d => {
      const k = (d.endAngle - d.startAngle) / d.value;
      return d3.range(0, d.value, 100).map(value => ({
        value, angle: value * k + d.startAngle,
        arcSpan: d.endAngle - d.startAngle
      }));
    })
    .join("g")
    .attr("transform", d => `rotate(${d.angle * 180 / Math.PI - 90}) translate(${outerRadius})`);

  ticks.append("line")
    .attr("x2", tickLabelOffset)
    .attr("stroke", "#999");

  // Tick text — only on arcs wide enough that numbers won't collide
  ticks.filter(d => d.arcSpan > MIN_ARC_FOR_TICK_TEXT && d.value % 200 === 0)
    .append("text")
    .attr("x", tickLabelOffset + 4)
    .attr("dy", "0.35em")
    .attr("transform", d => d.angle > Math.PI ? "rotate(180) translate(-16)" : null)
    .attr("text-anchor", d => d.angle > Math.PI ? "end" : null)
    .text(d => `${d.value}`)
    .style("font-size", "10px");
}

// Data format example:
// const data = [
//   { source: 'Category A', target: 'Category B', value: 100 },
//   { source: 'Category A', target: 'Category C', value: 50 },
//   { source: 'Category B', target: 'Category C', value: 75 }
// ];
// drawChordDiagram(data);
```

## Advanced chart types

### Heatmap

```javascript
function drawHeatmap(data) {
  // data format: array of objects with row, column, and value
  // Example: [{ row: 'A', column: 'X', value: 10 }, ...]

  if (!data || data.length === 0) return;

  const svg = d3.select('#chart');
  svg.selectAll("*").remove();

  const width = 800;
  const height = 600;
  const margin = { top: 100, right: 30, bottom: 30, left: 100 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Get unique rows and columns
  const rows = Array.from(new Set(data.map(d => d.row)));
  const columns = Array.from(new Set(data.map(d => d.column)));

  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

  // Create scales
  const xScale = d3.scaleBand()
    .domain(columns)
    .range([0, innerWidth])
    .padding(0.01);

  const yScale = d3.scaleBand()
    .domain(rows)
    .range([0, innerHeight])
    .padding(0.01);

  // Colour scale for values (sequential from light to dark red)
  const colourScale = d3.scaleSequential(d3.interpolateYlOrRd)
    .domain([0, d3.max(data, d => d.value)]);

  // Draw rectangles
  g.selectAll("rect")
    .data(data)
    .join("rect")
    .attr("x", d => xScale(d.column))
    .attr("y", d => yScale(d.row))
    .attr("width", xScale.bandwidth())
    .attr("height", yScale.bandwidth())
    .attr("fill", d => colourScale(d.value));

  // Add x-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(columns)
    .join("text")
    .attr("x", d => xScale(d) + xScale.bandwidth() / 2)
    .attr("y", -10)
    .attr("text-anchor", "middle")
    .text(d => d)
    .style("font-size", "12px");

  // Add y-axis labels
  svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`)
    .selectAll("text")
    .data(rows)
    .join("text")
    .attr("x", -10)
    .attr("y", d => yScale(d) + yScale.bandwidth() / 2)
    .attr("dy", "0.35em")
    .attr("text-anchor", "end")
    .text(d => d)
    .style("font-size", "12px");

  // Add colour legend
  const legendWidth = 20;
  const legendHeight = 200;
  const legend = svg.append("g")
    .attr("transform", `translate(${width - 60},${margin.top})`);

  const legendScale = d3.scaleLinear()
    .domain(colourScale.domain())
    .range([legendHeight, 0]);

  const legendAxis = d3.axisRight(legendScale).ticks(5);

  // Draw colour gradient in legend
  for (let i = 0; i < legendHeight; i++) {
    legend.append("rect")
      .attr("y", i)
      .attr("width", legendWidth)
      .attr("height", 1)
      .attr("fill", colourScale(legendScale.invert(i)));
  }

  legend.append("g")
    .attr("transform", `translate(${legendWidth},0)`)
    .call(legendAxis);
}

// Data format example:
// const data = [
//   { row: 'Monday', column: 'Morning', value: 42 },
//   { row: 'Monday', column: 'Afternoon', value: 78 },
//   { row: 'Tuesday', column: 'Morning', value: 65 },
//   { row: 'Tuesday', column: 'Afternoon', value: 55 }
// ];
// drawHeatmap(data);
```

### Area chart with gradient

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  // Define gradient
  const defs = svg.append("defs");
  const gradient = defs.append("linearGradient")
    .attr("id", "areaGradient")
    .attr("x1", "0%")
    .attr("x2", "0%")
    .attr("y1", "0%")
    .attr("y2", "100%");
  
  gradient.append("stop")
    .attr("offset", "0%")
    .attr("stop-color", "steelblue")
    .attr("stop-opacity", 0.8);
  
  gradient.append("stop")
    .attr("offset", "100%")
    .attr("stop-color", "steelblue")
    .attr("stop-opacity", 0.1);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const xScale = d3.scaleTime()
    .domain(d3.extent(data, d => d.date))
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.value)])
    .range([innerHeight, 0]);
  
  const area = d3.area()
    .x(d => xScale(d.date))
    .y0(innerHeight)
    .y1(d => yScale(d.value))
    .curve(d3.curveMonotoneX);
  
  g.append("path")
    .datum(data)
    .attr("fill", "url(#areaGradient)")
    .attr("d", area);
  
  const line = d3.line()
    .x(d => xScale(d.date))
    .y(d => yScale(d.value))
    .curve(d3.curveMonotoneX);
  
  g.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 2)
    .attr("d", line);
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### Stacked bar chart

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const categories = Object.keys(data[0]).filter(k => k !== 'group');
  const stackedData = d3.stack().keys(categories)(data);
  
  const xScale = d3.scaleBand()
    .domain(data.map(d => d.group))
    .range([0, innerWidth])
    .padding(0.1);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(stackedData[stackedData.length - 1], d => d[1])])
    .range([innerHeight, 0]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  g.selectAll("g")
    .data(stackedData)
    .join("g")
    .attr("fill", (d, i) => colourScale(i))
    .selectAll("rect")
    .data(d => d)
    .join("rect")
    .attr("x", d => xScale(d.data.group))
    .attr("y", d => yScale(d[1]))
    .attr("height", d => yScale(d[0]) - yScale(d[1]))
    .attr("width", xScale.bandwidth());
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### Grouped bar chart

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const categories = Object.keys(data[0]).filter(k => k !== 'group');
  
  const x0Scale = d3.scaleBand()
    .domain(data.map(d => d.group))
    .range([0, innerWidth])
    .padding(0.1);
  
  const x1Scale = d3.scaleBand()
    .domain(categories)
    .range([0, x0Scale.bandwidth()])
    .padding(0.05);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => Math.max(...categories.map(c => d[c])))])
    .range([innerHeight, 0]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  const group = g.selectAll("g")
    .data(data)
    .join("g")
    .attr("transform", d => `translate(${x0Scale(d.group)},0)`);
  
  group.selectAll("rect")
    .data(d => categories.map(key => ({ key, value: d[key] })))
    .join("rect")
    .attr("x", d => x1Scale(d.key))
    .attr("y", d => yScale(d.value))
    .attr("width", x1Scale.bandwidth())
    .attr("height", d => innerHeight - yScale(d.value))
    .attr("fill", d => colourScale(d.key));
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(x0Scale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

### Bubble chart

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]);
  
  const sizeScale = d3.scaleSqrt()
    .domain([0, d3.max(data, d => d.size)])
    .range([0, 50]);
  
  const colourScale = d3.scaleOrdinal(d3.schemeCategory10);
  
  g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", d => sizeScale(d.size))
    .attr("fill", d => colourScale(d.category))
    .attr("opacity", 0.6)
    .attr("stroke", "white")
    .attr("stroke-width", 2);
  
  g.append("g")
    .attr("transform", `translate(0,${innerHeight})`)
    .call(d3.axisBottom(xScale));
  
  g.append("g")
    .call(d3.axisLeft(yScale));
    
}, [data]);
```

## Geographic visualisations

### Basic map with points

```javascript
useEffect(() => {
  if (!geoData || !pointData) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const projection = d3.geoMercator()
    .fitSize([width, height], geoData);
  
  const pathGenerator = d3.geoPath().projection(projection);
  
  // Draw map
  svg.selectAll("path")
    .data(geoData.features)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", "#e0e0e0")
    .attr("stroke", "#999")
    .attr("stroke-width", 0.5);
  
  // Draw points
  svg.selectAll("circle")
    .data(pointData)
    .join("circle")
    .attr("cx", d => projection([d.longitude, d.latitude])[0])
    .attr("cy", d => projection([d.longitude, d.latitude])[1])
    .attr("r", 5)
    .attr("fill", "steelblue")
    .attr("opacity", 0.7);
    
}, [geoData, pointData]);
```

### Choropleth map

```javascript
useEffect(() => {
  if (!geoData || !valueData) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 600;
  
  const projection = d3.geoMercator()
    .fitSize([width, height], geoData);
  
  const pathGenerator = d3.geoPath().projection(projection);
  
  // Create value lookup
  const valueLookup = new Map(valueData.map(d => [d.id, d.value]));
  
  // Colour scale
  const colourScale = d3.scaleSequential(d3.interpolateBlues)
    .domain([0, d3.max(valueData, d => d.value)]);
  
  svg.selectAll("path")
    .data(geoData.features)
    .join("path")
    .attr("d", pathGenerator)
    .attr("fill", d => {
      const value = valueLookup.get(d.id);
      return value ? colourScale(value) : "#e0e0e0";
    })
    .attr("stroke", "#999")
    .attr("stroke-width", 0.5);
    
}, [geoData, valueData]);
```

## Advanced interactions

### Brush and zoom

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  svg.selectAll("*").remove();
  
  const width = 800;
  const height = 400;
  const margin = { top: 20, right: 30, bottom: 40, left: 50 };
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  
  const xScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.x)])
    .range([0, innerWidth]);
  
  const yScale = d3.scaleLinear()
    .domain([0, d3.max(data, d => d.y)])
    .range([innerHeight, 0]);
  
  const g = svg.append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);
  
  const circles = g.selectAll("circle")
    .data(data)
    .join("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 5)
    .attr("fill", "steelblue");
  
  // Add brush
  const brush = d3.brush()
    .extent([[0, 0], [innerWidth, innerHeight]])
    .on("start brush", (event) => {
      if (!event.selection) return;
      
      const [[x0, y0], [x1, y1]] = event.selection;
      
      circles.attr("fill", d => {
        const cx = xScale(d.x);
        const cy = yScale(d.y);
        return (cx >= x0 && cx <= x1 && cy >= y0 && cy <= y1) 
          ? "orange" 
          : "steelblue";
      });
    });
  
  g.append("g")
    .attr("class", "brush")
    .call(brush);
    
}, [data]);
```

### Linked brushing between charts

```javascript
function LinkedCharts({ data }) {
  const [selectedPoints, setSelectedPoints] = useState(new Set());
  const svg1Ref = useRef();
  const svg2Ref = useRef();
  
  useEffect(() => {
    // Chart 1: Scatter plot
    const svg1 = d3.select(svg1Ref.current);
    svg1.selectAll("*").remove();
    
    // ... create first chart ...
    
    const circles1 = svg1.selectAll("circle")
      .data(data)
      .join("circle")
      .attr("fill", d => selectedPoints.has(d.id) ? "orange" : "steelblue");
    
    // Chart 2: Bar chart
    const svg2 = d3.select(svg2Ref.current);
    svg2.selectAll("*").remove();
    
    // ... create second chart ...
    
    const bars = svg2.selectAll("rect")
      .data(data)
      .join("rect")
      .attr("fill", d => selectedPoints.has(d.id) ? "orange" : "steelblue");
    
    // Add brush to first chart
    const brush = d3.brush()
      .on("start brush end", (event) => {
        if (!event.selection) {
          setSelectedPoints(new Set());
          return;
        }
        
        const [[x0, y0], [x1, y1]] = event.selection;
        const selected = new Set();
        
        data.forEach(d => {
          const x = xScale(d.x);
          const y = yScale(d.y);
          if (x >= x0 && x <= x1 && y >= y0 && y <= y1) {
            selected.add(d.id);
          }
        });
        
        setSelectedPoints(selected);
      });
    
    svg1.append("g").call(brush);
    
  }, [data, selectedPoints]);
  
  return (
    <div>
      <svg ref={svg1Ref} width="400" height="300" />
      <svg ref={svg2Ref} width="400" height="300" />
    </div>
  );
}
```

## Animation patterns

### Enter, update, exit with transitions

```javascript
useEffect(() => {
  if (!data || data.length === 0) return;
  
  const svg = d3.select(svgRef.current);
  
  const circles = svg.selectAll("circle")
    .data(data, d => d.id); // Key function for object constancy
  
  // EXIT: Remove old elements
  circles.exit()
    .transition()
    .duration(500)
    .attr("r", 0)
    .remove();
  
  // UPDATE: Modify existing elements
  circles
    .transition()
    .duration(500)
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("fill", "steelblue");
  
  // ENTER: Add new elements
  circles.enter()
    .append("circle")
    .attr("cx", d => xScale(d.x))
    .attr("cy", d => yScale(d.y))
    .attr("r", 0)
    .attr("fill", "steelblue")
    .transition()
    .duration(500)
    .attr("r", 5);
    
}, [data]);
```

### Path morphing

```javascript
useEffect(() => {
  if (!data1 || !data2) return;
  
  const svg = d3.select(svgRef.current);
  
  const line = d3.line()
    .x(d => xScale(d.x))
    .y(d => yScale(d.y))
    .curve(d3.curveMonotoneX);
  
  const path = svg.select("path");
  
  // Morph from data1 to data2
  path
    .datum(data1)
    .attr("d", line)
    .transition()
    .duration(1000)
    .attrTween("d", function() {
      const previous = d3.select(this).attr("d");
      const current = line(data2);
      return d3.interpolatePath(previous, current);
    });
    
}, [data1, data2]);
```

## Label collision patterns

Reusable patterns for preventing text overlap across all chart types. These should be applied by default, not as an afterthought.

### Radial label gating (chord, sunburst, pie, donut)

```javascript
// Define thresholds based on chart type and label content
const LABEL_THRESHOLDS = {
  nameLabel: 0.08,    // radians — short category names
  tickMark: 0.3,      // radians — tick lines only
  tickText: 0.5,      // radians — tick lines + numbers
  detailLabel: 0.8,   // radians — longer descriptions
};

// Apply gating: filter before appending text
group.filter(d => (d.endAngle - d.startAngle) > LABEL_THRESHOLDS.nameLabel)
  .append("text")
  .text(d => d.data.name);

// For sunburst: also check radial depth (inner rings have less circumference)
labels.filter(d => {
  const arcLength = (d.x1 - d.x0) * (d.y0 + d.y1) / 2; // approx pixel arc length
  const textWidth = d.data.name.length * fontSize * 0.6;
  return arcLength > textWidth + 8; // 8px padding
});
```

### Separate radial label lanes

```javascript
// When a radial chart has both name labels and numeric labels,
// place them in distinct radial bands with clear separation.
const outerRadius = 200;
const TICK_LANE = outerRadius + 4;         // ticks hug the arc
const TICK_TEXT_LANE = outerRadius + 10;    // tick numbers just outside
const NAME_LANE = outerRadius + 34;         // names in outer lane (20px+ gap)

// Never place two text systems in the same radial band
```

### Linear label collision (bar charts, axes, scatter)

```javascript
// Approach 1: Skip labels that don't fit
const bandWidth = xScale.bandwidth();
labels.text(d => {
  const textWidth = d.label.length * fontSize * 0.6;
  return textWidth < bandWidth - 4 ? d.label : '';
});

// Approach 2: Rotate labels that don't fit horizontally
const maxLabelWidth = d3.max(data, d => d.label.length) * fontSize * 0.6;
if (maxLabelWidth > bandWidth) {
  xAxisGroup.selectAll("text")
    .attr("transform", "rotate(-45)")
    .attr("text-anchor", "end")
    .attr("dx", "-0.5em")
    .attr("dy", "0.25em");
  // Also increase bottom margin to accommodate rotated labels
}

// Approach 3: Truncate with ellipsis
labels.text(d => {
  const maxChars = Math.floor(bandWidth / (fontSize * 0.6));
  return d.label.length > maxChars ? d.label.slice(0, maxChars - 1) + '...' : d.label;
});
```

### Post-render overlap resolution

```javascript
// Use getBBox() to detect actual rendered overlap and nudge labels apart.
// Works for any chart type. Apply after all labels are rendered.
function resolveVerticalOverlaps(labelSelection, minGap = 4) {
  const entries = [];
  labelSelection.each(function() {
    const bbox = this.getBBox();
    entries.push({ node: this, y: bbox.y, h: bbox.height });
  });
  
  entries.sort((a, b) => a.y - b.y);
  
  for (let i = 1; i < entries.length; i++) {
    const prev = entries[i - 1];
    const curr = entries[i];
    const overlap = (prev.y + prev.h + minGap) - curr.y;
    if (overlap > 0) {
      const el = d3.select(curr.node);
      const currentY = parseFloat(el.attr('y') || 0);
      el.attr('y', currentY + overlap);
      curr.y += overlap; // update for cascading
    }
  }
}

// For radial labels, convert to angular overlap:
function resolveRadialOverlaps(labelSelection, minAngleGap = 0.06) {
  const entries = [];
  labelSelection.each(function(d) {
    entries.push({ node: this, angle: d.angle, d });
  });
  
  entries.sort((a, b) => a.angle - b.angle);
  
  for (let i = 1; i < entries.length; i++) {
    const gap = entries[i].angle - entries[i - 1].angle;
    if (gap < minAngleGap) {
      // Hide the label on the smaller arc
      const smaller = entries[i].d.value < entries[i - 1].d.value ? entries[i] : entries[i - 1];
      d3.select(smaller.node).attr('opacity', 0);
    }
  }
}
```

### Chart chrome layout template

```html
<!-- GOOD: all chrome in document flow, chart fills remainder -->
<style>
  body { display: flex; flex-direction: column; height: 100vh; margin: 0; }
  .header { padding: 24px 32px 8px; flex-shrink: 0; }
  .legend { padding: 4px 32px 12px; flex-shrink: 0; }
  .breadcrumb { padding: 6px 32px; flex-shrink: 0; }
  #chart { flex: 1; min-height: 0; overflow: hidden; }
</style>

<script>
  // Compute chart dimensions from actual remaining space
  function getChartDimensions() {
    const chartEl = document.getElementById('chart');
    const { width, height } = chartEl.getBoundingClientRect();
    return { width, height };
  }
</script>
```
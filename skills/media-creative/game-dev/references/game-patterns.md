# Game Patterns Reference

Common algorithms and patterns for HTML5 Canvas games.

## Enemy AI Patterns

### Patrol
```javascript
const enemy = {
  waypoints: [{x:100,y:100}, {x:200,y:100}, {x:200,y:200}],
  current: 0,
  speed: 50,
  pauseTime: 0
};

function updatePatrol(enemy, dt) {
  if (enemy.pauseTime > 0) {
    enemy.pauseTime -= dt;
    return;
  }
  
  const target = enemy.waypoints[enemy.current];
  const dx = target.x - enemy.x;
  const dy = target.y - enemy.y;
  const dist = Math.hypot(dx, dy);
  
  if (dist < 5) {
    enemy.current = (enemy.current + 1) % enemy.waypoints.length;
    enemy.pauseTime = 1.0; // Pause 1 second at waypoint
  } else {
    enemy.x += (dx / dist) * enemy.speed * dt;
    enemy.y += (dy / dist) * enemy.speed * dt;
  }
}
```

### Chase (with radius)
```javascript
function updateChase(enemy, player, dt) {
  const dx = player.x - enemy.x;
  const dy = player.y - enemy.y;
  const dist = Math.hypot(dx, dy);
  
  if (dist < enemy.chaseRadius && dist > enemy.stopRadius) {
    enemy.x += (dx / dist) * enemy.speed * dt;
    enemy.y += (dy / dist) * enemy.speed * dt;
  }
}
```

### Flee (when low health)
```javascript
function updateFlee(enemy, player, dt) {
  if (enemy.health / enemy.maxHealth > 0.3) return;
  
  const dx = enemy.x - player.x; // Note: reversed from chase
  const dy = enemy.y - player.y;
  const dist = Math.hypot(dx, dy);
  
  if (dist < enemy.fleeRadius) {
    enemy.x += (dx / dist) * enemy.speed * dt;
    enemy.y += (dy / dist) * enemy.speed * dt;
  }
}
```

## Camera Systems

### Follow with Dead Zone
```javascript
const camera = {
  x: 0, y: 0,
  w: 360, h: 640,
  deadZone: { x: 100, y: 150, w: 160, h: 340 },
  smoothing: 10
};

function updateCamera(camera, target, dt, bounds) {
  let targetX = camera.x;
  let targetY = camera.y;
  
  // Check if target outside dead zone
  if (target.x < camera.x + camera.deadZone.x) {
    targetX = target.x - camera.deadZone.x;
  } else if (target.x > camera.x + camera.deadZone.x + camera.deadZone.w) {
    targetX = target.x - camera.deadZone.x - camera.deadZone.w;
  }
  
  if (target.y < camera.y + camera.deadZone.y) {
    targetY = target.y - camera.deadZone.y;
  } else if (target.y > camera.y + camera.deadZone.y + camera.deadZone.h) {
    targetY = target.y - camera.deadZone.y - camera.deadZone.h;
  }
  
  // Smooth movement
  camera.x += (targetX - camera.x) * Math.min(1, dt * camera.smoothing);
  camera.y += (targetY - camera.y) * Math.min(1, dt * camera.smoothing);
  
  // Clamp to world bounds
  camera.x = Math.max(bounds.minX, Math.min(bounds.maxX - camera.w, camera.x));
  camera.y = Math.max(bounds.minY, Math.min(bounds.maxY - camera.h, camera.y));
  
  // Integer rounding for pixel-perfect
  camera.x = Math.round(camera.x);
  camera.y = Math.round(camera.y);
}
```

## A* Pathfinding (Grid)

```javascript
function astar(grid, start, goal) {
  const h = (a,b) => Math.abs(a.x-b.x) + Math.abs(a.y-b.y);
  const key = n => `${n.x},${n.y}`;
  const open = new Set([key(start)]);
  const came = new Map();
  const g = new Map([[key(start), 0]]);
  const f = new Map([[key(start), h(start, goal)]]);
  
  function neighbors(n) {
    const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
    return dirs
      .map(([dx,dy]) => ({x: n.x+dx, y: n.y+dy}))
      .filter(nb => !grid.blocked(nb.x, nb.y));
  }
  
  while (open.size) {
    // Find lowest f-score
    let curK = null, curF = Infinity;
    for (const k of open) {
      const val = f.get(k) ?? Infinity;
      if (val < curF) { curF = val; curK = k; }
    }
    
    const [cx, cy] = curK.split(',').map(Number);
    const cur = {x: cx, y: cy};
    
    if (cx === goal.x && cy === goal.y) {
      // Reconstruct path
      const path = [cur];
      while (came.has(key(path[0]))) {
        path.unshift(came.get(key(path[0])));
      }
      return path;
    }
    
    open.delete(curK);
    
    for (const nb of neighbors(cur)) {
      const nk = key(nb);
      const tentative = (g.get(curK) || Infinity) + 1;
      
      if (tentative < (g.get(nk) || Infinity)) {
        came.set(nk, cur);
        g.set(nk, tentative);
        f.set(nk, tentative + h(nb, goal));
        open.add(nk);
      }
    }
  }
  
  return null; // No path found
}
```

## Procedural Generation

### Simple Room Generation
```javascript
function generateDungeon(w, h, numRooms) {
  const grid = Array(h).fill(0).map(() => Array(w).fill(1)); // 1 = wall
  const rooms = [];
  
  for (let i = 0; i < numRooms; i++) {
    const rw = 5 + Math.floor(Math.random() * 5);
    const rh = 5 + Math.floor(Math.random() * 5);
    const rx = Math.floor(Math.random() * (w - rw - 2)) + 1;
    const ry = Math.floor(Math.random() * (h - rh - 2)) + 1;
    
    // Carve room
    for (let y = ry; y < ry + rh; y++) {
      for (let x = rx; x < rx + rw; x++) {
        grid[y][x] = 0; // 0 = floor
      }
    }
    
    rooms.push({x: rx, y: ry, w: rw, h: rh});
    
    // Connect to previous room
    if (i > 0) {
      const prev = rooms[i-1];
      const px = prev.x + Math.floor(prev.w/2);
      const py = prev.y + Math.floor(prev.h/2);
      const cx = rx + Math.floor(rw/2);
      const cy = ry + Math.floor(rh/2);
      
      // Horizontal corridor
      for (let x = Math.min(px, cx); x <= Math.max(px, cx); x++) {
        grid[py][x] = 0;
      }
      // Vertical corridor
      for (let y = Math.min(py, cy); y <= Math.max(py, cy); y++) {
        grid[y][cx] = 0;
      }
    }
  }
  
  return {grid, rooms};
}
```

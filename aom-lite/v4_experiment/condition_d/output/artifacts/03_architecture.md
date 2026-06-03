## 技术架构设计

### 1. 技术选型（≤50字）
- 渲染方式：Canvas
- 为什么：单文件内高效绘制游戏元素，性能优于DOM操作，适合像素级控制。

### 2. 模块划分（≤200字）
```
游戏引擎模块：管理游戏状态、逻辑更新、碰撞检测、计分
渲染模块：负责Canvas绑定、绘制蛇、食物、分数及界面
UI/输入模块：处理开始/结束界面、响应键盘与触摸事件、切换游戏阶段
数据存储模块：使用localStorage管理本地最高分
```

### 3. 核心数据结构（≤150字）
```javascript
// 蛇的数据结构
const snake = {
  body: [{x, y}], // 身体段坐标数组，头部在[0]
  direction: {x, y} // 当前移动方向向量
};

// 食物的数据结构
const food = {x, y}; // 坐标

// 游戏状态
const gameState = {
  stage: 'start' | 'playing' | 'over', // 当前阶段
  score: 0,
  highScore: 0,
  isPaused: false,
  canvas: {width, height}, // 画布逻辑尺寸
  gridSize: 20 // 网格单元大小(像素)
};
```

### 4. 关键接口（≤200字）
```javascript
// 游戏引擎模块
function initGame() // 重置状态，生成初始蛇和食物
function updateGame() // 驱动游戏主循环：移动蛇、检测碰撞、生成食物、计分
function handleInput(key) // 处理方向输入，防止反向移动

// 渲染模块
function render() // 清屏并绘制当前游戏状态（蛇、食物、分数）
function drawStartScreen() // 绘制开始界面
function drawGameOverScreen() // 绘制结束界面

// UI/输入模块
function setupEventListeners() // 绑定键盘、触摸、窗口事件
function switchStage(stage) // 切换游戏阶段并更新UI
```

### 5. 实现要点（≤100字）
- 关键算法：蛇移动通过向数组头部添加新坐标并移除尾部实现；碰撞检测检查头部与边界/自身坐标是否重合。
- 性能考虑：使用`requestAnimationFrame`控制游戏循环；Canvas尺寸基于视口动态计算以保证响应式。
- 边界处理：撞墙/撞自身触发游戏结束状态；窗口失焦时暂停游戏循环；反向输入被忽略。
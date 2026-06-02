## 技术架构设计

### 1. 技术选型（≤50字）
- 渲染方式：**Canvas**
- 为什么：适合高频绘图的游戏场景，性能优于DOM，且能轻松实现震动、闪烁等视觉效果。

### 2. 模块划分（≤200字）
```
GameState：管理游戏核心数据（蛇、食物、分数、速度）和逻辑更新。
Renderer：负责根据GameState将游戏画面绘制到Canvas上。
InputHandler：抽象并统一处理键盘、虚拟按键和触屏滑动的输入。
ScreenManager：控制开始、游戏、结束三个界面的显示与切换。
GameController：主控制器，协调其他模块，驱动游戏主循环。
```

### 3. 核心数据结构（≤150字）
```javascript
// 蛇：由坐标点组成的数组，数组头部为蛇头
snake: [{x, y}, ...],
// 食物：单个坐标点
food: {x, y},
// 游戏状态
gameState: {
  score: 0,
  speed: 1, // 基础速度系数，随分数增加
  isRunning: false,
  currentScreen: 'start' // 'start' | 'playing' | 'end'
}
```

### 4. 关键接口（≤200字）
```javascript
// 模块间的核心函数签名
GameController.initGame(): void // 初始化/重置所有游戏状态与界面
GameController.startGameLoop(): void // 启动requestAnimationFrame主循环
GameState.update(): boolean // 更新蛇位移、碰撞检测、得分，返回游戏是否结束
Renderer.render(): void // 清屏并根据当前GameState绘制所有元素
InputHandler.bindControls(): void // 初始化并绑定所有输入事件监听器
ScreenManager.switchTo(screen): void // 切换到指定界面，并显示/隐藏相应DOM元素
```

### 5. 实现要点（≤100字）
- **关键算法**：蛇移动为数组头增尾删；碰撞检测使用网格坐标比较；速度随分数线性增长。
- **性能考虑**：仅在`update`和`render`时操作状态与画布；使用`requestAnimationFrame`保证流畅。
- **边界处理**：蛇头坐标超出网格范围即判负；移动时禁止180度反向输入。
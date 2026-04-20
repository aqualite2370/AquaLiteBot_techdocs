# 🚀 AqualiteBot_Doc | 奶茶酱 帮助文档

一个基于 **Vue 3** 和 **FastAPI** 的现代化技术文档系统，融合了赛博朋克风格的极致动效体验和完美的响应式设计。

## ✨ 核心动效特性

### 🎯 Center-Splash（中央溅射进场）
元素从屏幕中央向外**爆炸式溅射**到原位，使用：
- **3D 变换**：`translate3d` + `rotate` + `scale`
- **弹簧物理**：自定义贝塞尔曲线 `cubic-bezier(0.34, 1.56, 0.64, 1)` 模拟回弹效果
- **分层动画**：导航、头部、内容区错开时间节点，形成先后顺序

```css
/* 未加载状态：聚集在屏幕中央 */
.pre-splash .nav-target {
  transform: translate3d(60vw, 50vh, -500px) scale(0.1) rotate(45deg);
  opacity: 0;
}

/* 加载完毕：爆炸式归位 */
.post-splash .splash-target {
  transform: translate3d(0, 0, 0) scale(1) rotate(0deg);
  opacity: 1;
}
```

### ⚡ Fast-Cut-in（极速切入转场）
摒弃传统淡入淡出，使用**倾斜 + 模糊 + 位移**的硬切效果：
- **Skew 倾斜**：`skewX(-15deg)` 营造速度感
- **运动模糊**：`filter: blur(10px)` 模拟高速移动
- **极速曲线**：`cubic-bezier(0.175, 0.885, 0.32, 1.275)` 快速切入

```css
.fast-cut-enter-from {
  opacity: 0;
  transform: translateX(60px) skewX(-15deg) scale(0.95);
  filter: blur(10px);
}
```

### 🎨 视觉设计
- **玻璃态效果**：毛玻璃背景 + 半透明边框
- **赛博朋克配色**：深色主题 + 霓虹蓝 (#0ea5e9)
- **科技感骨架屏**：渐变脉冲动画覆盖网络延迟
- **GPU 加速**：使用 `transform` 和 `opacity` 优化性能

## 📱 响应式设计

- ✅ 完美适配 PC、平板、移动设备
- ✅ 移动优先策略（Mobile First）
- ✅ 触摸优化的交互体验
- ✅ 流畅的断点切换（lg: 1024px）

## 🔧 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| **前端框架** | Vue 3 | Composition API + `<script setup>` |
| **构建工具** | Vite | 极速热更新 + ES Module |
| **路由** | Vue Router 4 | 单页应用路由管理 |
| **样式** | Tailwind CSS | 原子化 CSS + CDN 加载 |
| **图标** | Remix Icon | 现代化图标库 |
| **后端框架** | FastAPI | 高性能异步 Python Web 框架 |
| **服务器** | Uvicorn | ASGI 服务器 |
| **Markdown** | Marked.js | Markdown 渲染引擎 |

## 📦 项目结构

```
vue_fastapi_技术文档/
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI 主程序
│   ├── requirements.txt    # Python 依赖
│   └── venv/               # 虚拟环境（自动创建）
├── frontend/               # 前端应用
│   ├── src/
│   │   ├── api/           # API 接口封装
│   │   ├── assets/        # 静态资源
│   │   ├── router/        # 路由配置
│   │   ├── views/         # 页面组件
│   │   │   ├── Home.vue   # 首页
│   │   │   └── DocDetail.vue  # 文档详情
│   │   ├── App.vue        # 根组件（含动效系统）
│   │   └── main.js        # 入口文件
│   ├── index.html         # HTML 模板
│   ├── package.json       # 前端依赖
│   └── vite.config.js     # Vite 配置
├── 启动项目.bat            # 一键启动脚本
└── README.md              # 项目说明
```

## 🚀 快速开始

### 方式一：一键启动（推荐）⭐

**双击运行** `启动项目.bat`，脚本会自动：
1. ✅ 检查环境（Python、Node.js）
2. ✅ 创建虚拟环境并安装后端依赖
3. ✅ 安装前端依赖
4. ✅ 启动后端服务（端口 8000）
5. ✅ 启动前端服务（端口 3000）
6. ✅ 自动打开浏览器

### 方式二：手动启动

#### 1. 启动后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py
```

后端服务：`http://localhost:8000`

#### 2. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端服务：`http://localhost:3000`

## 📖 API 文档

启动后端后，访问以下地址查看 API 文档：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 主要接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/categories` | GET | 获取所有分类 |
| `/api/documents` | GET | 获取文档列表 |
| `/api/documents/{id}` | GET | 获取文档详情 |
| `/api/search?q={query}` | GET | 搜索文档 |

## 🎯 动效实现原理

### 1. 溅射效果核心代码

```javascript
// 计算元素从中央到目标位置的偏移
const triggerSplash = (element) => {
  const centerX = window.innerWidth / 2
  const centerY = window.innerHeight / 2
  const rect = element.getBoundingClientRect()
  const targetX = rect.left + rect.width / 2
  const targetY = rect.top + rect.height / 2
  
  const deltaX = centerX - targetX
  const deltaY = centerY - targetY
  const rotation = (Math.random() - 0.5) * 360
  
  element.style.setProperty('--splash-x', `${deltaX}px`)
  element.style.setProperty('--splash-y', `${deltaY}px`)
  element.style.setProperty('--splash-rotation', `${rotation}deg`)
  
  element.classList.add('splash-active')
}
```

### 2. 页面转场动效

```vue
<router-view v-slot="{ Component }">
  <transition name="fast-cut" mode="out-in">
    <component :is="Component" />
  </transition>
</router-view>
```

### 3. 骨架屏动画

```css
@keyframes tech-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton {
  background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
  background-size: 400% 100%;
  animation: tech-pulse 1.5s ease-in-out infinite;
}
```

## 🎨 设计理念

### 专业设计师精神 🎨
- 精心设计的配色方案（赛博朋克主题）
- 流畅的动画曲线（物理模拟）
- 统一的视觉语言
- 细腻的交互反馈

### 全栈工程师精神 💻
- 清晰的代码结构
- 性能优化（GPU 加速）
- 错误处理机制
- 可维护的架构
- 前后端分离

## 🔧 环境要求

- **Python**: 3.8+
- **Node.js**: 16+
- **浏览器**: 现代浏览器（支持 CSS3 和 ES6+）

## 📝 开发说明

### 添加新文档

在 `backend/main.py` 的 `DOCUMENTS` 列表中添加：

```python
{
    "id": "your-doc-id",
    "title": "文档标题",
    "content": """# Markdown 内容""",
    "category": "分类ID",
    "tags": ["标签1", "标签2"],
    "order": 5
}
```

### 自定义动效参数

在 `frontend/src/App.vue` 中调整：

```css
/* 调整溅射速度 */
.splash-target {
  transition: transform 1.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

/* 调整切入速度 */
.fast-cut-enter-active {
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
```

## 🌟 特色功能

1. **中央溅射进场** - 页面加载时的震撼视觉效果
2. **极速切入转场** - 赛博朋克风格的页面切换
3. **实时骨架屏** - 优雅的加载状态展示
4. **玻璃态设计** - 现代化的毛玻璃效果
5. **完美响应式** - 无缝适配各种设备
6. **Markdown 支持** - 完整的 Markdown 语法支持
7. **API 驱动** - 前后端分离架构

## 📄 许可证

MIT License

## 👨‍💻 致谢

- 设计灵感来源于赛博朋克和极客文化
- 动效理念参考了现代 UI/UX 最佳实践
- 感谢 Vue、FastAPI、Tailwind CSS 等开源社区

---

**享受极致的动效体验！** ✨🚀

# Design System — 阿福健康

## Product Context
- **What this is:** AI 驱动的智能健康助手，提供健康问答、体检报告分析、个人健康管理等服务
- **Who it's for:** 关注自身及家人健康的普通用户，包括需要管理慢病、解读体检报告的中老年人群
- **Space/industry:** 数字健康管理，参考产品：丁香医生、微医、Apple Health、Calm
- **Project type:** 移动端 Web App（uni-app 跨平台）

## Aesthetic Direction
- **Direction:** Organic Warmth（有机温暖）
- **Decoration level:** intentional — 柔和的背景纹理、卡片阴影层次、微妙的渐变
- **Mood:** 像一位温暖的专业医生朋友 — 值得信赖但不冷冰冰，关怀但不煽情。用户打开 app 应该感到安心和被照顾。
- **Reference:** Apple Health（数据可视化）、Calm（色彩温度）、丁香医生（医疗信任感）

## Typography
- **Display/Hero:** Plus Jakarta Sans — 几何无衬线，现代但温暖，线条柔和不尖锐，适合健康场景的友好感
- **Body:** Source Sans 3 — 优秀的中英文混排可读性，Adobe 出品，医疗文档级别的清晰度
- **UI/Labels:** 同 Body
- **Data/Tables:** DM Sans — 支持 tabular-nums，数字对齐工整，适合体检指标展示
- **Code:** JetBrains Mono — 清晰的等宽字体，用于代码片段或技术信息
- **Loading:** Google Fonts CDN，配合 `font-display: swap` 确保首屏不阻塞
- **Fallback:** `'PingFang SC', 'Noto Sans SC', 'Microsoft YaHei', sans-serif`
- **Scale（rpx）:**
  - 48rpx — 页面主标题
  - 32rpx — 卡片标题 / 区域标题
  - 28rpx — 正文（基准）
  - 26rpx — 次要正文
  - 24rpx — 辅助文字 / 元信息
  - 22rpx — 标注 / 脚注
  - 20rpx — 最小文字

## Color
- **Approach:** balanced — 主色 + 辅助色 + 语义色，色彩有意义而非装饰
- **Primary:** `#3B82A0` — 沉稳的青蓝色，传递医疗专业感和信任，比通用蓝 #4a90d9 更成熟
- **Primary Light:** `#5A9BB8` — 悬停、选中态
- **Primary Dark:** `#2D6A82` — 按下态、强调
- **Primary BG:** `#E8F4F8` — 主色最浅底色，用于标签、badge 背景
- **Accent Green:** `#6FCF97` — 健康正向指标、成功状态、达成目标
- **Accent Orange:** `#F2994A` — 温暖提醒、关注项、进行中状态
- **Neutrals (warm):**
  - `#F8F6F3` — 页面底色（暖灰，取代冷灰 #f5f7fa）
  - `#FAF9F7` — 表面色 / 卡片内嵌背景
  - `#FFFFFF` — 卡片背景
  - `#E8E5E0` — 边框、分割线
  - `#2C2C2E` — 主文字（深暖黑，取代纯 #333）
  - `#6B6B70` — 次要文字
  - `#A0A0A5` — 占位符文字
- **Semantic (Traffic Light):**
  - 异常偏高/紧急: `#E07070`（柔化红，不刺眼）
  - 需关注/偏高: `#E8B84A`（温暖琥珀）
  - 复查随访: `#5A9BB8`（跟随主色的蓝）
  - 正常范围: `#5CB87A`（自然绿）
  - Success: `#5CB87A`
  - Warning: `#E8B84A`
  - Error: `#E07070`
  - Info: `#5A9BB8`
- **Dark mode strategy:**
  - 背景降为 `#141416`（深暖黑，非纯黑）
  - 卡片 `#1E1E22`，表面 `#26262A`
  - 主色提亮至 `#5A9BB8`，降低饱和度 10%
  - 文字反转：主 `#F0EDE8`，次 `#9A9A9E`
  - 边框 `#333338`
  - 交通灯颜色整体提亮 15%

## Spacing
- **Base unit:** 8rpx
- **Density:** comfortable — 不挤不松，适合健康场景的从容感
- **Scale:**
  - 8rpx — xs（紧凑间距）
  - 16rpx — sm（元素内间距）
  - 24rpx — md（标准间距）
  - 32rpx — lg（区域间距）
  - 48rpx — xl（大区域分隔）
  - 64rpx — 2xl（页面级分隔）

## Layout
- **Approach:** grid-disciplined — 卡片式布局，健康类产品的标准范式
- **Grid:** 移动端单栏，快捷操作 4 列网格，功能入口 2-4 列
- **Max content width:** 750rpx（uni-app 标准满宽）
- **Page padding:** 24rpx top/bottom, 32rpx left/right
- **Card padding:** 28rpx
- **Border radius (rpx):**
  - sm: 12rpx — 小元素（tag、badge）
  - md: 20rpx — 卡片、输入框
  - lg: 28rpx — 大卡片、弹窗
  - pill: 999rpx — 按钮、搜索框
- **Shadow:** `0 2rpx 12rpx rgba(0, 0, 0, 0.04)` — 统一的柔和阴影

## Motion
- **Approach:** minimal-functional — 只添加有助于理解状态变化的动效，不为炫技
- **Easing:**
  - enter: `cubic-bezier(0.16, 1, 0.3, 1)` — 弹性进入
  - exit: `cubic-bezier(0.7, 0, 0.84, 0)` — 快速退出
  - move: `ease-in-out` — 位移过渡
- **Duration:**
  - micro: 50-100ms — 按钮反馈、开关切换
  - short: 150-200ms — 卡片入场、页面切换
  - medium: 250-350ms — 弹窗展开、列表加载
  - long: 400-700ms — 骨架屏渐显、首次加载
- **Patterns:**
  - 卡片入场：从下方 translateY(20rpx) + opacity 0 → 原位 + opacity 1
  - 骨架屏：pulse 动画，1.5s 循环
  - 打字光标：blink 动画，0.8s 循环（保持现有）
  - 语音波形：wave 动画（保持现有）

## Iconography
- **Style:** Emoji 字符（保持现有方案）
- **Rationale:** uni-app 跨平台一致性好，无需额外字体文件，中老年用户熟悉度高
- **Future:** 如需更专业的图标体系，可引入 iconify 或自定义 SVG sprite

## Elder Mode（长辈模式）
- 基础字号从 28rpx 提升至 36rpx
- 触摸目标最小 96rpx
- 按钮高度 108rpx
- 间距整体放大 25%
- 自动开启语音播放
- 简化界面层级

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-05-11 | 初始设计系统建立 | 基于产品定位和竞品研究，确定 Organic Warmth 方向 |
| 2026-05-11 | 主色从 #4a90d9 改为 #3B82A0 | 更沉稳、更有医疗信任感，区分于通用蓝色 |
| 2026-05-11 | 底色从冷灰改为暖灰 #F8F6F3 | 传递「家的温度」而非「医院的冷感」，差异化竞品 |
| 2026-05-11 | 引入 Google Fonts 自定义字体 | 品牌辨识度提升，Plus Jakarta Sans 温暖几何风格匹配产品调性 |
| 2026-05-11 | 圆角从 8/16/24 调整为 12/20/28 | 更柔和，配合有机温暖美学方向 |
| 2026-05-11 | 交通灯颜色柔化 | 降低红/黄的刺激感，健康场景下用户情绪敏感 |

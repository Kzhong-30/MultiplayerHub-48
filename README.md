# 宠物社交平台

一个以宠物社交为核心的全栈应用，Vue 3 前端配合 Element Plus 组件库，FastAPI 后端驱动，SQLite/PostgreSQL 持久化数据。

## 功能特性

### 🐾 宠物档案管理
- 每位用户可为多只宠物建立独立档案
- 记录昵称、品种、生日、性别等基本信息
- 体重曲线图表展示（ECharts）
- 疫苗接种时间线管理
- 专属相册功能

### 📱 动态广场
- 支持发布宠物图文动态
- 附带话题标签分类
- 点赞、评论互动
- 按标签筛选内容
- 热门话题推荐

### 💘 智能配对
- 基于品种兼容性匹配
- 年龄相近度计算
- 地理位置距离测算
- 综合匹配分数（品种40% + 年龄30% + 距离30%）
- 推荐潜在"玩伴"
- 配对请求管理（接受/拒绝）

### 📚 宠物百科
- 常见品种养护指南
- 品种详情：性格特点、外观特征、喂养指南、健康问题等
- 疾病自查手册
- 疾病详情：症状、病因、诊断、治疗、预防

### 📍 附近宠物
- 基于地理坐标展示周边宠物
- 支持发起线下聚会邀约
- 聚会报名/取消报名
- 距离筛选（1-50公里）
- 聚会状态管理（即将开始/进行中/已结束）

### 🏥 服务导航
- 周边宠物医院
- 美容店
- 寄养中心
- 训练学校
- 用品商店
- 支持按类别筛选、距离/评分/价格排序
- 一键拨打电话、导航跳转

### 👤 个人中心
- 用户基本信息编辑
- 地理位置设置
- 我的动态管理
- 修改密码
- 数据统计展示

## 技术栈

### 后端
- **框架**: FastAPI 0.109.0
- **数据库**: SQLite (开发) / PostgreSQL (生产)
- **ORM**: SQLAlchemy 2.0.25
- **数据验证**: Pydantic 2.5.3
- **认证**: JWT (python-jose) + BCrypt
- **地理计算**: Geopy 2.4.1
- **服务器**: Uvicorn

### 前端
- **框架**: Vue 3.4 (Composition API)
- **UI 组件**: Element Plus 2.5
- **状态管理**: Pinia 2.1
- **路由**: Vue Router 4.2
- **HTTP 客户端**: Axios 1.6
- **图表**: ECharts 5.4
- **日期处理**: Day.js 1.11
- **构建工具**: Vite 5.0
- **样式**: SCSS

## 项目结构

```
.
├── backend/                    # 后端项目
│   ├── app/
│   │   ├── routers/           # API 路由
│   │   │   ├── auth.py        # 认证路由
│   │   │   ├── pets.py        # 宠物档案路由
│   │   │   ├── posts.py       # 动态广场路由
│   │   │   ├── comments.py    # 评论路由
│   │   │   ├── matches.py     # 智能配对路由
│   │   │   ├── encyclopedia.py # 宠物百科路由
│   │   │   ├── nearby.py      # 附近宠物路由
│   │   │   └── services.py    # 服务导航路由
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI 主入口
│   │   ├── models.py          # SQLAlchemy 数据模型
│   │   ├── schemas.py         # Pydantic 请求响应模型
│   │   ├── auth.py            # JWT 认证模块
│   │   ├── database.py        # 数据库连接配置
│   │   └── utils.py           # 匹配算法工具函数
│   ├── init_data.py           # 数据库初始化脚本
│   ├── requirements.txt       # Python 依赖
│   ├── .env                   # 环境变量
│   └── start.sh               # 后端启动脚本
│
├── frontend/                   # 前端项目
│   ├── src/
│   │   ├── api/               # API 服务层
│   │   │   └── index.js
│   │   ├── stores/            # Pinia 状态管理
│   │   │   ├── user.js
│   │   │   ├── pet.js
│   │   │   └── app.js
│   │   ├── router/            # Vue Router 路由
│   │   │   └── index.js
│   │   ├── styles/            # 全局样式
│   │   │   └── global.scss
│   │   ├── views/             # 页面组件
│   │   │   ├── Layout.vue
│   │   │   ├── Login.vue
│   │   │   ├── Register.vue
│   │   │   ├── Home.vue
│   │   │   ├── Pets.vue
│   │   │   ├── PetDetail.vue
│   │   │   ├── Posts.vue
│   │   │   ├── Matches.vue
│   │   │   ├── Encyclopedia.vue
│   │   │   ├── BreedDetail.vue
│   │   │   ├── DiseaseDetail.vue
│   │   │   ├── Nearby.vue
│   │   │   ├── Services.vue
│   │   │   └── Profile.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── start.sh               # 前端启动脚本
│
└── README.md
```

## 快速开始

### 前置要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 一键启动

#### 方式一：分别启动（推荐）

**1. 启动后端服务**
```bash
cd backend
chmod +x start.sh
./start.sh
```

后端服务将在 `http://localhost:8000` 启动

API 文档地址：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**2. 启动前端服务**
```bash
cd frontend
chmod +x start.sh
./start.sh
```

前端服务将在 `http://localhost:5173` 启动

#### 方式二：手动启动

**后端：**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python init_data.py
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**前端：**
```bash
cd frontend
npm install
npm run dev
```

### 测试账号

系统预置了以下测试账号：

| 用户名 | 密码 | 说明 |
|--------|------|------|
| admin | 123456 | 管理员，2只宠物 |
| user1 | 123456 | 普通用户，1只宠物 |
| user2 | 123456 | 普通用户，1只宠物 |

### 初始化数据

启动后端时会自动初始化以下测试数据：
- 3个测试用户
- 4只宠物（柯基、金毛、布偶、泰迪）
- 4条动态
- 4个品种百科
- 5种疾病指南
- 2个线下聚会

服务数据需要手动初始化：
- 登录后进入"服务导航"页面
- 点击"初始化数据"按钮
- 将创建5个测试服务机构

## 智能匹配算法说明

### 匹配分数计算公式

综合匹配分数 = (品种兼容性 × 0.4 + 年龄相近度 × 0.3 + 距离得分 × 0.3) × 100

### 品种兼容性

内置常见品种兼容性映射表，同一品种或相似品种兼容性更高：
- 同一品种：100%
- 相似品种（如金毛-拉布拉多）：80-90%
- 不同品种：50-70%

### 年龄相近度

基于年龄差计算，年龄越相近得分越高：
- 年龄差 ≤ 1岁：90-100%
- 年龄差 ≤ 3岁：70-89%
- 年龄差 ≤ 5岁：50-69%
- 年龄差 > 5岁：<50%

### 距离得分

基于 Haversine 公式计算球面距离：
- 距离 ≤ 1公里：100%
- 距离 ≤ 5公里：80-99%
- 距离 ≤ 10公里：60-79%
- 距离 ≤ 20公里：40-59%
- 距离 > 20公里：<40%

## 数据库切换

开发环境默认使用 SQLite，生产环境可切换到 PostgreSQL：

修改 `backend/.env` 文件：
```env
DATABASE_URL=postgresql://user:password@localhost:5432/pet_social
```

## API 接口列表

### 认证模块
- `POST /auth/register` - 用户注册
- `POST /auth/login` - 用户登录
- `GET /auth/me` - 获取当前用户信息
- `PUT /auth/me` - 更新当前用户信息

### 宠物档案
- `GET /pets` - 获取我的宠物列表
- `POST /pets` - 创建宠物档案
- `GET /pets/{id}` - 获取宠物详情
- `PUT /pets/{id}` - 更新宠物信息
- `DELETE /pets/{id}` - 删除宠物
- `POST /pets/{id}/weight` - 添加体重记录
- `POST /pets/{id}/vaccine` - 添加疫苗记录
- `POST /pets/{id}/photos` - 添加相册照片
- `DELETE /pets/{pet_id}/photos/{photo_id}` - 删除照片

### 动态广场
- `GET /posts` - 获取动态列表
- `POST /posts` - 发布动态
- `GET /posts/{id}` - 获取动态详情
- `PUT /posts/{id}` - 更新动态
- `DELETE /posts/{id}` - 删除动态
- `POST /posts/{id}/like` - 点赞/取消点赞
- `GET /posts/user/{user_id}` - 获取用户动态

### 评论管理
- `GET /comments/post/{post_id}` - 获取动态评论
- `POST /comments` - 发表评论
- `DELETE /comments/{id}` - 删除评论

### 智能配对
- `GET /matches/recommendations` - 获取配对推荐
- `POST /matches` - 发起配对请求
- `GET /matches/sent` - 获取我发起的请求
- `GET /matches/received` - 获取收到的请求
- `PUT /matches/{id}/accept` - 接受配对
- `PUT /matches/{id}/reject` - 拒绝配对

### 宠物百科
- `GET /encyclopedia/breeds` - 获取品种列表
- `GET /encyclopedia/breeds/{id}` - 获取品种详情
- `GET /encyclopedia/diseases` - 获取疾病列表
- `GET /encyclopedia/diseases/{id}` - 获取疾病详情

### 附近宠物
- `GET /nearby/pets` - 获取附近宠物
- `GET /nearby/meetups` - 获取附近聚会
- `POST /nearby/meetups` - 创建聚会
- `GET /nearby/meetups/{id}` - 获取聚会详情
- `POST /nearby/meetups/{id}/join` - 报名参加聚会
- `DELETE /nearby/meetups/{id}/join` - 取消报名

### 服务导航
- `GET /services` - 获取服务列表
- `GET /services/categories` - 获取服务分类
- `GET /services/{id}` - 获取服务详情
- `POST /services/seed` - 初始化服务数据

## 开发说明

### 后端开发

添加新的 API 路由：
1. 在 `app/routers/` 目录下创建新的路由文件
2. 在 `app/main.py` 中注册路由
3. 如需要新的数据模型，在 `app/models.py` 中定义
4. 如需要新的请求响应模型，在 `app/schemas.py` 中定义

### 前端开发

添加新页面：
1. 在 `src/views/` 目录下创建新的 `.vue` 组件
2. 在 `src/router/index.js` 中添加路由配置
3. 如需要新的 API 接口，在 `src/api/index.js` 中封装
4. 如需要新的状态管理，在 `src/stores/` 目录下创建 store

## 常见问题

### 1. 后端启动失败
- 检查 Python 版本是否 ≥ 3.8
- 检查端口 8000 是否被占用
- 查看控制台错误信息

### 2. 前端启动失败
- 检查 Node.js 版本是否 ≥ 16
- 删除 `node_modules` 目录后重新执行 `npm install`
- 检查端口 5173 是否被占用

### 3. 无法获取配对推荐
- 确保当前用户已设置地理位置
- 确保当前用户至少有一只宠物
- 确保系统中有其他用户也设置了地理位置和宠物

### 4. 附近宠物为空
- 确保当前用户已设置地理位置
- 调整搜索范围滑块（最大50公里）

## License

MIT

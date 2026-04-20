# 部署到 Cloudflare Pages 详细步骤

本文档适用于当前项目：

- 项目根目录：`C:\Users\1\Desktop\前后端相关\vue_fastapi_技术文档`
- Cloudflare Pages 实际部署目录：`frontend`
- 构建命令：`npm run build`
- 构建输出目录：`dist`

当前项目已经完成以下适配：

- 文档数据改为前端静态读取：`frontend/public/data/documents.json`
- 图片代理改为 Pages Function：`frontend/functions/api/image-proxy.js`
- Vue 单页路由可直接部署到 Cloudflare Pages

---

## 一、部署前确认

请先确认本机已安装：

- Git
- Node.js
- GitHub 账号
- Cloudflare 账号

建议先本地确认前端可构建：

```powershell
cd "C:\Users\1\Desktop\前后端相关\vue_fastapi_技术文档\frontend"
npm run build
```

---

## 二、上传到 GitHub

当前目录还没有初始化 Git 仓库，所以先执行以下命令。

### 1. 进入项目根目录

```powershell
cd "C:\Users\1\Desktop\前后端相关\vue_fastapi_技术文档"
```

### 2. 初始化 Git 仓库

```powershell
git init
git add .
git commit -m "Prepare project for Cloudflare Pages"
git branch -M main
```

### 3. 在 GitHub 新建仓库

去 GitHub 创建一个新仓库，建议仓库名例如：

- `vue-fastapi-docs`
- `aqualitebot-docs`

创建时不要勾选：

- `Add a README file`
- `Add .gitignore`
- `Choose a license`

### 4. 关联远程仓库并推送

把下面命令中的地址替换成你自己的 GitHub 仓库地址：

```powershell
git remote add origin https://github.com/你的GitHub用户名/你的仓库名.git
git push -u origin main
```

如果你使用 SSH，也可以改成：

```powershell
git remote add origin git@github.com:你的GitHub用户名/你的仓库名.git
git push -u origin main
```

---

## 三、在 Cloudflare Pages 部署

### 1. 创建 Pages 项目

登录 Cloudflare 后：

1. 进入 `Workers & Pages`
2. 点击 `Create application`
3. 选择 `Pages`
4. 选择 `Import an existing Git repository`
5. 授权 GitHub
6. 选择你刚刚创建的仓库

### 2. 填写构建配置

请按下面填写：

- `Framework preset`：`Vue`
- `Production branch`：`main`
- `Root directory`：`frontend`
- `Build command`：`npm run build`
- `Build output directory`：`dist`

然后点击：

- `Save and Deploy`

### 3. 等待首次构建完成

构建成功后，你会得到一个类似这样的地址：

- `你的项目名.pages.dev`

先打开这个地址测试：

- 首页是否正常打开
- 点击分类是否能进入文章
- 文章详情页刷新是否正常
- 图片是否能正常显示

---

## 四、绑定你的域名

你需要先确定你绑定的是哪一种：

### 情况 A：绑定二级域名

例如：

- `docs.example.com`
- `help.example.com`

这是最省事的方式。

### 情况 B：绑定根域名

例如：

- `example.com`

这种方式要求域名已经接入 Cloudflare。

---

## 五、绑定二级域名的步骤

以 `docs.example.com` 为例。

### 1. 在 Pages 项目中添加域名

进入 Cloudflare Pages 项目后：

1. 打开 `Custom domains`
2. 点击 `Set up a domain`
3. 输入：`docs.example.com`
4. 点击继续

### 2. 配置 DNS

如果你的 DNS 已经托管在 Cloudflare：

- Cloudflare 通常会自动帮你创建对应记录

如果你的 DNS 不在 Cloudflare：

- 去你的 DNS 服务商后台添加一条 `CNAME`

记录模板如下：

| 类型 | 主机记录 | 记录值 |
|---|---|---|
| CNAME | docs | 你的项目.pages.dev |

例如：

| 类型 | 主机记录 | 记录值 |
|---|---|---|
| CNAME | docs | aqualitebot-docs.pages.dev |

### 3. 等待生效

Cloudflare 会为这个域名签发 HTTPS 证书。  
一般等几分钟到几十分钟。

生效后，你就可以通过：

- `https://docs.example.com`

访问站点。

---

## 六、绑定根域名的步骤

以 `example.com` 为例。

### 1. 先把域名接入 Cloudflare

如果根域名要给 Pages 使用，Cloudflare 官方要求这个根域名必须先作为一个 Zone 接入 Cloudflare。

操作流程：

1. 在 Cloudflare 添加站点：`example.com`
2. Cloudflare 会给你两条 nameserver
3. 去你的域名注册商后台
4. 把原来的 nameserver 改成 Cloudflare 提供的 nameserver
5. 等待 Cloudflare 接管成功

### 2. 在 Pages 项目中添加根域名

接管完成后：

1. 打开 Pages 项目
2. 进入 `Custom domains`
3. 点击 `Set up a domain`
4. 输入：`example.com`
5. 点击继续

Cloudflare 会自动为你创建对应记录和证书。

### 3. 测试访问

访问：

- `https://example.com`

---

## 七、推荐你优先使用哪种域名

如果你的网站只是文档站，我更推荐你先用二级域名：

- `docs.你的域名.com`

原因：

- 配置更简单
- 风险更小
- 不影响你主站
- DNS 改动更少

---

## 八、常见问题

### 1. 为什么现在不需要单独部署 FastAPI？

因为这个项目已经改成：

- 文档数据走静态 JSON
- 图片代理走 Cloudflare Pages Function

所以 Cloudflare Pages 就能单独完成部署。

### 2. 为什么不能直接用 Pages 的 Direct Upload？

因为当前项目包含 Pages Functions。  
Cloudflare 官方文档说明：带 Functions 的项目不适合直接通过 Dashboard 的 Direct Upload 部署，建议用 Git 集成部署。

### 3. Vue 路由刷新会不会 404？

不会。  
Cloudflare Pages 对 Vue 这类单页应用默认支持 SPA 路由回退。

### 4. 为什么我手动加了 CNAME 还是打不开？

因为 Cloudflare 官方明确提示：

- 必须先在 Pages 项目里通过 `Set up a domain` 关联域名
- 不能只在 DNS 里手动加记录

否则可能会出现解析失败或 `522` 错误。

### 5. 如果绑定域名后证书一直不生效怎么办？

重点检查：

- 域名是否真的解析到了 Pages
- 是否先在 Pages 面板里添加了域名
- 如果是根域名，是否已经把 nameserver 切到 Cloudflare
- 是否存在限制证书签发的 `CAA` 记录

---

## 九、你实际需要填写的内容

部署时你真正需要自己替换的地方只有这几个：

### GitHub 仓库地址

```powershell
git remote add origin https://github.com/你的GitHub用户名/你的仓库名.git
```

### Cloudflare Pages 构建配置

- `Root directory`：`frontend`
- `Build command`：`npm run build`
- `Build output directory`：`dist`

### 二级域名示例

- `docs.example.com`

### 根域名示例

- `example.com`

---

## 十、官方文档

- Vue 部署到 Cloudflare Pages  
  <https://developers.cloudflare.com/pages/framework-guides/deploy-a-vue-site/>

- Cloudflare Pages Git 集成  
  <https://developers.cloudflare.com/pages/get-started/git-integration/>

- Cloudflare Pages Functions  
  <https://developers.cloudflare.com/pages/functions/get-started/>

- Cloudflare Pages 自定义域名  
  <https://developers.cloudflare.com/pages/configuration/custom-domains/>

- Cloudflare Pages SPA 路由行为  
  <https://developers.cloudflare.com/pages/configuration/serving-pages/>

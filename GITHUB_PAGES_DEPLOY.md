# GitHub Pages 部署说明

这个仓库现在已经支持 GitHub Pages 版本。

## GitHub Pages 版本做了什么适配

- GitHub Actions 自动构建并发布
- 构建目录为 `frontend`
- 文档数据继续读取 `frontend/public/data/documents.json`
- GitHub Pages 构建时自动切换为 Hash 路由
- GitHub Pages 构建时关闭 `/api/image-proxy`
- 图片直接使用原始图片链接
- 自动生成 `404.html` 作为静态托管兜底页

## 已添加文件

- `.github/workflows/deploy-github-pages.yml`
- `GITHUB_PAGES_DEPLOY.md`

## 发布后的默认地址

如果使用默认域名，通常会发布到：

- `https://aqualite2370.github.io/AquaLiteBot_techdocs/`

## 如果你后续绑定自定义域名

如果你给 GitHub Pages 绑定独立域名，建议在 GitHub 仓库的 Actions Variables 里增加：

- `VITE_GITHUB_BASE=/`

这样构建出来的静态资源路径会从根路径开始，而不是继续带仓库名目录。

## 需要注意的限制

GitHub Pages 只能运行静态站点，不能运行：

- Cloudflare Worker
- Pages Function
- FastAPI

所以 GitHub Pages 版本保留的是纯静态浏览能力，不包含服务端图片代理。

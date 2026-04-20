# Cloudflare Pages 部署说明

这个项目已经适配为 Cloudflare Pages 版本：

- 前端通过 `frontend/public/data/documents.json` 直接读取文档数据
- 图片代理通过 `frontend/functions/api/image-proxy.js` 提供
- Cloudflare Pages 部署时只需要使用 `frontend` 目录

## 推荐部署参数

- Framework preset: `Vue`
- Root directory: `frontend`
- Build command: `npm run build`
- Build output directory: `dist`

## 自定义域名

- 如果绑定二级域名，例如 `docs.example.com`，可以直接在 Pages 项目里添加
- 如果绑定根域名，例如 `example.com`，需要先把域名托管到 Cloudflare

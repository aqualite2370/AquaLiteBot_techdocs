# Cloudflare Workers 部署说明

这个仓库现在同时支持两种部署方式：

- Cloudflare Pages
- Cloudflare Workers 静态站点

如果你当前用的是 `*.workers.dev` 或 `bot.aqualite.space` 绑定到 Worker，那么请使用本文件对应的 Workers 方案。

## 为什么之前会白屏

因为之前 Worker 很可能直接把源码目录当成静态资源目录发布了。

源码里的 `frontend/index.html` 只适合本地开发，会引用：

- `/src/main.js`
- `/boba-logo.svg`

如果 Worker 没有先构建 Vite，再正确发布 `frontend/dist`，线上就会出现：

- JS 入口找不到
- 图标加载失败
- 页面白屏

## 现在的 Worker 配置

仓库根目录新增了：

- `wrangler.jsonc`
- `worker/index.js`

作用如下：

- 自动先执行 `frontend` 里的 `npm run build`
- 正确发布 `frontend/dist`
- 对 Vue 路由启用 SPA 回退
- 让 `/api/image-proxy` 在 Worker 模式下也可用

## 重新部署后生效

你需要让当前 Worker 重新部署一次，新的配置才会生效。

如果你是在 Cloudflare Dashboard 里连 GitHub 部署：

1. 打开当前 Worker 项目 `bottechdocs`
2. 进入 `Deployments`
3. 触发一次重新部署

如果 Dashboard 里没有自动识别构建：

- Build command: `npm run build`
- Build working directory: `frontend`
- Asset directory: `frontend/dist`

## 自定义域名

你当前阿里云里的这条 CNAME 可以继续保留：

- `bot.aqualite.space -> bottechdocs.q712515712q.workers.dev`

重新部署成功后，它会自动指向新的 Worker 版本。

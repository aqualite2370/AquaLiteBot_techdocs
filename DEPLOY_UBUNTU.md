# Ubuntu 服务器部署说明

这个项目适合用下面这套方式部署到 Ubuntu：

- `Nginx`：托管前端静态文件，并把 `/api/*` 转发给 FastAPI
- `systemd`：常驻运行 FastAPI
- `Python venv`：隔离后端依赖
- `Node.js + npm`：构建前端 `frontend/dist`

## 0. 部署前先确认

本项目目前有两份文档数据：

- 后端源数据：`backend/data/documents.json`
- 前端静态数据：`frontend/public/data/documents.json`

部署时一定要先同步这两份数据，再构建前端。仓库里已经提供了自动同步脚本，部署脚本会帮你执行。

## 1. 本地先把代码推到 GitHub

如果你的服务器只能通过网页 SSH 进入，最省事的方式就是先把本地代码推到 GitHub，然后服务器再 `git clone` / `git pull`。

Windows 本地执行：

```powershell
cd "C:\Users\1\Desktop\前后端相关\vue_fastapi_技术文档"
git status
git add .
git commit -m "Prepare Ubuntu deploy"
git push origin main
```

如果仓库默认分支不是 `main`，把上面的分支名改成你的实际分支。

## 2. 在 Ubuntu 安装基础环境

网页登录 SSH 后执行：

```bash
sudo apt update
sudo apt install -y nginx python3 python3-venv python3-pip git curl
```

然后安装 Node.js 20（或任何 `>= 18` 的版本）：

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
```

## 3. 拉取项目代码

建议统一放到：

- `/var/www/aqualitebot-techdocs`

首次部署：

```bash
sudo mkdir -p /var/www
cd /var/www
sudo git clone https://github.com/aqualite2370/AquaLiteBot_techdocs.git aqualitebot-techdocs
sudo chown -R $USER:$USER /var/www/aqualitebot-techdocs
cd /var/www/aqualitebot-techdocs
```

如果你的 GitHub 仓库是私有仓库：

- 可以改用 PAT 方式克隆
- 或者先在本地推到一个你能从服务器访问的仓库

## 4. 运行部署脚本

仓库已提供脚本：

- `deploy/ubuntu/deploy.sh`

在服务器执行：

```bash
cd /var/www/aqualitebot-techdocs
chmod +x deploy/ubuntu/deploy.sh
./deploy/ubuntu/deploy.sh
```

这个脚本会自动完成：

1. 创建后端虚拟环境 `backend/.venv`
2. 安装 `backend/requirements.txt`
3. 把 `backend/data/documents.json` 同步到 `frontend/public/data/documents.json`
4. 执行 `npm ci`
5. 执行 `npm run build`

执行完成后，前端静态文件会出现在：

- `/var/www/aqualitebot-techdocs/frontend/dist`

## 5. 配置 FastAPI 为 systemd 服务

先把模板复制到 systemd：

```bash
sudo cp deploy/ubuntu/aqualitebot-docs.service /etc/systemd/system/aqualitebot-docs.service
```

如果你的项目目录不是 `/var/www/aqualitebot-techdocs`，先编辑模板里的路径：

```bash
sudo nano /etc/systemd/system/aqualitebot-docs.service
```

然后启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now aqualitebot-docs
sudo systemctl status aqualitebot-docs
```

正常情况下，FastAPI 会监听：

- `127.0.0.1:8000`

## 6. 配置 Nginx

复制模板：

```bash
sudo cp deploy/ubuntu/nginx.conf /etc/nginx/sites-available/aqualitebot-techdocs
```

编辑域名或服务器 IP：

```bash
sudo nano /etc/nginx/sites-available/aqualitebot-techdocs
```

把下面这一行：

```nginx
server_name your-domain.com your-server-ip;
```

改成你的实际域名或服务器公网 IP。

启用站点：

```bash
sudo ln -sf /etc/nginx/sites-available/aqualitebot-techdocs /etc/nginx/sites-enabled/aqualitebot-techdocs
sudo nginx -t
sudo systemctl reload nginx
```

这个模板额外处理了字体文件的 MIME 类型：

- `woff2 -> font/woff2`
- `woff -> font/woff`
- `ttf -> font/ttf`

如果你看到页面图标显示成方块，优先检查这一点。

## 7. 放行防火墙

如果服务器启用了 UFW：

```bash
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
sudo ufw status
```

## 8. 访问与检查

浏览器访问：

- `http://你的域名`
- 或 `http://你的服务器公网IP`

接口自检：

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/api/categories
```

如果页面能打开、接口返回 JSON，说明部署成功。

## 9. 后续更新

以后每次本地改完代码，按这个流程更新：

本地：

```powershell
cd "C:\Users\1\Desktop\前后端相关\vue_fastapi_技术文档"
git add .
git commit -m "Update docs"
git push origin main
```

服务器：

```bash
cd /var/www/aqualitebot-techdocs
git pull
./deploy/ubuntu/deploy.sh
sudo systemctl restart aqualitebot-docs
sudo systemctl reload nginx
```

## 10. 可选：配置 HTTPS

如果你已经绑定域名，推荐再执行：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

执行后，Nginx 会自动切到 HTTPS。

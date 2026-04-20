import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const githubRepoName = process.env.GITHUB_REPOSITORY?.split('/')[1] || 'AquaLiteBot_techdocs'
const isGitHubPagesBuild = process.env.GITHUB_PAGES === 'true'
const githubPagesBase = process.env.VITE_GITHUB_BASE || `/${githubRepoName}/`

export default defineConfig({
  plugins: [vue()],
  base: isGitHubPagesBuild ? githubPagesBase : '/',
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
})

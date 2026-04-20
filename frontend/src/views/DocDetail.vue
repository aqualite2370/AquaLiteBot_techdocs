<template>
  <div class="doc-detail-root">
    <div class="max-w-4xl mx-auto">
      <div v-if="isLoading" class="space-y-8 mt-4">
        <div class="skeleton h-12 w-2/3"></div>
        <div class="flex space-x-4 border-b border-slate-800 pb-4">
          <div class="skeleton h-4 w-24"></div>
          <div class="skeleton h-4 w-32"></div>
        </div>
        <div class="skeleton h-32 w-full mt-8"></div>
        <div class="space-y-4">
          <div class="skeleton h-4 w-full"></div>
          <div class="skeleton h-4 w-5/6"></div>
          <div class="skeleton h-4 w-4/6"></div>
        </div>
      </div>

      <article v-else class="mt-4">
        <h1 class="text-3xl lg:text-5xl font-black text-white mb-6 tracking-tight drop-shadow-md">
          {{ document.title || '文档详情' }}
        </h1>

        <div class="flex items-center text-sm font-mono text-slate-400 mb-10 border-b border-slate-800 pb-4 flex-wrap gap-2">
          <span class="flex items-center">
            <i class="ri-terminal-box-line mr-2 text-primary"></i>
            {{ currentDate }}
          </span>
          <span class="mx-4 text-slate-700 hidden sm:inline">|</span>
          <span class="flex items-center">
            <i class="ri-cpu-line mr-2 text-primary"></i>
            5 MIN READ
          </span>
          <span class="mx-4 text-slate-700 hidden sm:inline">|</span>
          <span class="flex items-center">
            <i class="ri-price-tag-3-line mr-2 text-primary"></i>
            <span v-for="(tag, idx) in document.tags || []" :key="idx" class="mr-2">
              {{ tag }}
            </span>
          </span>
        </div>

        <div class="space-y-8 text-slate-300 leading-relaxed">
          <div
            ref="contentRef"
            class="prose prose-invert prose-slate max-w-none"
            v-html="renderedContent"
            @click="handleContentClick"
          ></div>

          <div class="mt-12 pt-8 border-t border-slate-800">
            <router-link
              to="/"
              class="inline-flex items-center px-6 py-3 bg-primary/10 hover:bg-primary/20 text-primary border border-primary/30 rounded-lg transition-all duration-300 group"
            >
              <i class="ri-arrow-left-line mr-2 group-hover:-translate-x-1 transition-transform"></i>
              返回目录
            </router-link>
          </div>
        </div>
      </article>
    </div>

    <transition name="image-preview">
      <div
        v-if="previewImageSrc"
        class="fixed inset-0 z-[80] bg-slate-950/90 backdrop-blur-sm flex items-center justify-center p-4"
        @click="closeImagePreview"
      >
        <div
          class="image-preview-window w-full max-w-4xl max-h-[86vh] rounded-2xl border border-slate-600/60 bg-slate-900/80 shadow-2xl overflow-hidden"
          @click.stop
        >
          <div class="h-11 px-4 border-b border-slate-700/70 flex items-center justify-between bg-slate-900/70">
            <p class="text-sm md:text-base text-slate-200 truncate pr-3">
              {{ previewImageAlt || '图片预览' }}
            </p>
            <button
              type="button"
              class="text-slate-300 hover:text-white transition-colors"
              @click="closeImagePreview"
              aria-label="关闭预览"
            >
              <i class="ri-close-line text-xl"></i>
            </button>
          </div>
          <div
            class="p-4 md:p-5 bg-slate-950/45"
            @wheel.prevent="handlePreviewWheel"
            @touchstart="handlePreviewTouchStart"
            @touchmove.prevent="handlePreviewTouchMove"
            @touchend="handlePreviewTouchEnd"
            @touchcancel="handlePreviewTouchEnd"
          >
            <div class="preview-canvas">
              <img
                :src="previewImageSrc"
                :alt="previewImageAlt || '预览图片'"
                :style="{ transform: `scale(${previewScale})` }"
                class="preview-image max-w-full max-h-[72vh] object-contain rounded-lg border border-slate-700/80 shadow-xl"
              />
            </div>
          </div>
          <p class="px-4 pb-4 text-sm text-slate-300 text-center">点击窗口外空白处关闭 · 鼠标滚轮 / 移动端双指可缩放图片</p>
        </div>
      </div>
    </transition>

    <transition name="qq-notice">
      <div
        v-if="actionNotice"
        class="fixed right-5 bottom-5 z-[90] max-w-lg rounded-3xl border border-cyan-300/55 bg-[linear-gradient(135deg,rgba(8,47,73,0.94),rgba(15,23,42,0.96))] px-5 py-4 text-cyan-50 shadow-[0_24px_60px_rgba(8,47,73,0.5),0_0_0_1px_rgba(103,232,249,0.22)] backdrop-blur-xl"
      >
        <div class="flex items-start gap-3">
          <span class="mt-0.5 inline-flex h-9 w-9 shrink-0 items-center justify-center rounded-2xl border border-cyan-200/35 bg-cyan-300/12 text-cyan-100 shadow-[0_0_18px_rgba(103,232,249,0.2)]">
            <i class="ri-file-copy-2-line text-lg"></i>
          </span>
          <div class="min-w-0">
            <p class="text-[11px] font-black uppercase tracking-[0.22em] text-cyan-200/80">QQ 已复制</p>
            <p class="mt-1 text-sm leading-6 text-cyan-50">{{ actionNotice }}</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { fetchDocument } from '../api'

const QQ_CONTACT_DOC_IDS = new Set(['80dd24d52c9f79d0f9ef4fc3d0c434b1'])

const route = useRoute()
const document = ref({})
const isLoading = ref(true)
const currentDate = ref('')
const contentRef = ref(null)
const actionNotice = ref('')
const previewImageSrc = ref('')
const previewImageAlt = ref('')
const previewScale = ref(1)
let activeRequestId = 0
let loadingTimer = null
let noticeTimer = null
const MIN_PREVIEW_SCALE = 0.6
const MAX_PREVIEW_SCALE = 3.5
const pinchState = {
  active: false,
  startDistance: 0,
  startScale: 1
}

marked.setOptions({ gfm: true, breaks: true })

const proxyImageUrl = (rawUrl) => {
  try {
    const parsed = new URL(rawUrl)
    if (!parsed.hostname.endsWith('youdao.com')) return rawUrl
    return `/api/image-proxy?url=${encodeURIComponent(rawUrl)}`
  } catch {
    return rawUrl
  }
}

const markCodeBlocks = (html) => {
  if (!html) return ''

  return String(html)
    .replace(
      /<pre><code class="language-([A-Za-z0-9_-]+)">/gi,
      (_, lang) => `<pre class="code-block code-block-${String(lang).toLowerCase()}" data-lang="${String(lang).toUpperCase()}"><code class="language-${lang}">`
    )
    .replace(/<pre><code>/gi, '<pre class="code-block code-block-plain" data-lang="CODE"><code>')
}

const isMobileQqContext = () => typeof navigator !== 'undefined' && /Android|iPhone|iPad|iPod/i.test(navigator.userAgent)

const buildQqProfileLink = (uin) => `qqprofile://${uin}`

const buildQqGroupLink = (uin) => `qqgroup://${uin}`

const decorateQqReferences = (content, docId) => {
  if (!content || !QQ_CONTACT_DOC_IDS.has(String(docId || ''))) return String(content || '')

  const lines = String(content).split('\n')
  let expectGroupLine = false

  return lines.map((line) => {
    const trimmed = line.trim()

    if (!trimmed) return line

    if (/^QQ群聊[:：]?\s*$/.test(trimmed)) {
      expectGroupLine = true
      return line
    }

    const qqMatch = line.match(/^(.+?)\[(\d{5,12})\]（QQ）\s*$/)
    if (qqMatch) {
      const [, label, uin] = qqMatch
      expectGroupLine = false
      return `[${label.trim()}（QQ：${uin}）](${buildQqProfileLink(uin)})`
    }

    const groupMatch = line.match(/^(.+?)\s+(\d{5,12})\s*$/)
    if (groupMatch && expectGroupLine) {
      const [, label, uin] = groupMatch
      expectGroupLine = false
      return `[${label.trim()}（QQ群：${uin}）](${buildQqGroupLink(uin)})`
    }

    expectGroupLine = false
    return line
  }).join('\n')
}

const normalizeMarkdown = (content) => {
  if (!content) return ''

  const fixedImages = decorateQqReferences(content, route.params.id)
    .replace(/\r\n/g, '\n')
    .replace(/!\[([^\]]*)\]\s*\n+\s*\((https?:\/\/[^\s)]+)\)/g, '![$1]($2)')
    .replace(/!\\\[([^\]]*)\\\]\((https?:\/\/[^\s)]+)\)/g, '![$1]($2)')
  const normalized = fixedImages
    .replace(/!\[([^\]]*)\]\((https?:\/\/[^\s)]+)\)/g, (_, alt, url) => `![${alt}](${proxyImageUrl(url)})`)
    .replace(
      /<img\s+([^>]*?)src=["'](https?:\/\/[^"']+)["']([^>]*)>/gi,
      (_, pre, src, post) => `<img ${pre}src="${proxyImageUrl(src)}"${post}>`
    )

  return normalized
}

const decorateImageTags = (html) => {
  if (!html) return ''

  return String(html).replace(/<img\b([^>]*)>/gi, (_, attrs = '') => {
    let output = attrs

    if (/class=/i.test(output)) {
      output = output.replace(/class=(['"])(.*?)\1/i, (match, quote, className) => {
        if (className.includes('doc-image')) return match
        return `class=${quote}${className} doc-image${quote}`
      })
    } else {
      output += ' class="doc-image"'
    }

    if (!/loading=/i.test(output)) output += ' loading="lazy"'
    if (!/decoding=/i.test(output)) output += ' decoding="async"'
    if (!/referrerpolicy=/i.test(output)) output += ' referrerpolicy="no-referrer"'

    return `<img ${output.trim()}>`
  })
}

const decorateAnchorTags = (html) => {
  if (!html) return ''

  return String(html).replace(/<a\b([^>]*)>([\s\S]*?)<\/a>/gi, (_, attrs = '', inner = '') => {
    let output = attrs
    const hrefMatch = output.match(/href=(['"])(.*?)\1/i)
    const href = hrefMatch ? hrefMatch[2] : ''
    const isQqProfileLink = /^qqprofile:\/\/(\d{5,12})$/i.test(href)
    const isQqGroupLink = /^qqgroup:\/\/(\d{5,12})$/i.test(href)
    const isWebLink = /^https?:\/\//i.test(href)

    if (isQqProfileLink) {
      const uin = href.replace(/^qqprofile:\/\//i, '')
      if (isMobileQqContext()) {
        output = output.replace(
          /href=(['"])(.*?)\1/i,
          `href="mqqapi://card/show_pslcard?src_type=internal&version=1&uin=${uin}&card_type=person&source=qrcode"`
        )
      } else {
        output = output.replace(/href=(['"])(.*?)\1/i, 'href="#"')
        output += ` data-qq-profile="${uin}"`
      }
    }

    if (isQqGroupLink) {
      const uin = href.replace(/^qqgroup:\/\//i, '')
      if (isMobileQqContext()) {
        output = output.replace(
          /href=(['"])(.*?)\1/i,
          `href="mqqapi://card/show_pslcard?src_type=internal&version=1&card_type=group&uin=${uin}&source=qrcode"`
        )
      } else {
        output = output.replace(/href=(['"])(.*?)\1/i, 'href="#"')
        output += ` data-qq-group="${uin}"`
      }
    }

    if (/class=/i.test(output)) {
      output = output.replace(/class=(['"])(.*?)\1/i, (match, quote, className) => {
        if (className.includes('doc-fancy-link')) return match
        return `class=${quote}${className} doc-fancy-link${quote}`
      })
    } else {
      output += ' class="doc-fancy-link"'
    }

    if (isWebLink) {
      if (!/target=/i.test(output)) output += ' target="_blank"'
      if (!/rel=/i.test(output)) output += ' rel="noopener noreferrer nofollow"'
    }

    return `<a ${output.trim()}><span class="doc-fancy-link-text">${inner}</span></a>`
  })
}

const renderedContent = computed(() => {
  if (!document.value.content) return ''
  const html = marked.parse(normalizeMarkdown(document.value.content))
  const codeDecorated = markCodeBlocks(html)
  const linkDecorated = decorateAnchorTags(codeDecorated)
  return decorateImageTags(linkDecorated)
})

const showActionNotice = (message) => {
  if (noticeTimer) {
    clearTimeout(noticeTimer)
    noticeTimer = null
  }

  actionNotice.value = message
  noticeTimer = window.setTimeout(() => {
    actionNotice.value = ''
    noticeTimer = null
  }, 3400)
}

const applyImageLoadingState = () => {
  const root = contentRef.value
  if (!root) return

  const images = root.querySelectorAll('img.doc-image')
  images.forEach((img) => {
    img.classList.remove('is-loaded', 'is-error')
    img.classList.add('is-loading')

    const markLoaded = () => {
      img.classList.remove('is-loading')
      img.classList.add('is-loaded')
    }

    const markError = () => {
      img.classList.remove('is-loading')
      img.classList.add('is-error')
    }

    if (img.complete) {
      if (img.naturalWidth > 0) markLoaded()
      else markError()
      return
    }

    img.addEventListener('load', markLoaded, { once: true })
    img.addEventListener('error', markError, { once: true })
  })
}

const handleContentClick = (event) => {
  const target = event.target
  if (!(target instanceof HTMLElement)) return

  const qqProfileLink = target.closest('a[data-qq-profile]')
  if (qqProfileLink instanceof HTMLAnchorElement) {
    event.preventDefault()
    const profileUin = qqProfileLink.dataset.qqProfile || ''
    if (profileUin && navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(profileUin).catch(() => {})
    }
    showActionNotice(`桌面版 QQ 当前会拦截外部资料卡跳转，QQ 号 ${profileUin} 已复制，你可以在 QQ 内搜索或发起会话。`)
    return
  }

  const qqGroupLink = target.closest('a[data-qq-group]')
  if (qqGroupLink instanceof HTMLAnchorElement) {
    event.preventDefault()
    const groupUin = qqGroupLink.dataset.qqGroup || ''
    if (groupUin && navigator.clipboard?.writeText) {
      navigator.clipboard.writeText(groupUin).catch(() => {})
    }
    showActionNotice(`Windows 版 QQ 不能只靠群号直接打开群资料卡，群号 ${groupUin} 已复制，你可以在 QQ 内搜索加入。`)
    return
  }

  if (!(target instanceof HTMLImageElement)) return
  if (!target.classList.contains('doc-image')) return

  previewImageSrc.value = target.currentSrc || target.src
  previewImageAlt.value = target.alt || ''
  previewScale.value = 1
}

const closeImagePreview = () => {
  previewImageSrc.value = ''
  previewImageAlt.value = ''
  previewScale.value = 1
  pinchState.active = false
  pinchState.startDistance = 0
  pinchState.startScale = 1
}

const handleEscClose = (event) => {
  if (event.key === 'Escape') closeImagePreview()
}

const handlePreviewWheel = (event) => {
  if (!previewImageSrc.value) return
  const delta = event.deltaY < 0 ? 0.12 : -0.12
  const next = Math.min(MAX_PREVIEW_SCALE, Math.max(MIN_PREVIEW_SCALE, previewScale.value + delta))
  previewScale.value = Number(next.toFixed(2))
}

const getTouchDistance = (touches) => {
  if (!touches || touches.length < 2) return 0
  const [a, b] = touches
  return Math.hypot(a.clientX - b.clientX, a.clientY - b.clientY)
}

const handlePreviewTouchStart = (event) => {
  if (event.touches.length < 2) return
  pinchState.active = true
  pinchState.startDistance = getTouchDistance(event.touches)
  pinchState.startScale = previewScale.value
}

const handlePreviewTouchMove = (event) => {
  if (!pinchState.active || event.touches.length < 2) return
  const distance = getTouchDistance(event.touches)
  if (!distance || !pinchState.startDistance) return
  const rawScale = pinchState.startScale * (distance / pinchState.startDistance)
  const next = Math.min(MAX_PREVIEW_SCALE, Math.max(MIN_PREVIEW_SCALE, rawScale))
  previewScale.value = Number(next.toFixed(2))
}

const handlePreviewTouchEnd = (event) => {
  if (event.touches.length >= 2) return
  pinchState.active = false
  pinchState.startDistance = 0
  pinchState.startScale = previewScale.value
}

const loadDocument = async (docId) => {
  const requestId = ++activeRequestId

  if (loadingTimer) {
    clearTimeout(loadingTimer)
    loadingTimer = null
  }

  isLoading.value = true
  document.value = {}
  closeImagePreview()

  try {
    const result = await fetchDocument(docId)
    if (requestId !== activeRequestId) return
    document.value = result || {}
  } catch (error) {
    if (requestId !== activeRequestId) return
    console.error('加载文档失败:', error)
    document.value = {}
  } finally {
    loadingTimer = setTimeout(() => {
      if (requestId !== activeRequestId) return
      isLoading.value = false
    }, 400)
  }
}

const date = new Date()
currentDate.value = date.toISOString().split('T')[0]

watch(
  () => route.params.id,
  (docId) => {
    loadDocument(docId)
  },
  { immediate: true }
)

watch(renderedContent, async () => {
  await nextTick()
  applyImageLoadingState()
})

onMounted(() => {
  window.addEventListener('keydown', handleEscClose)
})

onUnmounted(() => {
  if (loadingTimer) {
    clearTimeout(loadingTimer)
    loadingTimer = null
  }
  if (noticeTimer) {
    clearTimeout(noticeTimer)
    noticeTimer = null
  }
  window.removeEventListener('keydown', handleEscClose)
})
</script>

<style scoped>
@keyframes tech-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@keyframes image-pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 0.9; }
}

.skeleton {
  background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
  background-size: 400% 100%;
  animation: tech-pulse 1.5s ease-in-out infinite;
  border-radius: 0.25rem;
}

.prose :deep(h2) {
  @apply text-4xl font-black text-white mt-12 mb-6 flex items-center;
}

.prose :deep(h2::before) {
  content: '';
  @apply inline-block w-1 h-7 bg-primary mr-3;
}

.prose :deep(h1) {
  @apply text-5xl md:text-6xl font-black text-white mt-8 mb-7 tracking-tight;
}

.prose :deep(h3) {
  @apply text-3xl font-bold text-white mt-10 mb-5;
}

.prose :deep(p) {
  @apply my-6 text-slate-100;
  font-size: 1.32rem;
  line-height: 2.15rem;
}

.prose :deep(ul),
.prose :deep(ol) {
  @apply my-5 pl-7 space-y-3;
}

.prose :deep(li) {
  @apply text-slate-200;
  font-size: 1.08rem;
  line-height: 1.95rem;
}

.prose :deep(strong) {
  @apply text-primary font-semibold;
}

.prose :deep(code) {
  @apply bg-slate-800 text-emerald-400 px-2 py-1 rounded text-sm font-mono;
}

.prose :deep(pre) {
  @apply relative border rounded-xl overflow-x-auto my-5;
  padding: 1rem 1.1rem;
  border-color: rgba(148, 163, 184, 0.32);
  background: rgba(15, 23, 42, 0.52);
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 24px rgba(2, 6, 23, 0.3);
}

.prose :deep(pre code) {
  @apply bg-transparent p-0 text-emerald-300;
  font-size: 0.95rem;
  line-height: 1.65;
}

.prose :deep(pre.code-block) {
  display: block !important;
  width: 100%;
  max-width: 100%;
  margin: 1rem 0;
  border-color: rgba(56, 189, 248, 0.42);
  background: linear-gradient(145deg, rgba(15, 23, 42, 0.62), rgba(30, 41, 59, 0.42));
  box-shadow: 0 14px 30px rgba(2, 6, 23, 0.34), inset 0 0 0 1px rgba(148, 163, 184, 0.08);
  transition: transform 220ms ease, border-color 220ms ease, box-shadow 220ms ease;
}

.prose :deep(pre.code-block)::after {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 1rem;
  z-index: -1;
  opacity: 0;
  transform: scale(0.98);
  transition: opacity 220ms ease, transform 220ms ease;
  background: radial-gradient(circle at 30% 30%, rgba(56, 189, 248, 0.3), transparent 72%);
  filter: blur(13px);
}

.prose :deep(pre.code-block code) {
  @apply text-emerald-200;
  font-size: 0.95rem;
  line-height: 1.62;
}

.prose :deep(pre.code-block:hover),
.prose :deep(pre.code-block:focus-within) {
  transform: scale(1.01);
  border-color: rgba(103, 232, 249, 0.92);
  box-shadow: 0 20px 34px rgba(8, 47, 73, 0.5), 0 0 0 1px rgba(34, 211, 238, 0.45);
}

.prose :deep(pre.code-block:hover::after),
.prose :deep(pre.code-block:focus-within::after) {
  opacity: 1;
  transform: scale(1.02);
}

.prose :deep(a) {
  @apply text-primary;
}

.prose :deep(a.doc-fancy-link) {
  @apply relative inline-flex items-center gap-2 px-3.5 py-2 rounded-xl border text-sm md:text-base font-medium no-underline;
  width: fit-content;
  max-width: min(100%, 38rem);
  min-width: 0;
  box-sizing: border-box;
  color: #a5f3fc;
  border-color: rgba(34, 211, 238, 0.4);
  background: linear-gradient(135deg, rgba(8, 47, 73, 0.55), rgba(15, 23, 42, 0.85));
  backdrop-filter: blur(8px);
  transition: transform 220ms ease, border-color 220ms ease, box-shadow 220ms ease, background 220ms ease;
  box-shadow: 0 10px 24px rgba(2, 6, 23, 0.35);
}

.prose :deep(a.doc-fancy-link .doc-fancy-link-text) {
  display: inline-block;
  width: fit-content;
  min-width: 0;
  max-width: 100%;
  white-space: normal;
  overflow-wrap: anywhere;
  word-break: break-word;
  line-height: 1.55;
  transform-origin: left center;
  transition: transform 220ms cubic-bezier(0.22, 0.9, 0.3, 1), text-shadow 220ms ease, letter-spacing 220ms ease;
}

.prose :deep(a.doc-fancy-link)::before {
  content: '';
  position: absolute;
  inset: -8px;
  border-radius: 0.95rem;
  z-index: -1;
  opacity: 0;
  transition: opacity 220ms ease, transform 220ms ease;
  background: radial-gradient(circle at 50% 50%, rgba(34, 211, 238, 0.28), transparent 72%);
  filter: blur(11px);
}

.prose :deep(a.doc-fancy-link):hover,
.prose :deep(a.doc-fancy-link):focus-visible {
  transform: scale(1.03);
  border-color: rgba(103, 232, 249, 0.9);
  background: linear-gradient(135deg, rgba(14, 116, 144, 0.65), rgba(30, 41, 59, 0.88));
  box-shadow: 0 18px 30px rgba(8, 47, 73, 0.52), 0 0 0 1px rgba(34, 211, 238, 0.38);
}

.prose :deep(a.doc-fancy-link:hover .doc-fancy-link-text),
.prose :deep(a.doc-fancy-link:focus-visible .doc-fancy-link-text) {
  transform: scale(1.06);
  letter-spacing: 0.01em;
  text-shadow: 0 0 12px rgba(125, 211, 252, 0.42);
}

.prose :deep(a.doc-fancy-link):hover::before,
.prose :deep(a.doc-fancy-link):focus-visible::before {
  opacity: 1;
  transform: scale(1.05);
}

.prose :deep(a.doc-fancy-link):focus-visible {
  outline: none;
}

.prose :deep(blockquote) {
  @apply border-l-4 border-primary pl-4 italic text-slate-400 my-4;
}

.prose :deep(img.doc-image) {
  @apply my-7 rounded-lg border border-slate-700/70 mx-auto;
  width: min(100%, 680px);
  max-height: 320px;
  object-fit: contain;
  cursor: zoom-in;
  box-shadow: 0 10px 28px rgba(2, 6, 23, 0.18);
  transition: filter 260ms ease, opacity 260ms ease, transform 260ms ease, box-shadow 260ms ease;
}

.prose :deep(img.doc-image.is-loading) {
  filter: blur(7px) brightness(0.8);
  animation: image-pulse 1.2s ease-in-out infinite;
}

.prose :deep(img.doc-image.is-loaded) {
  filter: saturate(0.94) brightness(0.94);
  opacity: 0.9;
  animation: none;
}

.prose :deep(img.doc-image:hover) {
  opacity: 0.97;
  transform: scale(1.01);
  box-shadow: 0 14px 32px rgba(2, 6, 23, 0.24);
}

.prose :deep(img.doc-image.is-error) {
  filter: grayscale(1);
  opacity: 0.45;
}

.image-preview-enter-active,
.image-preview-leave-active {
  transition: opacity 0.24s ease;
}

.image-preview-enter-active .image-preview-window,
.image-preview-leave-active .image-preview-window {
  transition: transform 0.28s cubic-bezier(0.22, 0.9, 0.3, 1), opacity 0.24s ease;
}

.image-preview-enter-from,
.image-preview-leave-to {
  opacity: 0;
}

.image-preview-enter-from .image-preview-window,
.image-preview-leave-to .image-preview-window {
  opacity: 0;
  transform: translateY(18px) scale(0.94);
}

.qq-notice-enter-active,
.qq-notice-leave-active {
  transition: opacity 0.24s ease, transform 0.28s cubic-bezier(0.22, 0.9, 0.3, 1);
}

.qq-notice-enter-from,
.qq-notice-leave-to {
  opacity: 0;
  transform: translateY(18px) scale(0.92);
}

.preview-canvas {
  max-height: 72vh;
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
  touch-action: none;
}

.preview-image {
  transform-origin: center center;
  transition: transform 130ms ease;
}
</style>

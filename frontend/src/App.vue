<template>
  <div
    id="app"
    :class="['app-shell relative isolate h-screen overflow-hidden', isAppLoaded ? 'post-splash' : 'pre-splash']"
  >
    <transition name="intro-overlay-fade">
      <div v-if="isIntroVisible" class="intro-overlay" :class="{ 'is-leaving': isIntroLeaving }" aria-hidden="true">
        <div class="intro-sky">
          <div class="intro-snow-atmosphere" aria-hidden="true">
            <span
              v-for="mist in introSnowMists"
              :key="`mist-${mist.id}`"
              class="intro-snow-mist"
              :style="introSnowMistStyle(mist)"
            ></span>
          </div>
          <div class="intro-snow-ridges" aria-hidden="true">
            <span class="intro-snow-ridge intro-snow-ridge-back"></span>
            <span class="intro-snow-ridge intro-snow-ridge-mid"></span>
            <span class="intro-snow-ridge intro-snow-ridge-front"></span>
          </div>
          <div class="intro-snow-flurry-layer" aria-hidden="true">
            <span
              v-for="flake in introSnowFlurries"
              :key="`flake-${flake.id}`"
              class="intro-snow-flake"
              :style="introSnowFlakeStyle(flake)"
            ></span>
          </div>

          <div class="intro-center-stage">
            <span class="intro-focus-frost"></span>
            <span class="intro-focus-glow"></span>
            <div class="intro-logo-shell">
              <BobaLogo :size="88" />
            </div>
          </div>
        </div>
      </div>
    </transition>

    <div class="lighting-stage" aria-hidden="true">
      <div class="fixed-light fixed-light-primary"></div>
      <div class="fixed-light fixed-light-secondary"></div>
      <div class="frost-layer"></div>

      <div class="cursor-glow" :style="cursorGlowStyle"></div>
    </div>

    <div class="weather-overlay" aria-hidden="true">
      <div class="weather-stage" :class="`weather-${weatherMode}`">
        <template v-if="weatherMode === 'rainy'">
          <div class="rain-layer">
            <span
              v-for="drop in rainDrops"
              :key="`drop-${drop.id}`"
              class="rain-drop"
              :style="rainDropStyle(drop)"
            ></span>
            <span
              v-for="drop in rainDrops"
              :key="`splash-${drop.id}`"
              class="rain-splash"
              :style="rainSplashStyle(drop)"
            ></span>
          </div>
          <div class="rain-projection"></div>
        </template>

        <template v-if="weatherMode === 'snowy'">
          <div class="snow-layer">
            <span
              v-for="flake in snowFlakes"
              :key="`flake-${flake.id}`"
              class="snow-flake"
              :style="snowFlakeStyle(flake)"
            ></span>
            <span
              v-for="flake in snowFlakes"
              :key="`land-${flake.id}`"
              class="snow-land"
              :style="snowLandStyle(flake)"
            ></span>
          </div>
          <div class="snow-projection"></div>
        </template>

        <div class="ground-cast" :class="`ground-${weatherMode}`"></div>
      </div>
    </div>

    <div class="ripple-layer" aria-hidden="true">
      <span
        v-for="ripple in ripples"
        :key="ripple.id"
        class="click-ripple"
        :style="rippleStyle(ripple)"
      ></span>
    </div>

    <div class="relative z-10 flex h-full overflow-hidden">
      <transition
        enter-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        leave-active-class="transition-opacity duration-300"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isMobileMenuOpen"
          @click="toggleMenu"
          class="fixed inset-0 z-40 bg-slate-900/80 backdrop-blur-sm lg:hidden"
        ></div>
      </transition>

      <aside
        :class="[
          'fixed inset-y-0 left-0 z-50 w-64 transition-transform duration-300 lg:static',
          isMobileMenuOpen || !isMobile ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        ]"
      >
        <div class="splash-target nav-target glass-panel h-full flex flex-col shadow-2xl border-r border-slate-700/50">
          <div class="h-16 flex items-center px-6 border-b border-slate-700/50">
            <div class="w-8 h-8 rounded-md border border-slate-300 bg-white text-black flex items-center justify-center shadow-[0_6px_16px_rgba(2,6,23,0.28)]">
              <BobaLogo :size="22" />
            </div>
            <span class="ml-3 font-bold text-base lg:text-lg tracking-wide text-slate-100">
              AqualiteBot_Doc
            </span>
          </div>

          <nav class="sidebar-scroll flex-1 overflow-y-auto py-6 px-4 space-y-1">
            <div v-for="(group, index) in navData" :key="index" class="mb-6">
              <h3 class="px-3 text-base font-bold text-slate-300 tracking-wide mb-3">
                {{ group.title }}
              </h3>
              <router-link
                v-for="item in group.items"
                :key="item.id"
                :to="item.path"
                @click="closeMobileMenu"
                :class="[
                  'block px-3 py-2.5 rounded text-base font-medium transition-all duration-200',
                  $route.path === item.path
                    ? 'bg-primary/10 text-primary border-l-2 border-primary'
                    : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200 border-l-2 border-transparent'
                ]"
              >
                <i
                  :class="[
                    item.icon,
                    'mr-2',
                    $route.path === item.path ? 'text-primary drop-shadow-[0_0_5px_rgba(14,165,233,0.8)]' : ''
                  ]"
                ></i>
                {{ item.name }}
              </router-link>
            </div>
          </nav>
        </div>
      </aside>

      <main class="main-shell flex-1 flex flex-col h-full relative w-full lg:w-[calc(100%-16rem)]">
        <header class="splash-target header-target h-16 glass-panel flex items-center justify-between px-4 lg:px-8 border-b border-slate-700/50 sticky top-0 z-30">
          <div class="flex items-center">
            <button @click="toggleMenu" class="lg:hidden p-2 -ml-2 mr-2 text-slate-300 hover:text-white transition-colors">
              <i class="ri-menu-fold-line text-2xl"></i>
            </button>
            <div class="hidden sm:flex items-center text-sm text-slate-400 font-mono">
              <span class="text-primary">/</span>
              <span class="mx-2">docs</span>
              <span class="text-primary">/</span>
              <span class="mx-2 text-slate-200">{{ currentPageTitle }}</span>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <div class="weather-switch" role="group" aria-label="切换天气">
              <button
                v-for="option in weatherOptions"
                :key="option.value"
                type="button"
                @click="setWeather(option.value)"
                :class="['weather-switch-btn', weatherMode === option.value ? 'active' : '']"
              >
                {{ option.label }}
              </button>
            </div>
            <span class="weather-chip">{{ weatherLabel }}</span>
            <div class="h-2 w-2 rounded-full bg-green-500 shadow-[0_0_8px_#22c55e] animate-pulse"></div>
            <span class="text-xs text-slate-400 font-mono">SYS.ONLINE</span>
          </div>
        </header>

        <div class="splash-target content-target route-stage flex-1 overflow-y-auto p-4 lg:p-10 scroll-smooth">
          <router-view v-slot="{ Component }">
            <transition name="fast-cut" mode="out-in" :duration="{ enter: 520, leave: 280 }">
              <component :is="Component" :key="$route.fullPath" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchCategories, fetchDocuments } from './api'
import BobaLogo from './components/BobaLogo.vue'

const route = useRoute()
const isAppLoaded = ref(false)
const isIntroVisible = ref(true)
const isIntroLeaving = ref(false)
const isMobileMenuOpen = ref(false)
const isMobile = ref(false)
const cursorX = ref(0)
const cursorY = ref(0)
const isPointerActive = ref(false)
const weatherMode = ref('snowy')
const rainDrops = ref([])
const snowFlakes = ref([])
const ripples = ref([])
const weatherOptions = [
  { value: 'rainy', label: '雨' },
  { value: 'snowy', label: '雪' }
]

const introSnowMists = [
  { id: 1, top: 10, left: 6, width: 36, height: 20, opacity: 0.26, blur: 20, delay: 0.12, duration: 5.4, driftX: 20, driftY: 8 },
  { id: 2, top: 20, left: 56, width: 30, height: 18, opacity: 0.22, blur: 16, delay: 0.42, duration: 6.2, driftX: -16, driftY: 6 },
  { id: 3, top: 44, left: 22, width: 42, height: 22, opacity: 0.18, blur: 24, delay: 0.18, duration: 5.9, driftX: 12, driftY: -5 },
  { id: 4, top: 54, left: 64, width: 34, height: 19, opacity: 0.16, blur: 18, delay: 0.56, duration: 6.8, driftX: -10, driftY: 4 }
]

const introSnowFlurries = Array.from({ length: 18 }, (_, i) => ({
  id: i + 1,
  left: 8 + (i * 5.1) % 84,
  top: -6 - (i % 5) * 8,
  size: 3 + (i % 4) * 1.4,
  opacity: 0.22 + (i % 3) * 0.08,
  blur: 0.6 + (i % 4) * 0.35,
  delay: i * 0.18,
  duration: 6.4 + (i % 5) * 0.7,
  drift: -10 + (i % 7) * 3.4
}))

let pointerRaf = null
let rippleIdSeed = 0
let introLeaveTimer = null
let introDoneTimer = null

const navData = ref([
  {
    title: '总览',
    items: [{ id: 'home', name: '文档首页', icon: 'ri-home-4-line', path: '/' }]
  }
])

const loadNavData = async () => {
  try {
    const [categories, documents] = await Promise.all([fetchCategories(), fetchDocuments()])
    if (!Array.isArray(categories) || !Array.isArray(documents) || documents.length === 0) return

    const docsByCategory = new Map()
    for (const doc of documents) {
      const categoryId = doc.category || 'uncategorized'
      if (!docsByCategory.has(categoryId)) docsByCategory.set(categoryId, [])
      docsByCategory.get(categoryId).push(doc)
    }

    const dynamicGroups = categories
      .map(category => {
        const docs = (docsByCategory.get(category.id) || [])
          .slice()
          .sort((a, b) => (a.order ?? 999999) - (b.order ?? 999999))
          .map(doc => ({
            id: doc.id,
            name: doc.title,
            icon: category.icon || 'ri-article-line',
            path: `/doc/${doc.id}`
          }))

        return {
          title: category.name,
          items: docs
        }
      })
      .filter(group => group.items.length > 0)

    navData.value = [
      {
        title: '总览',
        items: [{ id: 'home', name: '文档首页', icon: 'ri-home-4-line', path: '/' }]
      },
      ...dynamicGroups
    ]
  } catch (error) {
    console.error('加载导航失败:', error)
  }
}

const currentPageTitle = computed(() => {
  for (const group of navData.value) {
    const item = group.items.find(i => i.path === route.path)
    if (item) return item.name
  }
  return '文档'
})

const weatherLabel = computed(() => {
  const map = {
    rainy: '雨天模式',
    snowy: '雪天模式'
  }
  return map[weatherMode.value]
})

const cursorGlowStyle = computed(() => ({
  left: `${cursorX.value}px`,
  top: `${cursorY.value}px`,
  opacity: isPointerActive.value ? 1 : 0
}))

const checkScreen = () => {
  const nextIsMobile = window.innerWidth < 1024
  const hasChanged = nextIsMobile !== isMobile.value
  isMobile.value = nextIsMobile
  if (!isMobile.value) isMobileMenuOpen.value = false
  if (hasChanged) setWeather(weatherMode.value)
}

const toggleMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  if (isMobile.value) isMobileMenuOpen.value = false
}

const openMobileMenu = () => {
  if (isMobile.value) isMobileMenuOpen.value = true
}

const getRainDropCount = () => (isMobile.value ? 18 : 36)

const getSnowFlakeCount = () => (isMobile.value ? 14 : 28)

const createRainDrops = (count = getRainDropCount()) => {
  return Array.from({ length: count }, (_, index) => ({
    id: index,
    x: Math.random() * 100,
    delay: Math.random() * 1.8,
    duration: 0.65 + Math.random() * 0.7,
    length: 12 + Math.random() * 20,
    splashOffset: (Math.random() - 0.5) * 24
  }))
}

const createSnowFlakes = (count = getSnowFlakeCount()) => {
  return Array.from({ length: count }, (_, index) => ({
    id: index,
    x: Math.random() * 100,
    delay: Math.random() * 6,
    duration: 7 + Math.random() * 8,
    size: 3 + Math.random() * 6,
    drift: -30 + Math.random() * 60,
    opacity: 0.3 + Math.random() * 0.7
  }))
}

const setWeather = (mode) => {
  weatherMode.value = mode

  if (mode === 'rainy') {
    rainDrops.value = createRainDrops()
    snowFlakes.value = []
    return
  }

  if (mode === 'snowy') {
    snowFlakes.value = createSnowFlakes()
    rainDrops.value = []
    return
  }

  rainDrops.value = []
  snowFlakes.value = []
}

const rainDropStyle = (drop) => ({
  left: `${drop.x}%`,
  height: `${drop.length}px`,
  animationDelay: `${drop.delay}s`,
  animationDuration: `${drop.duration}s`
})

const rainSplashStyle = (drop) => ({
  left: `calc(${drop.x}% + ${drop.splashOffset}px)`,
  animationDelay: `${drop.delay}s`,
  animationDuration: `${drop.duration}s`
})

const snowFlakeStyle = (flake) => ({
  left: `${flake.x}%`,
  width: `${flake.size}px`,
  height: `${flake.size}px`,
  opacity: flake.opacity,
  animationDelay: `${flake.delay}s`,
  animationDuration: `${flake.duration}s`,
  '--drift': `${flake.drift}px`
})

const snowLandStyle = (flake) => ({
  left: `${flake.x}%`,
  animationDelay: `${flake.delay}s`,
  animationDuration: `${flake.duration}s`
})

const handlePointerMove = (event) => {
  const { clientX, clientY } = event
  isPointerActive.value = true

  if (pointerRaf) cancelAnimationFrame(pointerRaf)
  pointerRaf = requestAnimationFrame(() => {
    cursorX.value = clientX
    cursorY.value = clientY
    pointerRaf = null
  })
}

const handlePointerLeave = () => {
  isPointerActive.value = false
}

const handleTouchStart = () => {
  isPointerActive.value = false
}

const handleOpenMobileSidebar = () => {
  openMobileMenu()
}

const handlePointerDown = (event) => {
  if (event.button !== 0 && event.pointerType !== 'touch') return

  const ripple = {
    id: ++rippleIdSeed,
    x: event.clientX,
    y: event.clientY,
    size: isMobile.value ? 62 + Math.random() * 56 : 90 + Math.random() * 110
  }

  const maxRipples = isMobile.value ? 2 : 6
  ripples.value = [...ripples.value.slice(-(maxRipples - 1)), ripple]

  window.setTimeout(() => {
    ripples.value = ripples.value.filter(item => item.id !== ripple.id)
  }, 760)
}

const rippleStyle = (ripple) => ({
  left: `${ripple.x}px`,
  top: `${ripple.y}px`,
  width: `${ripple.size}px`,
  height: `${ripple.size}px`
})

const introSnowMistStyle = (mist) => ({
  left: `${mist.left}%`,
  top: `${mist.top}%`,
  width: `${mist.width}vw`,
  height: `${mist.height}vh`,
  '--mist-opacity': mist.opacity,
  filter: `blur(${mist.blur}px)`,
  '--mist-drift-x': `${mist.driftX}px`,
  '--mist-drift-y': `${mist.driftY}px`,
  animationDelay: `${mist.delay}s`,
  animationDuration: `${mist.duration}s`
})

const introSnowFlakeStyle = (flake) => ({
  left: `${flake.left}%`,
  top: `${flake.top}%`,
  width: `${flake.size}px`,
  height: `${flake.size}px`,
  '--flake-opacity': flake.opacity,
  filter: `blur(${flake.blur}px)`,
  '--flake-drift': `${flake.drift}px`,
  animationDelay: `${flake.delay}s`,
  animationDuration: `${flake.duration}s`
})

const clearIntroTimers = () => {
  if (introLeaveTimer) {
    clearTimeout(introLeaveTimer)
    introLeaveTimer = null
  }
  if (introDoneTimer) {
    clearTimeout(introDoneTimer)
    introDoneTimer = null
  }
}

const startIntroSequence = () => {
  clearIntroTimers()

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (prefersReducedMotion) {
    isIntroLeaving.value = false
    isIntroVisible.value = false
    isAppLoaded.value = true
    return
  }

  isAppLoaded.value = false
  isIntroVisible.value = true
  isIntroLeaving.value = false

  introLeaveTimer = window.setTimeout(() => {
    isIntroLeaving.value = true
  }, 2680)

  introDoneTimer = window.setTimeout(() => {
    isIntroVisible.value = false
    isAppLoaded.value = true
  }, 3240)
}

onMounted(() => {
  loadNavData()
  checkScreen()
  window.addEventListener('resize', checkScreen)
  window.addEventListener('mousemove', handlePointerMove)
  window.addEventListener('mouseleave', handlePointerLeave)
  window.addEventListener('touchstart', handleTouchStart, { passive: true })
  window.addEventListener('pointerdown', handlePointerDown, { passive: true })
  window.addEventListener('open-mobile-sidebar', handleOpenMobileSidebar)

  setWeather(weatherMode.value)
  startIntroSequence()
})

onUnmounted(() => {
  window.removeEventListener('resize', checkScreen)
  window.removeEventListener('mousemove', handlePointerMove)
  window.removeEventListener('mouseleave', handlePointerLeave)
  window.removeEventListener('touchstart', handleTouchStart)
  window.removeEventListener('pointerdown', handlePointerDown)
  window.removeEventListener('open-mobile-sidebar', handleOpenMobileSidebar)

  if (pointerRaf) {
    cancelAnimationFrame(pointerRaf)
    pointerRaf = null
  }

  clearIntroTimers()
})
</script>

<style>
body {
  background:
    radial-gradient(circle at 14% 16%, rgba(14, 165, 233, 0.2), transparent 36%),
    radial-gradient(circle at 84% 10%, rgba(56, 189, 248, 0.16), transparent 34%),
    linear-gradient(164deg, #050a14 0%, #0b1324 44%, #080d18 100%);
  color: #f8fafc;
  overflow: hidden;
  -webkit-tap-highlight-color: transparent;
  perspective: 1200px;
}

::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }

.app-shell {
  background: rgba(2, 6, 23, 0.65);
}

.intro-overlay {
  position: fixed;
  inset: 0;
  z-index: 140;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(2, 6, 23, 0.42);
  backdrop-filter: blur(18px) saturate(115%);
  -webkit-backdrop-filter: blur(18px) saturate(115%);
}

.intro-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 34% 40%, rgba(125, 211, 252, 0.24), transparent 42%),
    radial-gradient(circle at 70% 58%, rgba(56, 189, 248, 0.22), transparent 44%);
  opacity: 0.85;
}

.intro-sky {
  position: relative;
  z-index: 3;
  width: 100%;
  height: 100%;
  overflow: hidden;
  --intro-scene-scale: 1;
  background:
    radial-gradient(circle at 50% 18%, rgba(241, 245, 249, 0.18), transparent 24%),
    linear-gradient(180deg, rgba(226, 232, 240, 0.08), rgba(226, 232, 240, 0) 26%);
}

.intro-snow-atmosphere,
.intro-snow-ridges,
.intro-snow-flurry-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.intro-snow-atmosphere {
  z-index: 1;
}

.intro-snow-mist {
  position: absolute;
  border-radius: 9999px;
  background:
    radial-gradient(circle at 42% 50%, rgba(248, 250, 252, 0.62), rgba(226, 232, 240, 0.2) 42%, rgba(226, 232, 240, 0) 76%);
  mix-blend-mode: screen;
  opacity: 0;
  animation: intro-snow-mist 6s ease-in-out infinite;
}

.intro-snow-ridges {
  z-index: 2;
}

.intro-snow-ridge {
  position: absolute;
  left: -10%;
  right: -10%;
  bottom: -16%;
  border-radius: 50%;
  opacity: 0;
  transform: translateY(38px) scale(0.94);
  animation: intro-snow-ridge-rise 1.8s ease-out forwards;
}

.intro-snow-ridge-back {
  height: 42vh;
  background:
    radial-gradient(circle at 50% 20%, rgba(248, 250, 252, 0.18), rgba(226, 232, 240, 0) 48%),
    linear-gradient(180deg, rgba(226, 232, 240, 0.18), rgba(203, 213, 225, 0.08));
  filter: blur(18px);
  animation-delay: 0.16s;
}

.intro-snow-ridge-mid {
  left: -6%;
  right: -4%;
  bottom: -20%;
  height: 36vh;
  background:
    radial-gradient(circle at 46% 26%, rgba(255, 255, 255, 0.4), rgba(255, 255, 255, 0) 38%),
    linear-gradient(180deg, rgba(248, 250, 252, 0.54), rgba(226, 232, 240, 0.24));
  box-shadow: inset 0 18px 36px rgba(255, 255, 255, 0.12);
  filter: blur(10px);
  animation-delay: 0.3s;
}

.intro-snow-ridge-front {
  left: -4%;
  right: -8%;
  bottom: -27%;
  height: 34vh;
  background:
    radial-gradient(circle at 54% 12%, rgba(255, 255, 255, 0.58), rgba(255, 255, 255, 0) 36%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.9), rgba(226, 232, 240, 0.48));
  box-shadow:
    0 -10px 48px rgba(255, 255, 255, 0.12),
    inset 0 20px 28px rgba(255, 255, 255, 0.18);
  filter: blur(6px);
  animation-delay: 0.42s;
}

.intro-snow-flurry-layer {
  z-index: 4;
}

.intro-snow-flake {
  position: absolute;
  border-radius: 9999px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.92), rgba(226, 232, 240, 0.34) 72%, rgba(226, 232, 240, 0));
  box-shadow: 0 0 10px rgba(255, 255, 255, 0.22);
  opacity: 0;
  animation: intro-snow-flake-fall linear infinite;
}

.intro-center-stage {
  position: absolute;
  left: 50%;
  top: 50%;
  z-index: 12;
  width: 190px;
  height: 190px;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.intro-focus-frost {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 66px;
  height: 66px;
  border-radius: 9999px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.72), rgba(226, 232, 240, 0.24) 52%, rgba(226, 232, 240, 0) 74%);
  box-shadow: 0 0 38px rgba(241, 245, 249, 0.3);
  transform: translate(-50%, -50%) scale(0.28);
  opacity: 0;
  filter: blur(6px);
  animation: intro-focus-frost 2.28s ease-out 0.24s forwards;
}

.intro-focus-glow {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 120px;
  height: 120px;
  border-radius: 9999px;
  background: radial-gradient(circle, rgba(186, 230, 253, 0.45), rgba(186, 230, 253, 0));
  filter: blur(8px);
  opacity: 0;
  transform: translate(-50%, -50%) scale(0.5);
  animation: intro-focus-glow 2.05s ease-out 0.34s forwards;
}

.intro-logo-shell {
  position: relative;
  overflow: hidden;
  width: 132px;
  height: 132px;
  border-radius: 32px;
  border: 1px solid rgba(15, 23, 42, 0.25);
  background: #ffffff;
  box-shadow:
    0 16px 34px rgba(2, 6, 23, 0.36),
    inset 0 0 0 1px rgba(148, 163, 184, 0.28);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transform: scale(0.22) rotate(-22deg);
  filter: blur(12px);
  animation: intro-logo-reveal 2.15s cubic-bezier(0.2, 0.9, 0.2, 1.24) 0.34s forwards;
}

.intro-logo-shell::before {
  content: '';
  position: absolute;
  inset: -22%;
  background: linear-gradient(120deg, rgba(255, 255, 255, 0) 22%, rgba(255, 255, 255, 0.96) 46%, rgba(255, 255, 255, 0) 70%);
  transform: translateX(-140%) rotate(14deg);
  opacity: 0;
  animation: intro-logo-flash 1.1s ease-out 1.56s forwards;
}

.intro-logo-shell::after {
  content: '';
  position: absolute;
  inset: -14%;
  border-radius: inherit;
  background: radial-gradient(circle, rgba(186, 230, 253, 0.7) 0%, rgba(125, 211, 252, 0.22) 45%, rgba(125, 211, 252, 0) 76%);
  opacity: 0;
  filter: blur(1px);
  animation: intro-logo-spark 1.2s ease-out 1.42s forwards;
}

.intro-logo-shell > * {
  position: relative;
  z-index: 2;
}

.intro-overlay.is-leaving .intro-sky {
  transform: scale(0.92) translateY(-8px);
  opacity: 0;
  filter: blur(4px);
  transition: transform 320ms ease, opacity 320ms ease, filter 320ms ease;
}

.intro-overlay-fade-enter-active,
.intro-overlay-fade-leave-active {
  transition: opacity 280ms ease;
}

.intro-overlay-fade-enter-from,
.intro-overlay-fade-leave-to {
  opacity: 0;
}

.lighting-stage {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 0;
}

.weather-overlay {
  position: fixed;
  inset: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: 22;
}

.fixed-light {
  position: absolute;
  border-radius: 9999px;
  filter: blur(24px);
}

.fixed-light-primary {
  width: 640px;
  height: 640px;
  top: -200px;
  right: -160px;
  background: radial-gradient(circle, rgba(56, 189, 248, 0.34) 0%, rgba(56, 189, 248, 0.14) 38%, transparent 72%);
}

.fixed-light-secondary {
  width: 520px;
  height: 520px;
  left: -180px;
  bottom: -220px;
  background: radial-gradient(circle, rgba(14, 165, 233, 0.22) 0%, rgba(14, 165, 233, 0.1) 42%, transparent 74%);
}

.weather-stage {
  position: absolute;
  inset: 0;
  overflow: hidden;
  opacity: 0.98;
}

.weather-stage.weather-rainy {
  filter: saturate(1.02) contrast(1.02) brightness(1.02);
  opacity: 0.52;
}

.weather-stage.weather-snowy {
  filter: brightness(1.18) contrast(1.12);
  mix-blend-mode: screen;
}

.rain-layer,
.snow-layer {
  position: absolute;
  inset: 0;
}

.rain-drop {
  position: absolute;
  top: -18%;
  width: 1.4px;
  border-radius: 9999px;
  background: linear-gradient(to bottom, rgba(191, 219, 254, 0), rgba(186, 230, 253, 0.72));
  animation-name: rain-fall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.rain-splash {
  position: absolute;
  bottom: 7vh;
  width: 20px;
  height: 8px;
  border-radius: 9999px;
  border: 1px solid rgba(186, 230, 253, 0.92);
  transform: translateX(-50%) scale(0.3);
  animation-name: splash-hit;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  opacity: 0;
}

.rain-projection {
  position: absolute;
  inset: 0;
  background: repeating-linear-gradient(
    to bottom,
    rgba(147, 197, 253, 0.07) 0 1px,
    rgba(147, 197, 253, 0) 1px 13px
  );
  opacity: 0.18;
}

.snow-flake {
  position: absolute;
  top: -8%;
  border-radius: 9999px;
  background: radial-gradient(circle, rgba(248, 250, 252, 0.95), rgba(226, 232, 240, 0.45));
  box-shadow: 0 0 14px rgba(241, 245, 249, 0.78);
  animation-name: snow-fall;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
}

.snow-land {
  position: absolute;
  bottom: 6vh;
  width: 14px;
  height: 6px;
  border-radius: 9999px;
  background: rgba(226, 232, 240, 0.96);
  filter: blur(1px);
  transform: translateX(-50%) scale(0.2);
  animation-name: snow-land-hit;
  animation-timing-function: linear;
  animation-iteration-count: infinite;
  opacity: 0;
}

.snow-projection {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 70% 16%, rgba(241, 245, 249, 0.38), transparent 42%);
}

.ground-cast {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 24vh;
  opacity: 0.88;
}

.ground-rainy {
  background:
    radial-gradient(circle at 50% 100%, rgba(56, 189, 248, 0.12), transparent 62%),
    linear-gradient(to top, rgba(15, 23, 42, 0.24), transparent 100%);
}

.ground-snowy {
  background: linear-gradient(to top, rgba(226, 232, 240, 0.2), rgba(148, 163, 184, 0.05) 42%, transparent 100%);
}

.frost-layer {
  position: absolute;
  inset: -8%;
  z-index: 1;
  backdrop-filter: blur(12px) saturate(108%);
  -webkit-backdrop-filter: blur(12px) saturate(108%);
  mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 0.38), rgba(0, 0, 0, 0.72));
}

.cursor-glow {
  position: absolute;
  width: 420px;
  height: 420px;
  transform: translate(-50%, -50%);
  border-radius: 9999px;
  background: radial-gradient(circle, rgba(125, 211, 252, 0.34) 0%, rgba(56, 189, 248, 0.16) 36%, rgba(56, 189, 248, 0) 74%);
  filter: blur(18px);
  mix-blend-mode: screen;
  transition: opacity 180ms ease-out;
  z-index: 3;
}

.ripple-layer {
  position: fixed;
  inset: 0;
  z-index: 35;
  pointer-events: none;
  overflow: hidden;
}

.click-ripple {
  position: absolute;
  transform: translate(-50%, -50%) scale(0.2);
  border-radius: 9999px;
  border: 1px solid rgba(125, 211, 252, 0.65);
  background: radial-gradient(circle, rgba(125, 211, 252, 0.36) 0%, rgba(56, 189, 248, 0.2) 42%, rgba(56, 189, 248, 0) 78%);
  box-shadow: 0 0 28px rgba(56, 189, 248, 0.32);
  animation: ripple-burst 720ms ease-out forwards;
}

.main-shell {
  background: linear-gradient(160deg, rgba(15, 23, 42, 0.64), rgba(2, 6, 23, 0.84));
  border-left: 1px solid rgba(148, 163, 184, 0.14);
}

.main-shell::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background:
    radial-gradient(circle at 80% 0%, rgba(14, 165, 233, 0.12), transparent 30%),
    radial-gradient(circle at 0% 75%, rgba(56, 189, 248, 0.1), transparent 35%);
  z-index: 0;
}

.main-shell > * {
  position: relative;
  z-index: 1;
}

.route-stage {
  background: rgba(11, 17, 32, 0.28);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.route-stage::before {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background: linear-gradient(to bottom, rgba(15, 23, 42, 0.16), rgba(15, 23, 42, 0.06) 36%, rgba(15, 23, 42, 0.18));
}

.route-stage > * {
  position: relative;
  z-index: 1;
}

.weather-chip {
  display: inline-flex;
  align-items: center;
  padding: 2px 10px;
  border-radius: 9999px;
  border: 1px solid rgba(148, 163, 184, 0.35);
  background: rgba(15, 23, 42, 0.45);
  color: #cbd5e1;
  font-size: 11px;
  letter-spacing: 0.08em;
}

.weather-switch {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px;
  border-radius: 9999px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  background: rgba(2, 6, 23, 0.45);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

.weather-switch-btn {
  min-width: 30px;
  padding: 3px 8px;
  border: 0;
  border-radius: 9999px;
  background: transparent;
  color: #94a3b8;
  font-size: 11px;
  line-height: 1.2;
  cursor: pointer;
  transition: background-color 180ms ease, color 180ms ease, box-shadow 180ms ease;
}

.weather-switch-btn:hover {
  color: #e2e8f0;
}

.weather-switch-btn.active {
  background: linear-gradient(135deg, rgba(56, 189, 248, 0.48), rgba(14, 165, 233, 0.42));
  color: #f8fafc;
  box-shadow: 0 0 16px rgba(14, 165, 233, 0.28);
}

.sidebar-scroll {
  scrollbar-width: thin;
  scrollbar-color: rgba(186, 230, 253, 0.66) rgba(15, 23, 42, 0.2);
  scrollbar-gutter: stable;
}

.sidebar-scroll::-webkit-scrollbar {
  width: 11px;
}

.sidebar-scroll::-webkit-scrollbar-track {
  border-radius: 9999px;
  background: linear-gradient(
    180deg,
    rgba(148, 163, 184, 0.18),
    rgba(30, 41, 59, 0.16)
  );
  box-shadow:
    inset 0 0 0 1px rgba(226, 232, 240, 0.16),
    inset 0 10px 18px rgba(2, 6, 23, 0.34);
  backdrop-filter: blur(8px) saturate(120%);
  -webkit-backdrop-filter: blur(8px) saturate(120%);
}

.sidebar-scroll::-webkit-scrollbar-thumb {
  border-radius: 9999px;
  border: 1px solid rgba(224, 242, 254, 0.52);
  background: linear-gradient(
    180deg,
    rgba(224, 242, 254, 0.78),
    rgba(125, 211, 252, 0.58) 48%,
    rgba(56, 189, 248, 0.5) 100%
  );
  box-shadow:
    0 8px 18px rgba(2, 6, 23, 0.42),
    0 0 14px rgba(125, 211, 252, 0.34),
    inset 0 0 10px rgba(255, 255, 255, 0.22);
}

.sidebar-scroll::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(
    180deg,
    rgba(240, 249, 255, 0.9),
    rgba(186, 230, 253, 0.7) 45%,
    rgba(14, 165, 233, 0.62) 100%
  );
  box-shadow:
    0 12px 24px rgba(2, 6, 23, 0.5),
    0 0 20px rgba(125, 211, 252, 0.44),
    inset 0 0 12px rgba(255, 255, 255, 0.3);
}

.splash-target {
  transition: transform 1.15s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.8s ease-out;
  transform-origin: center center;
}

.pre-splash .nav-target {
  transform: translate3d(55vw, 48vh, -520px) scale(0.1) rotate(45deg);
  opacity: 0;
}

.pre-splash .header-target {
  transform: translate3d(0, 45vh, -320px) scale(0.25) rotate(-18deg);
  opacity: 0;
}

.pre-splash .content-target {
  transform: translate3d(-45vw, -35vh, -420px) scale(0.12) rotate(28deg);
  opacity: 0;
}

.post-splash .splash-target {
  transform: translate3d(0, 0, 0) scale(1) rotate(0deg);
  opacity: 1;
}

.nav-target { transition-delay: 0.1s; }
.header-target { transition-delay: 0.22s; }
.content-target { transition-delay: 0.36s; }

.fast-cut-enter-active {
  transition: opacity 0.52s cubic-bezier(0.2, 0.75, 0.3, 1), transform 0.52s cubic-bezier(0.2, 0.75, 0.3, 1), filter 0.52s ease;
  will-change: transform, opacity, filter;
}

.fast-cut-leave-active {
  transition: opacity 0.24s cubic-bezier(0.55, 0.08, 0.68, 0.53), transform 0.24s cubic-bezier(0.55, 0.08, 0.68, 0.53), filter 0.24s ease;
  will-change: transform, opacity, filter;
}

.fast-cut-enter-from {
  opacity: 0;
  transform: translate3d(92px, 18px, 0) skewX(-13deg) scale(0.95);
  filter: blur(14px) saturate(1.2);
}

.fast-cut-enter-to {
  opacity: 1;
  transform: translate3d(0, 0, 0) skewX(0deg) scale(1);
  filter: blur(0) saturate(1);
}

.fast-cut-leave-from {
  opacity: 1;
  transform: translate3d(0, 0, 0) skewX(0deg) scale(1);
  filter: blur(0);
}

.fast-cut-leave-to {
  opacity: 0;
  transform: translate3d(-68px, -12px, 0) skewX(8deg) scale(0.965);
  filter: blur(10px) brightness(1.08);
}

.glass-panel {
  background: linear-gradient(160deg, rgba(30, 41, 59, 0.72), rgba(15, 23, 42, 0.62));
  backdrop-filter: blur(16px) saturate(120%);
  -webkit-backdrop-filter: blur(16px) saturate(120%);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

:root {
  --color-primary: #0ea5e9;
}

.bg-primary { background-color: var(--color-primary); }
.text-primary { color: var(--color-primary); }
.border-primary { border-color: var(--color-primary); }

@keyframes rain-fall {
  0% {
    transform: translate3d(0, 0, 0);
    opacity: 0;
  }
  8% {
    opacity: 0.62;
  }
  100% {
    transform: translate3d(0, 122vh, 0);
    opacity: 0;
  }
}

@keyframes cloud-drift {
  0%,
  100% {
    transform: translate3d(0, 0, 0) scale(var(--cloud-scale));
  }
  50% {
    transform: translate3d(var(--cloud-drift), -6px, 0) scale(var(--cloud-scale));
  }
}

@keyframes splash-hit {
  0%, 82% {
    opacity: 0;
    transform: translateX(-50%) scale(0.2);
  }
  88% {
    opacity: 0.5;
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) scale(1.8);
  }
}

@keyframes snow-fall {
  0% {
    transform: translate3d(0, 0, 0);
  }
  50% {
    transform: translate3d(calc(var(--drift) * -0.45), 56vh, 0);
  }
  100% {
    transform: translate3d(var(--drift), 120vh, 0);
  }
}

@keyframes snow-land-hit {
  0%, 86% {
    opacity: 0;
    transform: translateX(-50%) scale(0.2);
  }
  92% {
    opacity: 0.45;
  }
  100% {
    opacity: 0;
    transform: translateX(-50%) scale(1.9);
  }
}

@keyframes ripple-burst {
  0% {
    opacity: 0.72;
    transform: translate(-50%, -50%) scale(0.2);
  }
  70% {
    opacity: 0.32;
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(1.9);
  }
}

@keyframes intro-snow-mist {
  0%,
  100% {
    opacity: 0;
    transform: translate3d(0, 12px, 0) scale(0.94);
  }
  22% {
    opacity: var(--mist-opacity);
  }
  58% {
    opacity: calc(var(--mist-opacity) * 0.9);
    transform: translate3d(var(--mist-drift-x), var(--mist-drift-y), 0) scale(1.05);
  }
  100% {
    opacity: 0;
    transform: translate3d(calc(var(--mist-drift-x) * 1.2), calc(var(--mist-drift-y) + 10px), 0) scale(1.08);
  }
}

@keyframes intro-snow-ridge-rise {
  0% {
    opacity: 0;
    transform: translateY(38px) scale(0.94);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes intro-snow-flake-fall {
  0% {
    opacity: 0;
    transform: translate3d(0, -4vh, 0) scale(0.7);
  }
  14% {
    opacity: var(--flake-opacity);
  }
  100% {
    opacity: 0;
    transform: translate3d(var(--flake-drift), 112vh, 0) scale(1.08);
  }
}

@keyframes intro-focus-frost {
  0%,
  24% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.24);
  }
  44% {
    opacity: 0.9;
    transform: translate(-50%, -50%) scale(1.12);
  }
  64% {
    opacity: 0.46;
    transform: translate(-50%, -50%) scale(0.92);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(1.28);
  }
}

@keyframes intro-focus-glow {
  0%,
  24% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.45);
  }
  44% {
    opacity: 0.9;
    transform: translate(-50%, -50%) scale(1.08);
  }
  64% {
    opacity: 0.52;
    transform: translate(-50%, -50%) scale(0.58);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(0.2);
  }
}

@keyframes intro-logo-reveal {
  0%,
  56% {
    opacity: 0;
    transform: scale(0.22) rotate(-22deg);
    filter: blur(12px);
  }
  67% {
    opacity: 1;
    transform: scale(1.5) rotate(18deg);
    filter: blur(2px);
  }
  78% {
    opacity: 1;
    transform: scale(0.88) rotate(-10deg);
    filter: blur(0);
  }
  90% {
    opacity: 1;
    transform: scale(1.16) rotate(4deg);
    filter: blur(0);
  }
  100% {
    opacity: 1;
    transform: scale(1) rotate(0deg);
    filter: blur(0);
  }
}

@keyframes intro-logo-flash {
  0% {
    opacity: 0;
    transform: translateX(-140%) rotate(14deg);
  }
  24% {
    opacity: 0.98;
  }
  100% {
    opacity: 0;
    transform: translateX(150%) rotate(14deg);
  }
}

@keyframes intro-logo-spark {
  0%,
  10% {
    opacity: 0;
    transform: scale(0.72);
  }
  42% {
    opacity: 0.92;
    transform: scale(1.12);
  }
  100% {
    opacity: 0;
    transform: scale(1.28);
  }
}

@media (max-width: 1023px) {
  .intro-sky {
    width: 100%;
    height: 100%;
    --intro-scene-scale: 0.42;
  }

  .intro-logo-shell {
    width: 108px;
    height: 108px;
    border-radius: 26px;
  }

  .cursor-glow {
    display: none;
  }

  .weather-switch {
    transform: scale(0.95);
    transform-origin: right center;
  }

  .fixed-light-primary,
  .fixed-light-secondary {
    filter: blur(30px);
    opacity: 0.8;
  }

  .rain-projection,
  .snow-projection {
    opacity: 0.6;
  }
}

@media (max-width: 640px) {
  .intro-sky {
    --intro-scene-scale: 0.3;
  }
}

@media (prefers-reduced-motion: reduce) {
  .splash-target,
  .rain-drop,
  .rain-splash,
  .snow-flake,
  .snow-land,
  .intro-shooting-star,
  .intro-star-core,
  .intro-focus-star,
  .intro-focus-glow,
  .intro-logo-shell,
  .click-ripple {
    transition: none !important;
    animation: none !important;
  }
}
</style>

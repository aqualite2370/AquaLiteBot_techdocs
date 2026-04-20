<template>
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
        <span class="inline-flex items-center gap-3">
          <span class="inline-flex items-center justify-center w-10 h-10 rounded-lg border border-slate-300 bg-white text-black shadow-[0_8px_18px_rgba(2,6,23,0.3)]">
            <BobaLogo :size="24" />
          </span>
          AqualiteBot_Doc | 奶茶酱 帮助文档
        </span>
      </h1>

      <div class="flex items-center text-sm font-mono text-slate-400 mb-10 border-b border-slate-800 pb-4">
        <span class="flex items-center">
          <i class="ri-terminal-box-line mr-2 text-primary"></i>
          {{ currentDate }}
        </span>
        <span class="mx-4 text-slate-700">|</span>
        <span class="flex items-center">
          <i class="ri-book-open-line mr-2 text-primary"></i>
          {{ totalDocs }} 篇文档
        </span>
      </div>

      <div class="space-y-8 text-slate-300 leading-relaxed">
        <h3 class="text-2xl font-bold text-white mt-10 mb-5 flex items-center">
          <i class="ri-folder-3-line text-primary mr-2"></i> 文档分类
        </h3>
        <div class="space-y-4">
          <router-link
            v-for="cat in categories"
            :key="cat.id"
            :to="`/doc/${cat.docId}`"
            @click="handleCategoryNavigation"
            class="tech-card p-6 rounded-lg block group"
          >
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center">
                <i :class="[cat.icon, 'text-3xl text-primary mr-3']"></i>
                <h4 class="text-xl font-bold text-white group-hover:text-primary transition-colors">
                  {{ cat.name }}
                </h4>
              </div>
              <span class="text-sm px-3 py-1 rounded border border-primary/30 text-primary">
                {{ cat.docCount }} 篇
              </span>
            </div>
            <p class="text-base text-slate-300">{{ normalizeDescriptionText(cat.description) }}</p>
          </router-link>
        </div>

        <div class="p-6 rounded-lg border border-slate-700/40 bg-slate-900/30 mt-8">
          <h2 class="text-xl font-bold text-white mb-4 flex items-center">
            <i class="ri-stack-line text-primary mr-2"></i> 技术栈
          </h2>
          <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div v-for="tech in techStack" :key="tech.name" class="text-center">
              <i :class="[tech.icon, 'text-3xl text-primary mb-2']"></i>
              <p class="text-sm font-medium text-slate-300">{{ tech.name }}</p>
            </div>
          </div>
        </div>
      </div>
    </article>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { fetchCategories, fetchDocuments } from '../api'
import BobaLogo from '../components/BobaLogo.vue'

const isLoading = ref(true)
const currentDate = ref('')
const categories = ref([])

const techStack = [
  { name: 'Vue 3', icon: 'ri-vuejs-line' },
  { name: 'FastAPI', icon: 'ri-flashlight-line' },
  { name: 'Python', icon: 'ri-code-box-line' },
  { name: 'Tailwind', icon: 'ri-palette-line' },
  { name: 'Vite', icon: 'ri-rocket-line' }
]

const totalDocs = computed(() => categories.value.reduce((sum, category) => sum + category.docCount, 0))

const normalizeDescriptionText = (text) => {
  if (!text) return ''
  const compact = String(text)
    .replace(/\r\n/g, '\n')
    .replace(/\t+/g, ' ')
    .replace(/\s{2,}/g, ' ')
    .replace(/\s*([，。；：！？])/g, '$1')
    .replace(/([，。；：！？])(?=[^\s])/g, '$1 ')
    .trim()

  const chunks = compact
    .split(/[。；;]+/)
    .map(chunk => chunk.trim())
    .filter(Boolean)

  if (chunks.length <= 1) return compact
  return chunks.join(' · ')
}

const handleCategoryNavigation = () => {
  if (typeof window === 'undefined' || window.innerWidth >= 1024) return
  window.dispatchEvent(new CustomEvent('open-mobile-sidebar'))
}

const loadCategories = async () => {
  try {
    const [apiCategories, allDocuments] = await Promise.all([fetchCategories(), fetchDocuments()])
    if (!Array.isArray(apiCategories) || !Array.isArray(allDocuments) || allDocuments.length === 0) {
      categories.value = []
      return
    }

    const docsByCategory = new Map()
    for (const doc of allDocuments) {
      const key = doc.category || 'uncategorized'
      if (!docsByCategory.has(key)) docsByCategory.set(key, [])
      docsByCategory.get(key).push(doc)
    }

    categories.value = apiCategories
      .map(category => {
        const docs = (docsByCategory.get(category.id) || [])
          .slice()
          .sort((a, b) => (a.order ?? 999999) - (b.order ?? 999999))

        if (docs.length === 0) return null

        return {
          id: category.id,
          name: category.name,
          icon: category.icon || 'ri-folder-3-line',
          description: category.description,
          docId: docs[0].id,
          docCount: docs.length
        }
      })
      .filter(Boolean)
  } catch (error) {
    console.error('加载分类失败:', error)
    categories.value = []
  }
}

onMounted(async () => {
  const date = new Date()
  currentDate.value = date.toISOString().split('T')[0]

  await loadCategories()

  setTimeout(() => {
    isLoading.value = false
  }, 400)
})
</script>

<style scoped>
@keyframes tech-pulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton {
  background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
  background-size: 400% 100%;
  animation: tech-pulse 1.5s ease-in-out infinite;
  border-radius: 0.25rem;
}

.tech-card {
  transition: all 0.3s ease;
  border: 1px solid rgba(14, 165, 233, 0.2);
  background: linear-gradient(145deg, rgba(30,41,59,0.8) 0%, rgba(15,23,42,0.9) 100%);
}

.tech-card:hover {
  transform: translateX(8px);
  border-color: rgba(14, 165, 233, 0.6);
  box-shadow: -4px 0 15px rgba(14, 165, 233, 0.15);
}
</style>

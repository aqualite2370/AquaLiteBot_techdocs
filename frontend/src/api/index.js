const DATA_URL = '/data/documents.json'

let payloadCache = null
let payloadPromise = null

const normalizeArray = (value) => (Array.isArray(value) ? value : [])

const loadPayload = async () => {
  if (payloadCache) return payloadCache
  if (payloadPromise) return payloadPromise

  payloadPromise = fetch(DATA_URL, {
    headers: {
      Accept: 'application/json'
    }
  })
    .then(async (response) => {
      if (!response.ok) {
        throw new Error(`Failed to load documents payload: ${response.status}`)
      }

      const payload = await response.json()
      payloadCache = {
        categories: normalizeArray(payload?.categories),
        documents: normalizeArray(payload?.documents)
      }
      return payloadCache
    })
    .catch((error) => {
      payloadPromise = null
      throw error
    })

  return payloadPromise
}

export const fetchCategories = async () => {
  try {
    const payload = await loadPayload()
    return payload.categories
  } catch (error) {
    console.error('获取分类失败:', error)
    return []
  }
}

export const fetchDocuments = async (category = null) => {
  try {
    const payload = await loadPayload()
    if (!category) return payload.documents
    return payload.documents.filter((doc) => doc?.category === category)
  } catch (error) {
    console.error('获取文档列表失败:', error)
    return []
  }
}

export const fetchDocument = async (docId) => {
  try {
    const payload = await loadPayload()
    return payload.documents.find((doc) => doc?.id === docId) || null
  } catch (error) {
    console.error('获取文档详情失败:', error)
    return null
  }
}

export const searchDocuments = async (query) => {
  try {
    const payload = await loadPayload()
    const keyword = String(query || '').trim().toLowerCase()
    if (!keyword) return []

    return payload.documents.filter((doc) => {
      const title = String(doc?.title || '').toLowerCase()
      const content = String(doc?.content || '').toLowerCase()
      const tags = normalizeArray(doc?.tags).map((tag) => String(tag).toLowerCase())

      return title.includes(keyword) || content.includes(keyword) || tags.some((tag) => tag.includes(keyword))
    })
  } catch (error) {
    console.error('搜索失败:', error)
    return []
  }
}

export const clearDocumentsCache = () => {
  payloadCache = null
  payloadPromise = null
}

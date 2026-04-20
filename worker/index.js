const ALLOWED_IMAGE_HOSTS = new Set(['note.youdao.com', 'cdn.note.youdao.com'])

function jsonError(message, status = 400) {
  return new Response(JSON.stringify({ error: message }), {
    status,
    headers: {
      'content-type': 'application/json; charset=UTF-8',
      'cache-control': 'no-store'
    }
  })
}

async function handleImageProxy(request) {
  const requestUrl = new URL(request.url)
  const targetUrl = requestUrl.searchParams.get('url')

  if (!targetUrl) {
    return jsonError('Missing url query parameter')
  }

  let parsedTarget
  try {
    parsedTarget = new URL(targetUrl)
  } catch {
    return jsonError('Invalid target URL')
  }

  if (!['http:', 'https:'].includes(parsedTarget.protocol)) {
    return jsonError('Unsupported URL scheme')
  }

  if (!ALLOWED_IMAGE_HOSTS.has(parsedTarget.hostname)) {
    return jsonError('Host is not allowed')
  }

  const upstream = await fetch(parsedTarget.toString(), {
    headers: {
      'user-agent': 'Mozilla/5.0 Cloudflare Worker Image Proxy'
    },
    cf: {
      cacheTtl: 86400,
      cacheEverything: true
    }
  }).catch(() => null)

  if (!upstream || !upstream.ok) {
    return jsonError('Failed to fetch upstream image', 502)
  }

  const contentType = upstream.headers.get('content-type') || 'application/octet-stream'
  if (!contentType.startsWith('image/')) {
    return jsonError(`Upstream is not an image: ${contentType}`, 502)
  }

  const headers = new Headers()
  headers.set('content-type', contentType)
  headers.set('cache-control', 'public, max-age=86400')

  const contentLength = upstream.headers.get('content-length')
  if (contentLength) {
    headers.set('content-length', contentLength)
  }

  return new Response(upstream.body, {
    status: 200,
    headers
  })
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url)

    if (url.pathname === '/api/image-proxy') {
      return handleImageProxy(request)
    }

    return env.ASSETS.fetch(request)
  }
}

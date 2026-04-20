const ALLOWED_IMAGE_HOSTS = new Set(['note.youdao.com', 'cdn.note.youdao.com'])

const buildError = (message, status = 400) =>
  new Response(JSON.stringify({ error: message }), {
    status,
    headers: {
      'content-type': 'application/json; charset=UTF-8',
      'cache-control': 'no-store'
    }
  })

export async function onRequestGet(context) {
  const requestUrl = new URL(context.request.url)
  const targetUrl = requestUrl.searchParams.get('url')

  if (!targetUrl) {
    return buildError('Missing url query parameter')
  }

  let parsedTarget
  try {
    parsedTarget = new URL(targetUrl)
  } catch {
    return buildError('Invalid target URL')
  }

  if (!['http:', 'https:'].includes(parsedTarget.protocol)) {
    return buildError('Unsupported URL scheme')
  }

  if (!ALLOWED_IMAGE_HOSTS.has(parsedTarget.hostname)) {
    return buildError('Host is not allowed')
  }

  const upstream = await fetch(parsedTarget.toString(), {
    headers: {
      'user-agent': 'Mozilla/5.0 Cloudflare Pages Image Proxy'
    },
    cf: {
      cacheTtl: 86400,
      cacheEverything: true
    }
  }).catch(() => null)

  if (!upstream || !upstream.ok) {
    return buildError('Failed to fetch upstream image', 502)
  }

  const contentType = upstream.headers.get('content-type') || 'application/octet-stream'
  if (!contentType.startsWith('image/')) {
    return buildError(`Upstream is not an image: ${contentType}`, 502)
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

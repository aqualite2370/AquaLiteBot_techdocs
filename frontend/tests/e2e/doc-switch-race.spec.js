import { test, expect } from '@playwright/test'

test('quickly switching docs keeps latest route content', async ({ page }) => {
  await page.route('**/api/documents/*', async (route) => {
    const url = route.request().url()
    const docId = url.split('/').pop()

    const payloadById = {
      'vue-intro': {
        id: 'vue-intro',
        title: 'Vue Doc (Slow)',
        content: '# Vue Slow',
        category: 'vue',
        tags: ['vue']
      },
      'fastapi-intro': {
        id: 'fastapi-intro',
        title: 'FastAPI Doc (Latest)',
        content: '# FastAPI Latest',
        category: 'fastapi',
        tags: ['fastapi']
      }
    }

    const delayMsById = {
      'vue-intro': 700,
      'fastapi-intro': 50
    }

    const payload = payloadById[docId]
    if (!payload) {
      await route.fallback()
      return
    }

    await page.waitForTimeout(delayMsById[docId] ?? 0)
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(payload)
    })
  })

  await page.goto('/')

  // Trigger the race: first click starts a slow request, second click starts a fast request.
  await page.locator('a[href="/doc/vue-intro"]').first().click({ noWaitAfter: true })
  await page.locator('a[href="/doc/fastapi-intro"]').first().click()

  await expect(page).toHaveURL(/\/doc\/fastapi-intro$/)
  await expect(page.locator('h1')).toHaveText('FastAPI Doc (Latest)')
})

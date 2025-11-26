import { test } from '@playwright/test'

test('debug login page', async ({ page, baseURL }) => {
  const logs = []
  page.on('console', msg => logs.push(`${msg.type()}: ${msg.text()}`))
  page.on('pageerror', err => logs.push(`pageerror: ${err.message}`))

  await page.goto('/login')
  // give scripts a moment to run
  await page.waitForTimeout(500)

  const html = await page.content()
  console.log('--- CONSOLE LOGS ---')
  logs.forEach(l => console.log(l))
  console.log('--- PAGE HTML START ---')
  console.log(html.substring(0, 2000))
  console.log('--- PAGE HTML END ---')
})

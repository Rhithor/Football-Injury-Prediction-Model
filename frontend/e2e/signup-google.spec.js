import { test, expect } from '@playwright/test'

test('signup with google shows social signup form', async ({ page, baseURL }) => {
  // Intercept the backend sign-in start and simulate provider redirect to
  // the social signup page which asks the user to complete the form.
  await page.route('http://localhost:8000/accounts/google/login*', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: `<!doctype html><html><head><meta charset="utf-8" /><title>Redirecting</title><script>window.location='http://localhost:8000/accounts/3rdparty/signup/'</script></head><body>Redirecting</body></html>`
    })
  })

  // Provide a deterministic response for the social signup page so the
  // test doesn't require a running backend.
  await page.route('http://localhost:8000/accounts/3rdparty/signup/', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: `<!doctype html><html><body><h1>Sign Up</h1><div style="display:flex;gap:12px"><img src="https://example.test/avatar.jpg" style="width:48px;height:48px;border-radius:8px"/><div><div style="font-weight:700">Anne Player</div><div style="color:#888">anne@example.test</div></div></div><p>We pre-filled the form below with information from your Google account — please confirm or edit any fields before continuing.</p><form><input name="username" value="anne" type="text"/></form></body></html>`
    })
  })

  await page.goto('/register')
  await expect(page.locator('text=Sign up with Google')).toBeVisible()

  await page.click('text=Sign up with Google')

  // Wait for the simulated social signup page and assert the message is visible
  await page.waitForURL('http://localhost:8000/accounts/3rdparty/signup/')
  await expect(page.locator('text=We pre-filled the form below with information from your Google account')).toBeVisible()
  await expect(page.locator('input[name="username"][value="anne"]')).toBeVisible()
})

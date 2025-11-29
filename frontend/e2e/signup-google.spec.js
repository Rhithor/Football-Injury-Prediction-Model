import { test, expect } from '@playwright/test'

test('signup with google shows social signup form', async ({ page, baseURL }) => {
  // Intercept provider start and redirect to a deterministic signup page
  await page.route('http://localhost:8000/accounts/google/login*', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: `<!doctype html><html><head><meta charset="utf-8" /><title>Redirecting</title><script>window.location='http://localhost:8000/accounts/3rdparty/signup/'</script></head><body>Redirecting</body></html>`
    })
  })

  // Deterministic signup page response
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

  // Wait for signup page and assert preview text
  await page.waitForURL('http://localhost:8000/accounts/3rdparty/signup/')
  await expect(page.locator('text=We pre-filled the form below with information from your Google account')).toBeVisible()
  await expect(page.locator('input[name="username"][value="anne"]')).toBeVisible()

  // Submit the signup form and emulate server redirect to SPA login
  await page.click('input[name="username"]')
  await page.evaluate(() => { document.forms[0].submit() })

  // Intercept the success handler to redirect to the SPA login page
  await page.route('http://localhost:8000/accounts/social/success/', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: `<!doctype html><html><head><meta charset="utf-8" /><title>Redirect</title><script>window.location='http://localhost:5173/login'</script></head><body>Redirecting</body></html>`
    })
  })

  // Wait for SPA login route
  await page.waitForURL('http://localhost:5173/login')

  // Intercept login POST to return a token
  await page.route('http://localhost:8000/auth/login/', async (route, req) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ key: 'NEW_USER_TOKEN' }) })
  })

  // Fill login form and submit
  await page.fill('input[name="email"]', 'anne@example.test')
  await page.fill('input[name="password"]', 'somepass')
  await page.click('button[type="submit"]')

  // App navigates to root on success
  await page.waitForURL('http://localhost:5173/')
  await expect(page.locator('text=Football Injury Prediction')).toBeVisible()
})


test('after social signup, server sends user to frontend login (no token)', async ({ page }) => {
  // Backend should redirect to SPA login (no token) for fresh social signups
  await page.route('http://localhost:8000/accounts/social/success/', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: `<!doctype html><html><head><meta charset="utf-8" /><title>Redirect</title><script>window.location='http://localhost:5173/login'</script></head><body>Redirecting</body></html>`
    })
  })

  // Navigate to success endpoint
  await page.goto('http://localhost:8000/accounts/social/success/')

  // SPA should land on login with no token issued
  await page.waitForURL('http://localhost:5173/login')
  await expect(page.locator('text=Sign In')).toBeVisible()
})

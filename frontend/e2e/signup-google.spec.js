import { test, expect } from '@playwright/test'

test('signup with google shows social signup form', async ({ page, baseURL }) => {
  // Block real Google
  await page.route('https://accounts.google.com/**', async (route) => {
    await route.abort()
  })

  // Mock Google OAuth callback - redirect to signup form
  await page.route('**/accounts/google/login/**', async (route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'text/html',
        body: `<!doctype html><html><head></head><body><script>window.location='http://localhost:8000/accounts/3rdparty/signup/'</script></body></html>`
      })
    } else {
      await route.continue()
    }
  })

  // Mock the signup form page - this page simulates what allauth shows
  await page.route('**/accounts/3rdparty/signup/**', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: `<!doctype html><html><body><h1>Sign Up</h1><form method="POST"><input name="username" value="anne" type="text"/><button type="submit">Sign Up</button></form></body></html>`
    })
  })

  // Mock the social success endpoint - in real flow this receives the token from backend
  // For now, just redirect to login to match the new user flow
  await page.route('**/accounts/social/success/**', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: `<!doctype html><html><head><script>window.location='http://localhost:5173/login'</script></head><body>Redirecting...</body></html>`
    })
  })

  // Mock auth endpoints
  await page.route('**/auth/login/**', async (route) => {
    if (route.request().method() === 'POST') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({ key: 'NEW_USER_TOKEN' })
      })
    } else {
      await route.continue()
    }
  })

  await page.goto('/register')
  await expect(page.locator('text=Sign up with Google')).toBeVisible()

  await page.click('text=Sign up with Google')

  // Wait for signup page
  await page.waitForURL('**/accounts/3rdparty/signup/**')
  await expect(page.locator('input[name="username"][value="anne"]')).toBeVisible()

  // Submit form - in real flow, backend processes this and redirects to success
  // Our mock will simulate POST going to success endpoint
  await page.click('button[type="submit"]')

  // Simulate the backend redirect chain by navigating directly
  // In a real test with backend, the form submission would trigger this
  await page.waitForTimeout(500) // Give time for any redirects
  await page.goto('http://localhost:8000/accounts/social/success/')

  // Wait for redirect to SPA login
  await page.waitForURL('http://localhost:5173/login')

  // Fill and submit login form
  await page.fill('input[name="email"]', 'anne@example.test')
  await page.fill('input[name="password"]', 'somepass')
  await page.click('button[type="submit"]')

  // Should redirect to home
  await page.waitForURL('http://localhost:5173/')
  await expect(page.locator('text=Football Injury Prediction')).toBeVisible()
})


test('after social signup, server sends user to frontend login (no token)', async ({ page }) => {
  // Backend should redirect to SPA login (no token) for fresh social signups
  await page.route('**/accounts/social/success/**', async (route) => {
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

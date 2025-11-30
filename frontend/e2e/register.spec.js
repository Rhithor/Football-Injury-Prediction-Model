import { test, expect } from '@playwright/test'

test('register returns token and app stores it', async ({ page, baseURL }) => {
  await page.goto('/register')

  // Intercept registration to return a token
  await page.route('http://localhost:8000/auth/registration/', async route => {
    await route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({ key: 'REG_TOKEN' }) })
  })

  await page.fill('input[name="username"]', 'reguser')
  await page.fill('input[name="email"]', 'reg@example.test')
  await page.fill('input[name="password1"]', 'pass1234')
  await page.fill('input[name="password2"]', 'pass1234')
  await page.click('button[type="submit"]')

  // After registration with token the app should store token and land on '/'
  await page.waitForSelector('text=Sign Out', { timeout: 3000 })
  const stored = await page.evaluate(() => localStorage.getItem('authToken'))
  expect(stored).toBe('REG_TOKEN')
})

test('register without token redirects to login', async ({ page, baseURL }) => {
  await page.goto('/register')

  // Intercept registration response that doesn't include a token
  await page.route('http://localhost:8000/auth/registration/', async route => {
    await route.fulfill({ status: 201, contentType: 'application/json', body: JSON.stringify({}) })
  })

  await page.fill('input[name="username"]', 'reguser2')
  await page.fill('input[name="email"]', 'reg2@example.test')
  await page.fill('input[name="password1"]', 'pass1234')
  await page.fill('input[name="password2"]', 'pass1234')
  await page.click('button[type="submit"]')

  // Should be redirected to login page and not have authToken
  await page.waitForURL('http://localhost:5173/login')
  const stored = await page.evaluate(() => localStorage.getItem('authToken'))
  expect(stored).toBe(null)
})

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

  // Simulate the user submitting the social signup form — after submitting
  // the backend would redirect to /accounts/social/success/ where the
  // application will decide whether to hand out a token or redirect to
  // the frontend login page for manual signups. We'll emulate the
  // server redirect to /accounts/social/success/ and then emulate that
  // endpoint sending the user to the frontend login route.
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

  // Wait until SPA arrives at login page
  await page.waitForURL('http://localhost:5173/login')

  // Now simulate the user entering password and logging in — intercept
  // the backend login POST to return a token and ensure SPA navigates to '/'
  await page.route('http://localhost:8000/auth/login/', async (route, req) => {
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ key: 'NEW_USER_TOKEN' }) })
  })

  // Fill login form and submit
  await page.fill('input[name="email"]', 'anne@example.test')
  await page.fill('input[name="password"]', 'somepass')
  await page.click('button[type="submit"]')

  // App should navigate to root after successful login
  await page.waitForURL('http://localhost:5173/')
  await expect(page.locator('text=Football Injury Prediction')).toBeVisible()
})


test('after social signup, server sends user to frontend login (no token)', async ({ page }) => {
  // Simulate the backend route that would normally issue a token for
  // authenticated social logins. For a recently signed up user the
  // backend should redirect the browser to the frontend login page
  // rather than sending an auth token.
  await page.route('http://localhost:8000/accounts/social/success/', async (route) => {
    await route.fulfill({
      status: 200,
      contentType: 'text/html',
      body: `<!doctype html><html><head><meta charset="utf-8" /><title>Redirect</title><script>window.location='http://localhost:5173/login'</script></head><body>Redirecting</body></html>`
    })
  })

  // Kick off the flow by navigating the user to the success endpoint
  // (the backend would normally redirect here).
  await page.goto('http://localhost:8000/accounts/social/success/')

  // The SPA should land on the login route and not receive a token.
  await page.waitForURL('http://localhost:5173/login')
  await expect(page.locator('text=Sign In')).toBeVisible()
})

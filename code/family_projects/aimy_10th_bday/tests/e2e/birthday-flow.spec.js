import { test, expect } from '@playwright/test'

test.describe('Birthday Riddle Presentation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('full happy path - all riddles and challenges', async ({ page }) => {
    // Slide 1: Intro
    await expect(page.getByText('אוי לא!')).toBeVisible()
    await page.getByText('!יאללה').click()

    // Slide 2: Riddle 1 - בלון
    await expect(page.getByText('חידה 1')).toBeVisible()
    await page.getByTestId('answer-input').fill('בלון')
    await page.getByTestId('submit-button').click()
    await expect(page.getByTestId('message')).toContainText('נכון')
    await page.waitForTimeout(1500)

    // Slide 3: Transition 1
    await expect(page.getByText('כל הכבוד!')).toBeVisible()
    await page.getByText('!סיימתי').click()

    // Slide 4: Riddle 2 - שיר
    await expect(page.getByText('חידה 2')).toBeVisible()
    await page.getByTestId('answer-input').fill('שיר')
    await page.getByTestId('submit-button').click()
    await expect(page.getByTestId('message')).toContainText('נכון')
    await page.waitForTimeout(1500)

    // Slide 5: Transition 2
    await expect(page.getByText('מעולה!')).toBeVisible()
    await page.getByText('!סיימתי').click()

    // Slide 6: Video
    await expect(page.getByText('הפתעה!')).toBeVisible()
    await expect(page.getByTestId('video-player')).toBeVisible()
    await page.getByText('!המשך').click()

    // Slide 7: Riddle 3 - מתנה
    await expect(page.getByText('חידה 3')).toBeVisible()
    await page.getByTestId('answer-input').fill('מתנה')
    await page.getByTestId('submit-button').click()
    await expect(page.getByTestId('message')).toContainText('נכון')
    await page.waitForTimeout(1500)

    // Slide 8: Transition 3
    await expect(page.getByText('יופי!')).toBeVisible()
    await page.getByText('!סיימתי').click()

    // Slide 9: Riddle 4 - עוגה
    await expect(page.getByText('חידה 4')).toBeVisible()
    await page.getByTestId('answer-input').fill('עוגה')
    await page.getByTestId('submit-button').click()
    await expect(page.getByTestId('message')).toContainText('נכון')
    await page.waitForTimeout(1500)

    // Slide 10: Final
    await expect(page.getByText('!כל הכבוד')).toBeVisible()
    await expect(page.getByText('!פתרת את כל החידות')).toBeVisible()
  })

  test('wrong answer shows error and hint after 2 attempts', async ({ page }) => {
    await page.getByText('!יאללה').click()
    await expect(page.getByText('חידה 1')).toBeVisible()

    // First wrong attempt
    await page.getByTestId('answer-input').fill('כדור')
    await page.getByTestId('submit-button').click()
    await expect(page.getByTestId('message')).toContainText('לא נכון')
    await expect(page.getByTestId('hint')).toHaveCount(0)

    // Second wrong attempt - hint should appear
    await page.getByTestId('answer-input').clear()
    await page.getByTestId('answer-input').fill('שמש')
    await page.getByTestId('submit-button').click()
    await expect(page.getByTestId('hint')).toBeVisible()

    // Correct answer still works
    await page.getByTestId('answer-input').clear()
    await page.getByTestId('answer-input').fill('בלון')
    await page.getByTestId('submit-button').click()
    await expect(page.getByTestId('message')).toContainText('נכון')
  })

  test('progress bar updates as slides progress', async ({ page }) => {
    await expect(page.getByTestId('progress-dot-0')).toHaveClass(/active/)
    await page.getByText('!יאללה').click()
    await expect(page.getByTestId('progress-dot-1')).toHaveClass(/active/)
    await expect(page.getByTestId('progress-dot-0')).toHaveClass(/completed/)
  })

  test('app has RTL direction', async ({ page }) => {
    const html = page.locator('html')
    await expect(html).toHaveAttribute('dir', 'rtl')
    await expect(html).toHaveAttribute('lang', 'he')
  })

  test('restart from final slide returns to intro', async ({ page }) => {
    // Speed-run through all slides
    await page.getByText('!יאללה').click()

    await page.getByTestId('answer-input').fill('בלון')
    await page.getByTestId('submit-button').click()
    await page.waitForTimeout(1500)
    await page.getByText('!סיימתי').click()

    await page.getByTestId('answer-input').fill('שיר')
    await page.getByTestId('submit-button').click()
    await page.waitForTimeout(1500)
    await page.getByText('!סיימתי').click()

    await page.getByText('!המשך').click()

    await page.getByTestId('answer-input').fill('מתנה')
    await page.getByTestId('submit-button').click()
    await page.waitForTimeout(1500)
    await page.getByText('!סיימתי').click()

    await page.getByTestId('answer-input').fill('עוגה')
    await page.getByTestId('submit-button').click()
    await page.waitForTimeout(1500)

    await expect(page.getByText('!כל הכבוד')).toBeVisible()
    await page.getByText('!שחקי שוב').click()
    await expect(page.getByText('אוי לא!')).toBeVisible()
  })
})

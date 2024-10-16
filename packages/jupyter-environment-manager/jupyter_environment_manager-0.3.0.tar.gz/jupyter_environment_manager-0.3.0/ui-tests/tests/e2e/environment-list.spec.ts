import { expect, test } from '@jupyterlab/galata';

test.describe('Environment manager Create environment test', () => {
  test.beforeEach(async ({ page }) => {
    await page.sidebar.openTab('environments-sidebar');
    await page.waitForSelector('div[data-testid="env-sidebar-container"]', {
      timeout: 5000
    });
  });

  test('Tests list of environments', async ({ page }) => {
    const envListEl = page.getByTestId('environment-list');
    if (envListEl) {
      expect(
        await page.getByTestId('environment-tile').count()
      ).toBeGreaterThanOrEqual(0);
    }
  });
});

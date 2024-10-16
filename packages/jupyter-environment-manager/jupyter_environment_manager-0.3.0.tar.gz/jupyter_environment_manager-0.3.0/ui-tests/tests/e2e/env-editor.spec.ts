import { expect, test } from '@jupyterlab/galata';

test.describe('Environment manager Create environment test', () => {
  test.beforeEach(async ({ page }) => {
    await page.sidebar.openTab('environments-sidebar');
    await page.waitForSelector('div[data-testid="env-sidebar-container"]', {
      timeout: 5000
    });
  });

  test('Tests environment editor', async ({ page }) => {
    const envListEl = page.getByTestId('environment-list');
    if (envListEl) {
      const envTile = page.getByTestId('environment-tile');
      const count = await envTile.count();

      if (count > 0) {
        await envTile.nth(0).click();
        await page.getByTestId('env-more-btn').nth(0).click();
        await page.waitForSelector(
          'div[data-testid="environment-editor-container"]',
          {
            timeout: 5000
          }
        );
        expect(page.getByTestId('env-editor-title')).toBeInViewport();
        expect(page.getByTestId('env-editor-info-pane')).toBeVisible();
        expect(page.getByTestId('env-editor-sharing-pane')).toBeVisible();
        expect(page.getByTestId('env-editor-package-pane')).toBeVisible();
      }
    }
  });
});

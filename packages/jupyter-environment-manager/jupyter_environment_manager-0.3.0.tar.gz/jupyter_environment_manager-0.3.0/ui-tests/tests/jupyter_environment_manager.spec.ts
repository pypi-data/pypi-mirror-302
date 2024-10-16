import { expect, test } from '@jupyterlab/galata';

test.describe('Environment manager extension test', () => {
  test.beforeEach(async ({ page }) => {
    await page.sidebar.openTab('environments-sidebar');
    await page.waitForSelector('div[data-testid="env-sidebar-container"]', {
      timeout: 5000
    });
  });

  test('Renders ui properly', async ({ page }) => {
    expect(page.getByTestId('installed-env-header')).toHaveText('Environments');
    expect(page.getByTestId('env-sidebar-container')).toBeVisible();
    expect(page.getByTestId('env-action-btn')).toBeVisible();
    expect(page.getByTestId('env-refresh-btn')).toBeVisible();
    expect(page.getByTestId('env-docs-btn')).toBeVisible();
    expect(page.getByTestId('env-list-container')).toBeInViewport();
  });
});

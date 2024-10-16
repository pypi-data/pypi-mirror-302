import { expect, test } from '@jupyterlab/galata';

test('Refresh btn working properly', async ({ page }) => {
  await page.sidebar.openTab('environments-sidebar');
  await page.waitForSelector('div[data-testid="env-sidebar-container"]', {
    timeout: 5000
  });
  expect(page.getByTestId('env-refresh-btn')).toBeVisible();
  const allEnvPromise = page.waitForResponse('**/api/environments');
  const installedEnvResponsePromise = page.waitForResponse(
    '**/jupyter-environment-manager/**'
  );
  await page.getByTestId('env-refresh-btn').click();
  const allEnvResponse = await allEnvPromise;
  const installedEnvResponse = await installedEnvResponsePromise;
  expect(allEnvResponse.status()).toBe(200);
  expect(installedEnvResponse.status()).toBe(200);
});

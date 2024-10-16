import { expect, test } from '@jupyterlab/galata';

test.describe('Environment manager Create environment test', () => {
  test.beforeEach(async ({ page }) => {
    await page.sidebar.openTab('environments-sidebar');
    await page.waitForSelector('div[data-testid="env-sidebar-container"]', {
      timeout: 5000
    });
  });

  test('Test ui and env submission', async ({ page }) => {
    expect(page.getByTestId('env-action-btn')).toBeVisible();
    const actionContext = await page
      .getByTestId('env-action-btn')
      .textContent();

    if (actionContext === '+ Create') {
      expect(actionContext).toBe('+ Create');
      await page.getByTestId('env-action-btn').click();

      page.waitForTimeout(5000);

      expect(page.getByTestId('create-env-header')).toBeInViewport();
      // title
      await page.getByTestId('env-create-title').click();
      await page.keyboard.type('env-test');

      // description
      await page.getByTestId('env-create-description').click();
      await page.keyboard.type('env-description');

      // tags
      await page.getByTestId('env-create-tag').click();
      await page.keyboard.type('tag');
      await page.keyboard.press('Enter');

      // code
      await page.getByTestId('env-create-code').click();
      await page.keyboard.type('#this is test');

      expect(page.getByTestId('env-create-submit-btn')).toBeVisible();

      // submit
      // const creationPromise = page.waitForResponse("**/environments/create")
      // await page.getByTestId('env-create-submit').click();
      // const creationResponse = await creationPromise;
      // expect(creationResponse.status()).toBe(200);
    } else {
      expect(actionContext).toBe('+ Add');
    }
  });
});

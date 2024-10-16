// global-setup.ts
import { chromium, FullConfig } from '@playwright/test';
import { Auth } from '@aws-amplify/auth';

Auth.configure({
  region: 'us-east-1',
  userPoolId: 'us-east-1_7hq9OmpnT',
  userPoolWebClientId: '70fo00fpob1sd133m98k7b0jan'
});

const EMAIL = 'markovshama@gmail.com';
const PASSWORD = 'qBraid2!';
const BASE_URL = 'http://localhost:8888/lab';

async function globalSetup(config: FullConfig) {
  const username = EMAIL;
  const password = PASSWORD;
  const { baseURL, storageState } = config.projects[0].use;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const context = await browser.newContext();

  const signIn = await Auth.signIn({ username, password });
  const refreshToken = signIn?.signInUserSession?.refreshToken?.token;
  const email = signIn?.attributes?.email;

  // Here follows the step to log in if you setup a known password
  // See the server documentation https://jupyter-server.readthedocs.io/en/latest/operators/public-server.html?#automatic-password-setup
  await page.context().addCookies([
    { name: 'EMAIL', value: email, url: BASE_URL },
    { name: 'REFRESH', value: refreshToken, url: BASE_URL }
  ]);
  await page.goto(BASE_URL);
  await page.context().storageState({ path: storageState as string });
  await browser.close();
}

export default globalSetup;

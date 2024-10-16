/**
 * Configuration for Playwright using default from @jupyterlab/galata
 */
const baseConfig = require('@jupyterlab/galata/lib/playwright-config');

module.exports = {
  ...baseConfig,
  gloablSetup: require.resolve('./global-setup'),
  use: {
    ...baseConfig.use,
    storageState: 'storageState.json'
  }
};

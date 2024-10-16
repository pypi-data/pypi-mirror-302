import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ICommandPalette } from '@jupyterlab/apputils';
import svgString from './assets/icons/IconString';
import { LabIcon } from '@jupyterlab/ui-components';
import { EnvironmentsSidebarWidget } from './EnvironmentsSidebarWidget';
import Flux from './Flux';
import { API_URL } from './actions/ApiActions';

const envsIcon = new LabIcon({
  name: 'environments-sidebar:icon',
  svgstr: svgString
});

const CreateEnvWidget = (flux: any, app: JupyterFrontEnd) => {
  const envsSidebarWidget: EnvironmentsSidebarWidget =
    new EnvironmentsSidebarWidget(flux, app); // create the envsSidebarWidget
  envsSidebarWidget.id = 'environments-sidebar';
  envsSidebarWidget.title.label = 'ENVS';
  envsSidebarWidget.title.caption = 'Environment Manager';
  envsSidebarWidget.title.className = 'environment_sidebar_li';
  envsSidebarWidget.title.icon = envsIcon;
  envsSidebarWidget.title.iconClass = 'env_icon_parent';
  return envsSidebarWidget;
};

const extension: JupyterFrontEndPlugin<void> = {
  id: '@qbraid/jupyter-environment-manager',
  autoStart: true,
  activate: async (app: JupyterFrontEnd, palette: ICommandPalette) => {
    const { commands } = app;

    const flux = new Flux({
      apiBaseUrl: API_URL,
      jupyterlab: app
    });
    try {
      const authActions = flux.getActions('AuthActions');
      const userActions = flux.getActions('UserActions');
      const environmentActions = flux.getActions('EnvironmentActions');
      console.log('loading env manager');

      // Load data prior to loading UI. If errors are encountered in any
      // AuthActions or UserActions, they will still resolve successfully to
      // allow the sidebar to load with a "No User Found" instead of crashing.
      await authActions.getUser();
      await userActions.getLocalConfig();
      await userActions.getUser();
      await userActions.checkFileMount();
      try {
        // EnvironmentActions are not required to resolve successfully in the case of
        // 400 errors, so we need to catch them here to prevent the sidebar from crashing.
        await environmentActions.updateAll();
        await environmentActions.registerInstalled();
        userActions.verifyUserSession();
      } catch (err) {
        console.error('Error updating environments', err);
      }

      // mark environments that are installed on the filesystem as such
      let envsSidebarWidget = CreateEnvWidget(flux, app);
      app.shell.add(envsSidebarWidget, 'right', { rank: 1 }); // add it to the frontend shell (still hidden at this point)
      // BEGIN environments sidebar widget
      app.shell.activateById('environments-sidebar');

      // "Environments" command - opens the sidebar
      const cmdOpenEnvironmentsSidebar = 'environment-manager:open-sidebar';
      commands.addCommand(cmdOpenEnvironmentsSidebar, {
        caption: 'Environments',
        label: 'Environments',
        icon: undefined, // todo
        execute: () => {
          console.log('open env maanger');
          if (envsSidebarWidget) {
            // this happens for the second and all subsequent open actions
            envsSidebarWidget.dispose(); // always dispose and remount, per jlab conventions
          }
          envsSidebarWidget = CreateEnvWidget(flux, app);
          app.shell.add(envsSidebarWidget, 'right', {
            rank: 1
          }); // add it to the frontend shell (still hidden at this point)
          app.shell.activateById('environments-sidebar'); // activate the widget in the sidebar
        }
      });

      if (palette) {
        palette.addItem({
          command: cmdOpenEnvironmentsSidebar,
          category: 'qBraid Ecosystem',
          args: { origin: 'from the palette' }
        });
        // END environments sidebar widget
      }

      // env-manager close commands
      const cmdCloseEnvironmentsSidebar = 'environment-manager:close-sidebar';
      commands.addCommand(cmdCloseEnvironmentsSidebar, {
        caption: 'Environments',
        label: 'Environments',
        icon: undefined, // todo
        execute: () => {
          if (envsSidebarWidget) {
            // this happens for the second and all subsequent close actions
            envsSidebarWidget.dispose(); // always dispose and remount, per jlab conventions
          }
          envsSidebarWidget = CreateEnvWidget(flux, app);
          app.shell.add(envsSidebarWidget, 'right', {
            rank: 1
          }); // add it to the frontend shell (still hidden at this point)
        }
      });

      if (palette) {
        palette.addItem({
          command: cmdCloseEnvironmentsSidebar,
          category: 'qBraid Ecosystem',
          args: { origin: 'from the palette' }
        });
      }
      // END environments sidebar widget

      // function returns a widget that creates a browser sandbox inside jupyter lab

      // Opens quantum device docs inside jupyter lab inbuild browser
      const cmdEnvMangerDocsReference = 'docs:qbraid-env-manager';
      commands.addCommand(cmdEnvMangerDocsReference, {
        label: 'Environment Manager Reference',
        execute: () => {
          const url = 'https://docs.qbraid.com/lab/user-guide/environments';
          window.open(url, '_blank');
        }
      });
    } catch (err) {
      console.log('\n[!] Failed to activate environment-manager [!]\n');
      console.error(err);
    }
  }
};

export default extension;

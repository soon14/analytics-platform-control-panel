moj.Modules.toolStatus = {
  actionClass: ".tool-action",
  buttonClass: ".govuk-button",
  eventType: "toolStatus",
  hidden: "govuk-visually-hidden",
  listenerClass: ".tool",
  statusLabelClass: ".tool-status-label",

  versionSelector: "select[name='version']",
  versionNotInstalledClass: "not-installed",
  versionInstalledClass: "installed",
  installedSuffix: " (installed)",

  init() {
    const toolStatusListeners = document.querySelectorAll(this.listenerClass);
    if (toolStatusListeners) {
      this.bindEvents(toolStatusListeners);
    }

    // Bind version selects' change event listeners
    const versionSelects = document.querySelectorAll(this.versionSelector);
    versionSelects.forEach(versionSelect => {
      versionSelect.addEventListener("change", (event) => this.versionSelectChanged(event.target));
    });
  },

  bindEvents(listeners) {
    listeners.forEach(listener => {
      moj.Modules.eventStream.addEventListener(
        this.eventType,
        this.buildEventHandler(listener)
      );
    });
  },

  buildEventHandler(listener) {
    const toolstatus = this;
    return event => {
      const data = JSON.parse(event.data);
      if (data.toolName != listener.dataset.toolName) {
        return;
      }
      listener.querySelector(toolstatus.statusLabelClass).innerText = data.status;
      switch (data.status.toUpperCase()) {
        case 'NOT DEPLOYED':
          toolstatus.showActions(listener, ['deploy']);
          break;
        case 'DEPLOYING':
          toolstatus.showActions(listener, []);
          // maybe have a Cancel button? Report issue?
          break;
        case 'READY':
        case 'IDLED':
          toolstatus.showActions(listener, ['deploy', 'open', 'restart', 'remove']);
          toolstatus.updateAppVersion(listener, data.version);
          break;
        case 'FAILED':
          toolstatus.showActions(listener, ['deploy', 'restart', 'remove']);
          break;
      }
    };
  },

  // Select the new version from the tool "version" select input
  updateAppVersion(listener, newVersion) {
    const selectElement = listener.querySelector(this.versionSelector);

    if (newVersion) {
      // 1. remove "(not installed)" option
      let notInstalledOption = selectElement.querySelector("option." + this.versionNotInstalledClass);

      if (notInstalledOption) {
        notInstalledOption.remove();
      }

      // 2. remove "(installed)" suffix and class from old version
      let oldVersionOption = selectElement.querySelector("option." + this.versionInstalledClass);

      if (oldVersionOption) {
        oldVersionOption.innerText = oldVersionOption.innerText.replace(this.installedSuffix, "");
        oldVersionOption.classList.remove(this.versionInstalledClass);
      }

      // 3. add "(installed)" suffix and class to new version
      let newVersionOption = listener.querySelector(this.versionSelector + " option[value='" + newVersion + "']");

      if (newVersionOption) {
        newVersionOption.innerText = newVersionOption.innerText + this.installedSuffix;
        newVersionOption.classList.add(this.versionInstalledClass)
      }
    }

    // After deploy, update select/deploy button
    this.versionSelectChanged(selectElement);
  },

  showActions(listener, actionNames) {
    listener.querySelectorAll(this.actionClass).forEach(action => {
      const actionName = action.dataset.actionName;
      const button = listener.querySelector(`${this.buttonClass}[data-action-name='${actionName}']`);

      if (actionNames.includes(actionName)) {
        button.removeAttribute("disabled");
      } else {
        button.setAttribute("disabled", true);
      }
    });
  },

  // version select "change" event handler
  versionSelectChanged(target) {
    const selected = target.options[target.options.selectedIndex];
    const classes = selected.className.split(" ");

    const notInstalledSelected = classes.indexOf(this.versionNotInstalledClass) !== -1;
    const installedSelected = classes.indexOf(this.versionInstalledClass) !== -1;

    const targetTool = target.attributes["data-action-target"];
    const deployButton = document.getElementById("deploy-" + targetTool.value);

    // If "(not installed)" or "(installed)" version selected
    // the "Deploy" button needs to be disabled
    deployButton.disabled = notInstalledSelected || installedSelected;
  },
};

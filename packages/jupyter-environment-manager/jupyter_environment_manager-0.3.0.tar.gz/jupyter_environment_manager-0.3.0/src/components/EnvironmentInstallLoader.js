import React, { useState, useEffect } from 'react';
import '../../style/EnvironmentInstallLoader.css';

const EnvironmentInstallLoader = () => {
  return (
    <div class="env-install-loader container">
      <div class="loader">
        <div class="crystal"></div>
        <div class="crystal"></div>
        <div class="crystal"></div>
        <div class="crystal"></div>
        <div class="crystal"></div>
        <div class="crystal"></div>
      </div>
    </div>
  );
};

export default EnvironmentInstallLoader;

import React, { useState, useEffect } from 'react';
import '../../style/LogoLoader.css';

const logoData = {
  nvidia: {
    url: 'https://qbraid-static.s3.amazonaws.com/logos/nvidia.png',
    name: 'nvidia',
    logo_class: ''
  },
  amd: {
    url: 'https://qbraid-static.s3.amazonaws.com/logos/amd.png',
    name: 'amd',
    logo_class: 'invert'
  }
};

const logoInfo = ['nvidia', 'amd'];

const LogoLoader = ({ isCuda = false }) => {
  const [currentLogo, setCurrentLogo] = useState();

  useEffect(() => {
    let i = 0;
    setCurrentLogo(logoData['nvidia']);
    // i++ & logoData.length
    let timer;
    if (!isCuda) {
      timer = setInterval(() => {
        setCurrentLogo(logoData[logoInfo[i++ % logoInfo.length]]);
      }, 1500);
    }

    return () => clearInterval(timer);
  }, [isCuda]);

  return (
    <div
      className={currentLogo?.name}
      style={{ animationIterationCount: isCuda && 'infinite' }}
    >
      <img
        src={currentLogo?.url}
        width={200}
        height={40}
        className={currentLogo?.logo_class}
      />
    </div>
  );
};

export default LogoLoader;

import Header from '@/components/shared/Header';
import React from 'react';


const RootLayout = ({ children }) => {
  return (
    <div>
      <Header />
      {children}
    </div>
  );
};

export default RootLayout;

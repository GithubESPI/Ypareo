import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import ViewBulletins from './_root/page/ViewBulletins.jsx';
import Profile from './_root/page/Profile.jsx';
import RootLayout from './_root/RootLayout';

ReactDOM.createRoot(document.getElementById('root')).render(
  <Router>
    <RootLayout>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/viewBulletins" element={<ViewBulletins />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
    </RootLayout>
  </Router>
);
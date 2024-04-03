import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import App from './App.jsx'
import './index.css'
import ViewBulletins from './_root/page/ViewBulletins.jsx';
import Profile from './_root/page/Profile.jsx';


ReactDOM.createRoot(document.getElementById('root')).render(
  <Router>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/viewBulletins" element={<ViewBulletins />} />
        <Route path="/profile" element={<Profile />} />
      </Routes>
  </Router>
)

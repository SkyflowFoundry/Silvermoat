import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

// Hide loading screen after React app is mounted
// This will wait for the minimum 3 seconds defined in index.html
if (window.hideLoadingScreen) {
  window.hideLoadingScreen()
}


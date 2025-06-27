import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import v1 from './imgs/v1.mp4'

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <div className='videoDiv'>
        <video src={v1} className='video' autoPlay loop muted/>
        <div className='overlay-dark'>
        </div>
        <div className='overlay'>
            <App />
        </div>
    </div>
    
  </React.StrictMode>
);

reportWebVitals();
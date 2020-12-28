import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const [artists, setArtists] = useState(0);

  useEffect(() => {
    fetch('/artists').then(res => res.json()).then(data => {
       setArtists(data.artists);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        { artists.map((artist, index) => <p key={index}>{artist}</p>)}
      </header>
    </div>
  );
}

export default App;

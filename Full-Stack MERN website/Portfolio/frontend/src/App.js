import './App.css'
import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { useState } from 'react';
import HomePage from './pages/HomePage';
import AddGamePage from './pages/AddGamePageTable';
import GamePage from './pages/GamePage';
import EditGamePage from './pages/EditGamePageTable';
import Nav from './components/Nav';
import TopicsPage from './pages/TopicsPage';
//On edit, cannot get shit to work. chart not displaying, update not going through
function App() {
  const [game, setGame] = useState([])
  return (
    <div>
      <BrowserRouter>
        <header>
          <h1><img src="./android-chrome-192x192.png" alt="Portfolio Site Logo"/>Ryan Dobkin</h1>
        </header>
        <Nav/>
        <main>
          <section>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/topics" element={<TopicsPage />} />
              <Route path="/game-list" element={<GamePage setGame={setGame}/>} />
              <Route path="/edit-game" element={<EditGamePage game={game}/>} />
              <Route path="/add-game" element={<AddGamePage />} />
            </Routes>
          </section>
        </main>
        <footer>
          <p><cite>&copy; 2024 Ryan Dobkin</cite></p>
        </footer>
        </BrowserRouter>
      </div>
  );
}

export default App;
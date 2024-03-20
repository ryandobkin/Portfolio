import { React, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { RiGameFill } from 'react-icons/ri'
import GameTable from '../components/GameTable';

function GamePage({ setGame }) {
    // Use the Navigate for redirection
    const redirect = useNavigate();

    // Use state to bring in the data
    const [games, setGames] = useState([]);

    // RETRIEVE the entire list of games
    const loadGames = async () => {
        const response = await fetch('/games');
        const games = await response.json();
        setGames(games);
    }
    

    // UPDATE a single game
    const onEditGame = async game => {
        setGame(game);
        redirect("/edit-game");
    }


    // DELETE a single game  
    const onDeleteGame = async _id => {
        const response = await fetch(`/games/${_id}`, { method: 'DELETE'});
        if (response.status === 200) {
            const getResponse = await fetch('/games');
            const games = await getResponse.json();
            setGames(games);
        } else {
            console.error(`Game entry at id:${_id} failed to delete due to (status) ${response.status}`)
        }
    }

    // LOAD all the games
    useEffect(() => {
        loadGames();
    }, []);

    // DISPLAY the games
    return (
        <>
            <h2><i class='icon'><RiGameFill /></i> List of Games</h2>
            <article>
            <p>Click the add, remove, or edit icons to update the list of game entries.</p>
                <GameTable
                    games={games} 
                    onEdit={onEditGame} 
                    onDelete={onDeleteGame} 
                />
            </article>
        </>
    );
}

export default GamePage;
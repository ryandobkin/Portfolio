import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import { RiGameFill } from 'react-icons/ri'

// Change the icons, function names, and parameters 
// to fit your portfolio topic and schema.

export const AddGamePageTable = () => {

    const [name, setName]       = useState('');
    const [price, setPrice]     = useState('');
    const [rating, setRating]   = useState('');
    const [date, setDate]       = useState('');
    
    const redirect = useNavigate();

    const addGame = async () => {
        const newGame = { name, price, rating, date };
        const response = await fetch('/games', {
            method: 'post',
            body: JSON.stringify(newGame),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        if(response.status === 201){
            alert(`Successfully added game to entry.`);
        } else {
            alert(`Entry failed due to missing data: (status code ${response.status})`);
        }
        redirect("/");
    };


    return (
        <>
        <article>
            <h2><i class='icon'><RiGameFill /></i> Add a game</h2>
            <p>Please enter all fields:</p>
            
            <table id="games">
                <caption>Which game are you adding?</caption>
                <thead>
                    <tr>Add a game to the list</tr>
                </thead>
                <tbody>
                <tr>
                <td><label for="name">Name</label>
                        <input
                            type="text"
                            placeholder="Name of the game"
                            value={name}
                            onChange={e => setName(e.target.value)} 
                            id="name" />
                    </td>

                    <td><label for="price">Price</label>
                        <input
                            type="number"
                            value={price}
                            placeholder="Price of the game"
                            onChange={e => setPrice(e.target.value)} 
                            id="price" />
                    </td>

                    <td><label for="rating">Rating</label>
                        <input
                            type="number"
                            placeholder="Rating of the game"
                            value={rating}
                            onChange={e => setRating(e.target.value)} 
                            id="rating" />
                    </td>

                    <td><label for="date">Date</label>
                        <input
                            type="date"
                            placeholder="Release Date of the game"
                            value={date}
                            onChange={e => setDate(e.target.value)} 
                            id="date" />
                    </td>

                    <td>
                    <label for="submit">Add</label>
                        <button
                            type="add"
                            onClick={addGame}
                            id="submit"
                        >Add</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </article>
    </>
);
}

export default AddGamePageTable;
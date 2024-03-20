import React, { useState }  from 'react';
import { useNavigate } from "react-router-dom";

export const EditGamePageTable = ({ game }) => {
 
    const [name, setName]         = useState(game.name);
    const [price, setPrice]       = useState(game.price);
    const [rating, setRating]     = useState(game.rating);
    const [date, setDate]         = useState(game.date);
    
    const redirect = useNavigate();

    const editGame = async () => {
        const response = await fetch(`/games/${game._id}`, {
            method: 'PUT',
            body: JSON.stringify({ 
                name: name, 
                price: price, 
                rating: rating,
                date: date
            }),
            headers: {'Content-Type': 'application/json',},
        });

        if (response.status === 200) {
            alert(`Successfully edited entry.`);
        } else {
            const errMessage = await response.json();
            alert(`Error editing entry: (Status ${response.status}. ${errMessage.Error})`);
        }
        redirect("/");
    }

    return (
        <>
            <h2>Edit a game</h2>
            <p>Paragraph about this page.</p>
            <table id="games">
                <caption>Which game are you adding?</caption>
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Price</th>
                        <th>Rating</th>
                        <th>Date</th>
                    </tr>
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
                    <label for="submit">Commit</label>
                        <button
                            type="submit"
                            onClick={editGame}
                            id="submit"
                        >Edit</button>
                    </td>
                </tr>
                </tbody>
            </table>
        </>
    );
}
export default EditGamePageTable;
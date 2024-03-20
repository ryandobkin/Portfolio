import React from "react";
import {RiDeleteBin5Fill, RiEditFill  } from 'react-icons/ri';

function GameRow ({ game, onDelete, onEdit }) {
    return (
        <tr>
            <td><i class='icon'><RiDeleteBin5Fill onclick={() => onDelete(game._id)} title="Click to delete" /></i></td>
            <td><i class='icon'><RiEditFill onClick={() => onEdit(game)} title="Editing will allow you to edit an entry" /></i></td>
            <td title="What is the name of the game?">{game.name}</td>
            <td title="What is the price of the game?">{game.price}</td>
            <td title="What is the rating of the game?">{game.rating}</td>
            <td title="When did the game come out?">{game.date.slice(0, 10)}</td>
            <td></td>
        </tr>
    );
}

export default GameRow;
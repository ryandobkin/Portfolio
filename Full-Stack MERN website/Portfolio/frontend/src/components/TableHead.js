import React from "react";
import { Link } from 'react-router-dom';
import { RiFileAddFill  } from 'react-icons/ri'

function TableHead(){
    return (
        <thead>
            <tr>
                <th title="Delete">Delete</th>
                <th title="Edit">Edit</th>
                <th title="Name">Name</th>
                <th title="Price">Price</th>
                <th title="Rating">Rating</th>
                <th title="Date">Date</th>
                <th><Link to="../add-game"><i class="addElement" ><RiFileAddFill title="Add an entry"/></i></Link></th>
            </tr>
        </thead>
    )
}

export default TableHead;
import React from 'react';
import { Link } from 'react-router-dom';
import { RiHome2Fill, RiFileList2Fill, RiListOrdered2  } from 'react-icons/ri'

function Nav() {
    return (
        <nav className="App-nav">
            <Link to="/"><i class='icon'><RiHome2Fill /></i> Home</Link>
            <Link to="../topics"><i class='icon'><RiListOrdered2 /></i> Topics</Link>
            <Link to="../game-list"><i class='icon'><RiFileList2Fill /></i> Game List</Link>
        </nav>
    )
}

export default Nav;

//<Link to="../edit-game"><i><AiFillPicture /></i> Gallery</Link>
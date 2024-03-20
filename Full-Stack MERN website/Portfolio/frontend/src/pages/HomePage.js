import React from 'react';


function HomePage() {
    return(
        <>
            <h2>Home</h2>
            <h3>About me</h3>
                <img class="homeImg" src="./ryan-dobkin-yosemite-half-dome-valley-photo.jpg" alt="Picture of me standing below half dome, Yosemite."/>
                <p class="wrapMe">I'm Ryan. I'm a second year computer science major at Oregon State University, currently living in California. 
                    Although I don't have a ton of experience, graphics programming is one of the cooler things I've tried.
                    One of the things I've been interested in for a long time is game development, but unfortunately in this climate, it doesn't seem like the most stable job position.
                    I plan to take networking next term for my computer science class, allowing me to expand my experience and maybe find a new passion and potential career path.
                    </p>
            <h3>About this app</h3>
                <p>This app is built on the full-stack MERN architecture. It utilizes MongoDB (the M in MERN) for its noSQL database needs.
                    Express.js (the E) is used to handle routing and to act as middleware, parsing and routing requests from React and acting as a layer between
                    the frontend and backend. React.js (the R) is the framework used to develop the UI and manipulate the DOM, using components as a way to improve
                    modularity and reduce bugs. Finally, Node.js (the N) is used to actually run the web server, which then communicated via Express.
                </p>
        </>
    );
}

export default HomePage;
// Controllers for the game Collection

import 'dotenv/config';
import express from 'express';
import * as games from './games-model.mjs';

const PORT = process.env.PORT;
const app = express();
app.use(express.json());  // REST needs JSON MIME type.


// CREATE controller ******************************************
app.post ('/games', (req,res) => { 
    games.createGame(
        req.body.name,
        req.body.price,
        req.body.rating,
        req.body.date
        )
        .then(game => {
            console.log(`"${game.name}" was added to the collection.`);
            res.status(201).json(game);
        })
        .catch(error => {
            console.log(error);
            res.status(400).json({ Error: '400: Error adding game to collection.' });
        });
});


// RETRIEVE controller ****************************************************
app.get('/games', (req, res) => {
    games.retrieveGames()
        .then(games => { 
            if (games !== null) {
                console.log(`All games were retrieved from the collection.`);
                res.json(games);
            } else {
                res.status(404).json({ Error: '404: Error retrieving game from collection.' });
            }         
         })
        .catch(error => {
            console.log(error);
            res.status(400).json({ Error: '400: Bad Request.' });
        });
});


// RETRIEVE by ID controller
app.get('/games/:_id', (req, res) => {
    games.retrieveGameByID(req.params._id)
    .then(game => { 
        if (game !== null) {
            console.log(`"${game.name}" was retrieved, based on its ID.`);
            res.json(game);
        } else {
            res.status(404).json({ Error: '404: Could not retrive game based on ID.' });
        }         
     })
    .catch(error => {
        console.log(error);
        res.status(400).json({ Error: '400: Bad ID.' });
    });

});


// UPDATE controller ************************************
app.put('/games/:_id', (req, res) => {
    games.updateGame(
        req.params._id, 
        req.body.name, 
        req.body.price, 
        req.body.rating,
        req.body.date
    )
    .then(game => {
        console.log(`"${game.name}" was updated.`);
        res.json(game);
    })
    .catch(error => {
        console.log(error);
        res.status(400).json({ Error: '400: Could not update name.' });
    });
});


// DELETE Controller ******************************
app.delete('/games/:_id', (req, res) => {
    games.deleteGameById(req.params._id)
        .then(deletedCount => {
            if (deletedCount === 1) {
                console.log(`Based on its ID, ${deletedCount} game was deleted.`);
                res.status(200).send({ Success: '200: Successfully deleted game.' });
            } else {
                res.status(404).json({ Error: '404: Could not delete game.' });
            }
        })
        .catch(error => {
            console.error(error);
            res.send({ Error: 'Could not delete game based on ID.' });
        });
});


app.listen(PORT, () => {
    console.log(`Server listening on port ${PORT}...`);
});
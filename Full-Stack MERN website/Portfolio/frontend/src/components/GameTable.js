import TableHead from './TableHead';
import GameRow from './GameRow';

// Change the function names and parameters 
// to fit your portfolio topic and schema.

function GameTable({ games, onDelete, onEdit }) {
    return (
        <table id="gameTable">
            <caption>Table of games</caption>
            <TableHead />
            <tbody>
                {games.map((game, i) => 
                    <GameRow
                        game={game} 
                        key={i}
                        onDelete={onDelete}
                        onEdit={onEdit} 
                    />)}
            </tbody>
            <tfoot>
            </tfoot>
        </table>
    );
}

export default GameTable;

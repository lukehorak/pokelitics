function getScore(player) {
    var name = player.name;
    var alive = 6;
    for (var mon in player.team) {
        if (!player.team[mon].alive) {
            alive -= 1;
        }
    }
    return name + ": " + alive;
}

function clearAttributes(player) {
    var playerLite = player;

    delete playerLite.player_number;

    for (mon in playerLite.team) {

        var species = playerLite.team[mon].species;
        playerLite.team[species] = playerLite.team[mon];

        var monSpecies = playerLite.team[mon].species;
        var monName = playerLite.team[mon].name;

        delete playerLite.team[species].species;
        delete playerLite.team[species].used;

        if (monName != monSpecies) {
            delete playerLite.team[mon];
        }

    }
    return playerLite
}

function addToPage(pLite) {
    var wholeDiv = document.createElement("SECTION");
    var headerTag = document.createElement("H3");
    var headerText = document.createTextNode(pLite.name + " Summary:");
    headerTag.appendChild(headerText);
    var summaryTag = document.createElement("PRE");
    summaryTag.setAttribute('data-src', "{{ url_for('static',filename='prism.js') }}");
    summaryTag.className += "language-json";
    var code = document.createElement("CODE");
    code.className += "language-json";
    var summaryText = document.createTextNode(JSON.stringify(pLite.team, null, 4));
    summaryTag.appendChild(code);
    code.appendChild(summaryText);
    wholeDiv.appendChild(headerTag);
    wholeDiv.appendChild(summaryTag);
    //wholeDiv.className += "centerDiv";
    document.body.appendChild(wholeDiv);
    return wholeDiv;
}

window.onload = function() {

    var jstring = document.getElementById("secret").innerHTML;
    var jobj = JSON.parse(jstring);
    // TODO Make table out of JS object with certain attributes as columns
    var head = document.createElement("H1");
    var headText = document.createTextNode("WINNER: " + jobj.battle_winner);
    head.appendChild(headText);
    document.body.appendChild(head);

    var score = document.createElement("H1");
    var scoreText = document.createTextNode("Score -->    " + getScore(jobj.p1) + " - " + getScore(jobj.p2));
    score.appendChild(scoreText);
    document.body.appendChild(score);

    var leftDiv = addToPage(clearAttributes(jobj.p1));
    leftDiv.classList.add("left")
    var rightDiv = addToPage(clearAttributes(jobj.p2));
    rightDiv.classList.add("right")

}

<?php
$servername = "localhost";
$username = "root";
$password = "920kroket";
$dbname = "AirBlitz";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
<html>
<head>
    <title>Highscores Airhockey</title>
    <link rel="stylesheet" href="css/csswebsiteairhockey.css">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="style.css?v=5">
</head>


<body>
<div class="Background">
    <img src="assets/websitebackground.webp" height="100%" width="100%" id="Backgroundback">
</div>


<div class="Title">
    <img src="assets/placeholdersquare.jpg" width="100%" height="100%">
</div>

<div class="Highscores5Mins">
    <img src="assets/highscorebackground.png" width="100%" height="100%">
    <div class="Highscore5Mins tableclass">
        <table class="Tabletextcolor">
        <br><br>Round Duration 5 Minutes<br><br>
        <tr><td>Playername</td><td>&nbsp;&nbsp;Score&nbsp;&nbsp;</td><td>HighscoreDate</td></tr>
            <?php
            $sql = "select * from fivemins order by score desc limit 10;";
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo "<tr>";
                    echo "<td>" . htmlspecialchars($row["playername"]) . "</td>";
                    echo "<td>" . htmlspecialchars($row["score"]) . "</td>";
                    echo "<td>" . htmlspecialchars($row["highscoredate"]) . "</td>";
                    echo "</tr>";
                }
            } else {
                echo "<tr><td colspan='3'>Geen resultaten</td></tr>";
            }
            ?>
        </table>
        <h4><span class="Tableunderline">~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</span></h4>
    </div>
</div>

<div class="Highscores10Mins">
    <img src="assets/highscorebackground.png" width="100%" height="100%">
    <div class="Highscore10Mins tableclass">
        <table class="Tabletextcolor">
            <br><br>Round Duration 10 Minutes<br><br>
            <tr><td>Playername</td><td>&nbsp;&nbsp;Score&nbsp;&nbsp;</td><td>HighscoreDate</td></tr>
            <?php
            $sql = "select * from tenmins order by score desc limit 10;";
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo "<tr>";
                    echo "<td>" . htmlspecialchars($row["playername"]) . "</td>";
                    echo "<td>" . htmlspecialchars($row["score"]) . "</td>";
                    echo "<td>" . htmlspecialchars($row["highscoredate"]) . "</td>";
                    echo "</tr>";
                }
            } else {
                echo "<tr><td colspan='3'>Geen resultaten</td></tr>";
            }
            ?>
        </table>
        <h4><span class="Tableunderline">~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</span></h4>
    </div>
</div>

<div class="Highscores15Mins">
    <img src="assets/highscorebackground.png" width="100%" height="100%">
    <div class="Highscore15Mins tableclass">
        <table class="Tabletextcolor">
            <br><br>Round Duration 15 Minutes<br><br>
            <tr><td>Playername</td><td>&nbsp;&nbsp;Score&nbsp;&nbsp;</td><td>HighscoreDate</td></tr>
            <?php
            $sql = "select * from fifteenmins order by score desc limit 10;";
            $result = $conn->query($sql);
            if ($result->num_rows > 0) {
                while($row = $result->fetch_assoc()) {
                    echo "<tr>";
                    echo "<td>" . htmlspecialchars($row["playername"]) . "</td>";
                    echo "<td>" . htmlspecialchars($row["score"]) . "</td>";
                    echo "<td>" . htmlspecialchars($row["highscoredate"]) . "</td>";
                    echo "</tr>";
                }
            } else {
                echo "<tr><td colspan='3'>Geen resultaten</td></tr>";
            }
            $conn->close();
            ?>
        </table>
        <h4><span class="Tableunderline">~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~</span></h4>
    </div>
</div>

<div class="HighscoreBackground15Mins">
    <img src="assets/placeholdersquare.jpg" width="100%" height="100%"
</div>


<div class="Gamemodes">
<div class="Singleplayer">
    <div class="Singleplayerimage"><img src="assets/singleplayer.webp" width="100%" height="45%"></div>
    <div class="Redgamemodetext">
        <center>
            <h2>Singleplayer</h2>
            <br>Classic Airhockey but
            <br>against AI.
        </center>
    </div>
</div>
<div class="Multiplayer">
    <div class="Multiplayerimage"><img src="assets/singleplayer.webp" width="100%" height="45%"></div>
    <div class="Bluegamemodetext">
        <center>
            <h2>Multiplayer</h2>
            <br>Classic Airhockey.
        </center>
    </div>
</div>
<div class="Double-Ball">
    <div class="Double-Ballimage"><img src="assets/Double-Ball.webp" width="100%" height="45%"></div>
    <div class="Redgamemodetext">
        <center>
            <h2>Double-Ball</h2>
            <br>Classic Airhockey but with double the balls.
        </center>
    </div>
</div>
<div class="Obstacles">
    <div class="Obstaclesimage"><img src="assets/placeholdersquare.jpg" width="100%" height="45%"></div>
    <div class="Bluegamemodetext">
        <center>
            <h2>Obstacles</h2>
            <br>Classic Airhockey but there
            <br>are obstacles.
        </center>
    </div>
</div>
<div class="Two-vs-Two">
    <div class="Two-vs-Twoimage"><img src="assets/Two-vs-Two.webp" width="100%" height="45%"></div>
    <div class="Redgamemodetext">
        <center>
            <h2>Two-vs-Two</h2>
            <br>Airhockey with a teammate by your side.
        </center>
    </div>
</div>
<div class="Free-For-All">
    <div class="Free-For-Allimage"><img src="assets/Free-For-All.webp" width="100%" height="45%"></div>
    <div class="Bluegamemodetext">
        <center>
            <h2>Free-For-All</h2>
            <br>Airhockey but there are
            <br>enemies all around you.
        </center>
    </div>
</div>


<div class="SidebarLeft">
    <img src="assets/redsidebar.webp"
         alt="Moving image" class="SidebarLeftMoving"
</div>
<div class="SidebarLeft2">
    <img src="assets/redsidebar.webp"
         alt="Moving image" class="SidebarLeftMoving2"
</div>


<div class="SidebarRight">
    <img src="assets/bluesidebar.webp"
         alt="Moving image" class="SidebarRightMoving"
</div>
<div class="SidebarRight2">
    <img src="assets/bluesidebar.webp"
         alt="Moving image" class="SidebarRightMoving2"
</div>
</body>

</html>

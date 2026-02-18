<?php
header("Content-Type: application/json");

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(array("error" => "Alleen POST toegestaan"));
    exit;
}

$host = "123test";
$db   = "123test";
$user = "123test";
$pass = "123test";
$charset = "123test";

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
];

try {
    $pdo = new PDO($dsn, $user, $pass, $options);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(array("error" => "Database connectie mislukt: " . $e->getMessage()));
    exit;
}

$playername = isset($_POST['playername']) ? $_POST['playername'] : null;
$score = isset($_POST['score']) ? intval($_POST['score']) : null;
$highscoredate = isset($_POST['highscoredate']) ? $_POST['highscoredate'] : null;
$gamemode = isset($_POST['gamemode']) ? $_POST['gamemode'] : null;

if ($playername === null || $score === null || $highscoredate === null || $gamemode === null) {
    http_response_code(400);
    echo json_encode(array("error" => "Ontbrekende gegevens"));
    exit;
}


try {
    if ($gamemode == 1) {
        $stmt = $pdo->prepare("INSERT INTO OneMins (playername, score, highscoredate) VALUES (?, ?, ?)");
        $stmt->execute([$playername, $score, $highscoredate]);
    }
    else if ($gamemode == 2) {
        $stmt = $pdo->prepare("INSERT INTO TwoMins (playername, score, highscoredate) VALUES (?, ?, ?)");
        $stmt->execute([$playername, $score, $highscoredate]);
    }
    else if ($gamemode == 3) {
        $stmt = $pdo->prepare("INSERT INTO FiveMins (playername, score, highscoredate) VALUES (?, ?, ?)");
        $stmt->execute([$playername, $score, $highscoredate]);
    }

} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(array("error" => "Database insert mislukt: " . $e->getMessage()));
    exit;
}

echo json_encode(array(
    "status" => "success",
    "playername" => $playername,
    "score" => $score,
    "highscoredate" => $highscoredate
));

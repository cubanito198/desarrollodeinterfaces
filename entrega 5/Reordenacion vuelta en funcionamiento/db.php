<?php
// db.php - Configuración de conexión a la base de datos
$host = 'localhost';
$dbname = 'crimsonn';
$username = 'luisss'; // Cambia si usas otro usuario
$password = 'luis'; // Si tienes contraseña en MySQL, agrégala aquí

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname;charset=utf8", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Error de conexión: " . $e->getMessage());
}

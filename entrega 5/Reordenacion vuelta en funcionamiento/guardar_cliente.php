<?php
include 'db.php';
header('Content-Type: application/json'); // Asegura que la respuesta sea JSON
error_reporting(E_ALL);
ini_set('display_errors', 1);

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = json_decode(file_get_contents('php://input'), true);
    
    if (!$data) {
        echo json_encode(["status" => "error", "message" => "Datos no válidos"]);
        exit;
    }

    try {
        $stmt = $pdo->prepare("INSERT INTO clientes (nombre, apellidos, email, direccion, poblacion, cp, pais) VALUES (?, ?, ?, ?, ?, ?, ?)");
        $stmt->execute([
            $data['name'],
            $data['lastname'], // 👈 Asegúrate de que en JavaScript usas 'lastname'
            $data['email'],
            $data['address'],
            $data['population'],
            $data['zip_code'], 
            $data['country']
        ]);
        echo json_encode(["status" => "success", "message" => "Cliente guardado"]);
    } catch (PDOException $e) {
        echo json_encode(["status" => "error", "message" => $e->getMessage()]);
    }
    exit;
}

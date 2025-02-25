<?php
// Configuración de conexión a la base de datos
$host = "localhost";
$username = "luisss";
$password = "luis";
$database = "crimsonn";

// Crear conexión
$conn = new mysqli($host, $username, $password, $database);

// Verificar conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}

// Verificar la acción que se pasa por GET
if (isset($_GET['o']) && $_GET['o'] === 'listatablas') {
    // Obtener la lista de tablas de la base de datos
    $sql = "SHOW TABLES";
    $result = $conn->query($sql);

    // Verificar si se obtuvieron tablas
    if ($result->num_rows > 0) {
        $tablas = [];
        while ($row = $result->fetch_assoc()) {
            $tablas[] = $row;
        }
        echo json_encode($tablas);
    } else {
        echo json_encode([]);
    }
} elseif (isset($_GET['o']) && $_GET['o'] === 'columnastabla' && isset($_GET['tabla'])) {
    // Obtener las columnas de la tabla seleccionada
    $tabla = $_GET['tabla'];
    $sql = "DESCRIBE " . $tabla;
    $result = $conn->query($sql);

    // Verificar si se obtuvieron columnas
    if ($result->num_rows > 0) {
        $columnas = [];
        while ($row = $result->fetch_assoc()) {
            $columnas[] = $row;
        }
        echo json_encode($columnas);
    } else {
        echo json_encode([]);
    }
} else {
    // Si no se reconoce la acción
    echo json_encode(["error" => "Acción no reconocida"]);
}

// Cerrar la conexión
$conn->close();
?>

<style>
   body {
        font-family: Arial, sans-serif;
        background-color: #f4f4f4; /* Color de fondo claro */
        margin: 20px;
        padding: 0;
        color: #333; /* Texto oscuro para buen contraste */
    }

    /* Estilo de la tabla */
    table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
        background-color: #ffffff; /* Fondo blanco */
        border-radius: 12px; /* Bordes redondeados */
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* Sombra suave */
        overflow: hidden; /* Asegura que los bordes redondeados se vean bien */
    }

    /* Estilo de las celdas de la tabla */
    th, td {
        padding: 12px;
        text-align: left;
        border: 1px solid #ddd; /* Borde gris suave */
        color: #555; /* Color de texto más suave */
    }

    /* Estilo para los encabezados de la tabla */
    th {
        background-color: #333; /* Fondo oscuro para el encabezado */
        color: #fff; /* Texto blanco */
        font-weight: bold; /* Negrita para los encabezados */
    }

    /* Estilo de las filas alternas */
    tr:nth-child(even) {
        background-color: #f9f9f9; /* Fondo gris claro para filas alternas */
    }

    /* Hover sobre las filas */
    tr:hover {
        background-color: #eaeaea; /* Fondo ligeramente gris para el hover */
    }

    /* Estilo para el número de fila */
    .row-number {
        font-weight: bold;
        text-align: center;
        color: #777; /* Color gris para el número de fila */
    }

    /* Botón de descarga */
    button {
        background-color: #FFD700; /* Azul elegante */
        color: white;
        padding: 10px 20px;
        font-size: 16px;
        border: none;
        border-radius: 30px; /* Bordes redondeados */
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    button:hover {
        background-color: #f9e79f; /* Color más oscuro al pasar el ratón */
    }

    /* Formulario con borde redondeado */
    form {
        display: inline-block;
        margin-top: 20px;
    }
</style>
<?php
// Database connection details
$host = "localhost";
$username = "luisss";
$password = "luis";
$database = "crimsonn";

// Create connection
$conn = new mysqli($host, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Define the SQL query
$sql = $_GET['sql'];

// Execute the query
$result = $conn->query($sql);

// Function to generate table HTML
function generateTableHTML($result) {
    if ($result && $result->num_rows > 0) {
        $html = "<table border='1'>";
        
        // Fetch and display column headers dynamically
        $html .= "<tr><th>#</th>";
        $columns = $result->fetch_fields();
        foreach ($columns as $column) {
            $html .= "<th>" . htmlspecialchars($column->name) . "</th>";
        }
        $html .= "</tr>";
        
        // Display rows dynamically
        $rowNumber = 1;
        while ($row = $result->fetch_assoc()) {
            $html .= "<tr>";
            $html .= "<td>" . $rowNumber++ . "</td>";
            foreach ($row as $value) {
                $html .= "<td>" . htmlspecialchars($value) . "</td>";
            }
            $html .= "</tr>";
        }
        
        $html .= "</table>";
        return $html;
    } else {
        return "No results found.";
    }
}

// Generate table HTML
$tableHTML = generateTableHTML($result);

// Display table
echo $tableHTML;

// Generate download link
if ($result && $result->num_rows > 0) {
    $encodedTableHTML = base64_encode($tableHTML);
    echo "<form method='post' action='download.php'>";
    echo "<input type='hidden' name='table' value='" . $encodedTableHTML . "'>";
    echo "<button type='submit'>Download as HTML</button>";
    echo "</form>";
}

// Close the connection
$conn->close();
?>


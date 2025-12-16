<?php
require 'apiActions.php';
$api = new apiActions();
$pdo = new PDO('sqlite:../data/Main.db');
header('Content-Type: application/json');

$do_what = $api->fetch_api_action_from_url();

switch ($api->get_request_method()) {
    case 'GET':
        // Read operations
        $result = '';

        if ($do_what['main_action'] == 'allusers') {
            $stmt = $pdo->query('SELECT * FROM USERS');
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        }
        if ($do_what['main_action'] == 'user') {
            $user_id = intval($do_what['parameter']);
            $stmt = $pdo->query("SELECT * FROM USERS WHERE ID=$user_id");
            $result = $stmt->fetchAll(PDO::FETCH_ASSOC);
        }
        $api->print_result($result);
        break;
    case 'POST':
        // Create operations
        break;
    case 'PUT':
        // Update operations
        break;
    case 'DELETE':
        // Delete operations
        break;
    default:
        // Invalid method
        http_response_code(405);
        echo json_encode(['error' => 'Method not allowed']);
        break;
}

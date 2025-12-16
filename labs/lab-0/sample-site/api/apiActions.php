<?php

class apiActions {

    /**
     * Get request method based on $_SERVER variable
     *
     * @return string
     */
    function get_request_method(): string
    {
        return $_SERVER['REQUEST_METHOD'];
    }


    /**
     * Gets main action from url, and if exists the parameter (parameter depth so far is 1)
     *
     * @return array
     */
    function fetch_api_action_from_url(): array
    {
        $result = array();
        $needle = '/api/';
        $request_str = $_SERVER["REQUEST_URI"];
        $parts = explode($needle, $request_str);

        // When just /api is called
        if(count($parts) == 1){
            $result['main_action'] = null;
            $result['parameter'] = null;
        }
        // When request comes with additional parameter
        elseif (str_contains($parts[1], '/')) {
            $details = explode('/', $parts[1]);
            $result['main_action'] = $details[0];
            $result['parameter'] = $details[1];
        }
        // Request with no additional parameter
        else {
            $result['main_action'] = $parts[1];
            $result['parameter'] = null;
        }
        return $result;
    }

    /**
     * Echos the result
     *
     * @param $result
     * @return void
     */
    function print_result($result): void
    {
        if (strlen($result < 1)) {
            $result = 'Error.';
        }
        echo json_encode($result);
    }
}


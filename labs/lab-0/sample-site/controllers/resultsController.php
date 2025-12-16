<?php

namespace Controllers;

class resultsController extends base
{

    private array $data;

    public function __construct()
    {
        $this->data = array();
        $this->getData();
    }

    public function getData()
    {
        $results = print_r($_POST, true);
        $this->data['results'] = $results;
    }

    public function run()
    {
        $this->renderView('results', $this->data);
    }
}

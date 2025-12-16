<?php

namespace Controllers;

class orangePageController extends base
{

    private array $data;

    public function __construct()
    {
        $this->data = array();
    }

    public function run()
    {
        $this->renderView('orange-page', $this->data);
    }
}

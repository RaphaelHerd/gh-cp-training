<?php

namespace Controllers;

class greenPageController extends base
{

    private array $data;

    public function __construct()
    {
        $this->data = array();
    }

    public function run()
    {
        $this->renderView('green-page', $this->data);
    }
}

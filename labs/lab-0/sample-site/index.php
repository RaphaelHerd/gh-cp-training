<?php
require_once __DIR__.'/vendor/autoload.php';

use Controllers\base;
use Symfony\Component\HttpFoundation\Request;

$action = Request::createFromGlobals()->get('action', 'index');

$APP = new base();
$APP->runController( $action );
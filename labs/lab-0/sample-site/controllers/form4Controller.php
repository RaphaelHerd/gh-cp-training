<?php

namespace Controllers;

use Exception;
use Symfony\Component\HttpFoundation\Cookie;
use Symfony\Component\HttpFoundation\Response;

class form4Controller extends base {

	private array $data;

	public function __construct() {
		$this->data = array();
	}

	/**
	 * @throws Exception
	 */
	public function run() {
		$this->renderView( 'form-4', $this->data );
	}
}

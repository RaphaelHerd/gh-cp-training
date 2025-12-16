<?php

namespace Controllers;

class form6Controller extends base {

	private array $data;

	public function __construct() {
		$this->data = array();
	}

	public function convertCelsius() {
		$celsius                  = $_POST['celsius'] ?? 0;
		$fahrenheit               = $celsius * 1.8 + 32;
		$this->data['fahrenheit'] = $fahrenheit;
		$this->data['celsius']    = $celsius;
	}

	public function run() {
		$this->convertCelsius();
		$this->renderView( 'form-6-celsius-fahrenheit', $this->data );
	}
}

<?php
namespace Controllers;

class form3Controller extends base {

	private array $data;

	public function __construct(){
		$this->data = array();
	}

	public function run(){
		$this->renderView( 'form-3' , $this->data );
	}
}

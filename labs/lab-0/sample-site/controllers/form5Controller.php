<?php
namespace Controllers;

class form5Controller extends base {

	private array $data;

	public function __construct(){
		$this->data = array();
	}

	public function run(){
		$this->renderView( 'form-5-media' , $this->data );
	}
}

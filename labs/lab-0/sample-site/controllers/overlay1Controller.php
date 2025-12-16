<?php
namespace Controllers;

class overlay1Controller extends base {

	private array $data;

	public function __construct(){
		$this->data = array();
	}

	public function run(){
		$this->renderView( 'overlay-1' , $this->data );
	}
}

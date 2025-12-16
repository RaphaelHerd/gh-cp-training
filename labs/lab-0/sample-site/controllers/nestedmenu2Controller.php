<?php
namespace Controllers;

class nestedmenu2Controller extends base {

	private array $data;

	public function __construct(){
		$this->data = array();
	}

	public function run(){
		$this->renderView( 'nested-menu-2' , $this->data );
	}
}

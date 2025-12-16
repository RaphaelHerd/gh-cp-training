<?php
namespace Controllers;

class nestedmenu1Controller extends base {

	private array $data;

	public function __construct(){
		$this->data = array();
	}

	public function run(){
		$this->renderView( 'nested-menu-1' , $this->data );
	}
}

<?php
namespace Controllers;

class thankYouController extends base {

	private array $data;

	public function __construct(){
		$this->data = array();
		$this->data['thankyou_message'] = 'Thank you!';
	}

	public function run(){
		$this->renderView( 'thankYou' , $this->data );
	}
}

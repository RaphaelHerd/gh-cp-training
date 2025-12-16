<?php

namespace Controllers;

use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;

class useraccountController extends base {

	private array $data;

	public function __construct() {
		$this->data = array();
	}

	public function credentialsValid() {
		$this->data['isValid']   = false;
		$this->data['userLevel'] = 'none';

		$this->getFormData();

		if ( $this->data['user'] == 'admin' && $this->data['pw'] == 'pw1234' ) {
			$this->data['isValid']   = true;
			$this->data['userLevel'] = 'admin';
		}
		if ( $this->data['user'] == 'joe' && $this->data['pw'] == 'doe' ) {
			$this->data['isValid']   = true;
			$this->data['userLevel'] = 'employee';
		}
	}

	public function getFormData() {
		$this->data['user'] = $_POST['user'];
		$this->data['pw']   = $_POST['pw'];
	}

	/**
	 * @throws SyntaxError
	 * @throws RuntimeError
	 * @throws LoaderError
	 */
	public function run() {
		$this->credentialsValid();
		$this->renderView( 'user-account', $this->data );
	}
}

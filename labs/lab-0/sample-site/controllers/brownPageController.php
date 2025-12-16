<?php

namespace Controllers;

use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;

class brownPageController extends base {

	private array $data;

	public function __construct() {
		$this->data = array();
	}

	/**
	 * @throws SyntaxError
	 * @throws RuntimeError
	 * @throws LoaderError
	 */
	public function run(): void {
		$this->renderView( 'brown-page', $this->data );
	}
}

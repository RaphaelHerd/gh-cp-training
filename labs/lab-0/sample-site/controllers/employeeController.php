<?php

namespace Controllers;

use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;
use Symfony\Component\HttpFoundation\Request;

class employeeController extends base {

	private array $data;
	private string $request;

	public function __construct() {
		$this->data = array();
	}

	public function maybeDisplayEmployeeDetails(): void {
		$this->data['show_search_results'] = '0';

		$find = Request::createFromGlobals()->get( 'find' );

		if ( $find == '1' ) {
			$this->data['show_search_results'] = '1';
		}
	}

	/**
	 * @throws SyntaxError
	 * @throws RuntimeError
	 * @throws LoaderError
	 */
	public function run() {
		$this->maybeDisplayEmployeeDetails();
		$this->renderView( 'admin/find-employee', $this->data );
	}
}

<?php

namespace Controllers;

use Nekman\LuhnAlgorithm\Contract\LuhnAlgorithmExceptionInterface;
use Nekman\LuhnAlgorithm\LuhnAlgorithmFactory;
use Nekman\LuhnAlgorithm\Number;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;

class responseccController extends base {

	private array $data;

	public function __construct() {
		$this->data = array();
	}

	public function getData(): void {
		$results                       = print_r( $_POST, true );
		$this->data['results_print_r'] = $results;
		$this->data['cardnumber']      = trim( $_POST['cardnumber'] );
	}

	public function ccNumberInputCheck(): void {
		if ( ! is_numeric( $this->data['cardnumber'] ) || empty( $this->data['cardnumber'] ) ) {
			$this->data['cc_number_valid'] = false;
		} else {
			$this->data['cc_number_valid'] = true;
		}
	}

	/**
	 * @throws LuhnAlgorithmExceptionInterface
	 */
	public function luhnCheck(): void {
		if ( $this->data['cc_number_valid'] === false ) {
			return;
		}

		$luhn   = LuhnAlgorithmFactory::create();
		$number = Number::fromString( $this->data['cardnumber'] );

		$this->data['luhncheck'] = false;

		if ( $luhn->isValid( $number ) ) {
			$this->data['luhncheck'] = true;
		}
	}

	/**
	 * @throws SyntaxError
	 * @throws RuntimeError
	 * @throws LuhnAlgorithmExceptionInterface
	 * @throws LoaderError
	 */
	public function run(): void {
		$this->getData();
		$this->ccNumberInputCheck();
		$this->luhnCheck();
		$this->renderView( 'response-cc', $this->data );
	}
}

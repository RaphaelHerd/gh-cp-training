<?php
namespace Controllers;

use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;

class childWindowController extends base {

	private array $data;

	public function __construct(){
		$this->data = array();
	}

    /**
     * @throws RuntimeError
     * @throws SyntaxError
     * @throws LoaderError
     */
    public function run(): void
    {
		$this->renderView( 'child-window' , $this->data );
	}
}

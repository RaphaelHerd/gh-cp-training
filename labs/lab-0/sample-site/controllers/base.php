<?php

namespace Controllers;

use Symfony\Component\HttpFoundation\RedirectResponse;
use Twig\Environment;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Error\SyntaxError;
use Twig\Loader\FilesystemLoader;
use Config\setup;

class base {

	public static function runController( $action ): void {
		$controllerClass = 'Controllers\\' . $action . 'Controller';
		$controller      = new $controllerClass;
		$controller->run();
	}

	protected function goto_url( $action_name ): void {
		$url      = 'index.php?action=' . $action_name;
		$response = new RedirectResponse( $url );
		$response->send();
	}

	/**
	 * @throws SyntaxError
	 * @throws RuntimeError
	 * @throws LoaderError
	 */
	protected function renderView( $template, $data ): void {
		$loader = new FilesystemLoader( dirname( __DIR__ ) . '/views' );
		$twig   = new Environment( $loader, [ 'debug' => true ] );
		echo $twig->render( $template . '.twig', $data );

		if ( setup::DEBUG ) {
			$this->renderDebugData();
		}
	}

	protected function renderDebugData(): void {
		echo "<br><br>";
		echo "<hr>";
		echo "<strong>Cookies</strong>";
		echo "<pre>";
		print_r( $_COOKIE );
		echo "</pre>";
	}
}

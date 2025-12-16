<?php
namespace Console;
 
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
 
class CreateControllerCommand extends Command
{
    protected function configure(): void
    {
        $this->setName('create:controller')
             ->setDescription('Creates a new controller class.')
             ->setHelp('Some helpful things ...')
             ->addArgument('controllername', InputArgument::REQUIRED, 'Pass the controller name.');
    }
 
    protected function execute(InputInterface $input,OutputInterface $output): int
    {
        $controllerName         = $input->getArgument('controllername');
        $newControllerPath      = 'controllers/' . $controllerName . 'Controller.php';
        $newControllerClassName = $controllerName . 'Controller';

        $this->copy_index_controller( $newControllerPath );
        $this->adjust_controller_class_name( $newControllerPath, $newControllerClassName );

        $output->writeln(sprintf('%sController has been created.', $input->getArgument('controllername')));
        return Command::SUCCESS;
    }

    private function copy_index_controller( $newControllerPath )
    {
        copy('controllers/indexController.php', $newControllerPath );
    }

    private function adjust_controller_class_name( $newControllerPath, $controllerName )
    {
        $str = file_get_contents( $newControllerPath );
        $str = str_replace('indexController', $controllerName , $str);
        file_put_contents( $newControllerPath, $str );
    }
}
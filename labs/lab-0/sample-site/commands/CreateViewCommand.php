<?php
namespace Console;
 
use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputArgument;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
 
class CreateViewCommand extends Command
{
    protected function configure(): void
    {
        $this->setName('create:view')
             ->setDescription('Creates a new view.')
             ->setHelp('Some helpful things ...')
             ->addArgument('viewname', InputArgument::REQUIRED, 'Pass the view name.');
    }
 
    protected function execute(InputInterface $input,OutputInterface $output): int
    {
        $viewName       = $input->getArgument('viewname');
        $newViewPath    = 'views/' . $viewName . '.twig';

        $this->copy_index_view( $newViewPath );
        $this->adjust_view_info( $newViewPath, $viewName );

        $output->writeln(sprintf('%s view has been created.', $input->getArgument('viewname')));
        return Command::SUCCESS;
    }

    private function copy_index_view(string $newViewPath)
    {
        copy('views/index.twig', $newViewPath );
    }

    private function adjust_view_info( $newViewPath, $viewName )
    {
        $str        = file_get_contents( $newViewPath );
        $viewName   = ucfirst( $viewName );
        $str        = str_replace('This is the Index view.', "This is the {$viewName} view." , $str);
        file_put_contents( $newViewPath, $str );
    }
}
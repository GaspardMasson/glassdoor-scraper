import click
from colorama import Fore, Style

def colored(string,color):
    return color + string+Fore.RESET


def dialogue():
    click.echo(Fore.GREEN + 'Bienvenue dans votre outil de recommandation d\'offres d\'emplois personnalisé !' + Style.RESET_ALL)

    location = click.prompt(colored('Dans quelle ville recherchez-vous un emploi ?','\n'+Fore.BLUE), type=str)
    click.echo('Vous avez choisi la ville de ' + colored(location,Fore.BLUE))
    enterprise_type = click.echo(colored('Quel type d\'entreprise recherchez-vous dans la liste suivante ?','\n'+Fore.BLUE))

    types = ['startup', 'PME', 'ETI', 'Grande entreprise']

    for i, type in enumerate(types):
        click.echo('[' + str(i) + '] ' + type)

    enterprise_type = click.prompt(colored('Votre choix :','\n'+Fore.BLUE), type=int)
    click.echo('Vous avez choisi ' + colored(types[enterprise_type],Fore.BLUE))

    


if __name__ == '__main__':
    dialogue()


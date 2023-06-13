import click
from colorama import Fore, Style
# from recommandation import get_recommendations

def colored(string,color):
    return color + string+Fore.RESET


def dialogue():
    click.echo(Fore.GREEN + 'Bienvenue dans votre outil de recommandation d\'offres d\'emplois personnalisé !' + Style.RESET_ALL)

    # type d'emploi parmi les suivants : ["Data Scientist", "Data Analyst", "Data Engineer", "Business Intelligence Developer"]

    click.echo(colored('Quel type d\'emploi recherchez-vous dans la liste suivante ?','\n'+Fore.BLUE))

    jobs = ["Data Scientist", "Data Analyst", "Data Engineer", "Business Intelligence Developer"]

    for i, job in enumerate(jobs):
        click.echo('[' + str(i) + '] ' + job)

    job_type = click.prompt(colored('Votre choix :','\n'+Fore.BLUE), type=int)
    click.echo('Vous recherchez un poste de ' + colored(jobs[job_type],Fore.CYAN))


    location = click.prompt(colored('Dans quelle ville recherchez-vous un emploi ?','\n'+Fore.BLUE), type=str)
    click.echo('Vous avez choisi la ville de ' + colored(location,Fore.CYAN))
    enterprise_type = click.echo(colored('Quel type d\'entreprise recherchez-vous dans la liste suivante ?','\n'+Fore.BLUE))

    types = ['startup', 'PME', 'ETI', 'Grande entreprise']

    for i, type in enumerate(types):
        click.echo('[' + str(i) + '] ' + type)

    enterprise_type = click.prompt(colored('Votre choix :','\n'+Fore.BLUE), type=int)
    click.echo('Vous avez choisi ' + colored(types[enterprise_type],Fore.CYAN))

    skills = ["java", "business intelligence", "machine learning", "software", "artificial intelligence"]

    click.echo(colored('Quelles compétences recherchez-vous dans la liste suivante ?', '\n'+Fore.BLUE))

    for i, skill in enumerate(skills):
        click.echo('[' + str(i) + '] ' + skill)

    skills_choice_str = click.prompt(colored('Votre choix (séparé par des virgules) :', '\n'+Fore.BLUE), type=str)

    # Diviser la chaîne en une liste de compétences individuelles
    skills_choice = [skill.strip() for skill in skills_choice_str.split(',')]

    # Afficher les compétences choisies
    target_skills = []
    click.echo('Vous avez choisi les compétences suivantes :')
    for skill in skills_choice:
        click.echo(colored(skills[int(skill)], Fore.CYAN)) 
        target_skills.append(skills[int(skill)]) 


    # XXX = get_recommendations(job_type, location, enterprise_type, target_skills)





if __name__ == '__main__':
    dialogue()


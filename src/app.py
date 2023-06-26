import click
from colorama import Fore, Style
from recommandation import get_recommendations
from tabulate import tabulate
import pandas as pd

def colored(string,color):
    return color + string+Fore.RESET

# def display_dataframe(df):
#     pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_colwidth', None)
#     click.echo(df.to_string(index=False))

def display_dataframe(df):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)
    table = df.to_string(index=False)
    table = '\n'.join([line.rstrip() for line in table.split('\n')])
    click.echo(table)


def dialogue():
    click.echo(Fore.GREEN + 'Bienvenue dans votre outil de recommandation d\'offres d\'emplois personnalisé !' + Style.RESET_ALL)

    # type d'emploi parmi les suivants : ["Data Scientist", "Data Analyst", "Data Engineer", "Business Intelligence Developer"]

    click.echo(colored('Quel type d\'emploi recherchez-vous dans la liste suivante ?','\n'+Fore.BLUE))

    jobs = ["Data Scientist", "Data Analyst", "Data Engineer", "Business Intelligence Developer"]

    for i, job in enumerate(jobs):
        click.echo('[' + str(i) + '] ' + job)

    job_type = click.prompt(colored('Votre choix :','\n'+Fore.BLUE), type=int)
    click.echo('Vous recherchez un poste de ' + colored(jobs[job_type],Fore.CYAN))


    ##TODO : demander si la location a une importance (0 si non)
    location = click.prompt(colored('Dans quelle ville recherchez-vous un emploi ? (0 si pas d\'importance)','\n'+Fore.BLUE), type=str)
    if location == str(0):
        click.echo('Vous n\'avez pas d\'importance pour la localisation')
    else:
        click.echo('Vous avez choisi la ville de ' + colored(location,Fore.CYAN))
    
    enterprise_type = click.echo(colored('Quel type d\'entreprise recherchez-vous dans la liste suivante ?','\n'+Fore.BLUE))

    types = ['startup', 'PME', 'ETI', 'Grande entreprise']

    for i, type in enumerate(types):
        click.echo('[' + str(i) + '] ' + type)

    enterprise_type = click.prompt(colored('Votre choix :','\n'+Fore.BLUE), type=int)
    click.echo('Vous avez choisi ' + colored(types[enterprise_type],Fore.CYAN))

    skills = ["python","engineer","design","database","visualization","business","finance","github","azure machine learning", "business intelligence", "machine learning", "software", "artificial intelligence"]

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

    similarity_weight = 0.8
    distance_weight = 0.2

    dataset = get_recommendations(jobs[job_type], location, types[enterprise_type], target_skills, similarity_weight, distance_weight)

    # Afficher les 5 premières recommandations
    click.echo(colored('Voici les 5 premières recommandations :', '\n'+Fore.BLUE))

    click.echo(dataset[["company_offeredRole", "Company_Name", "Company_RoleLocation", "distance_en_km", "weighted_similarity_distance"]].head(5))
    display_dataframe(dataset["requested_url"].head(5))
    
    # display_dataframe(XXX.head(5))

    click.echo("\n")

    # Afficher les poids de similarité et de distance et demander à l'utilisateur s'il souhaite les modifier
    click.echo(colored('Les poids de similarité et de distance sont respectivement de ' + str(similarity_weight) + ' et ' + str(distance_weight) + '.', '\n'+Fore.BLUE))
    click.echo(colored('Souhaitez-vous les modifier ? (Oui/Non)', '\n'+Fore.BLUE))

    change_weights = click.prompt(colored('Votre choix :', '\n'+Fore.BLUE), type=str)

    if change_weights == 'Oui':
        similarity_weight = click.prompt(colored('Poids de similarité :','\n'+Fore.CYAN), type=float)
        distance_weight = click.prompt(colored('Poids de distance :', Fore.CYAN), type=float)
        dataset = get_recommendations(jobs[job_type], location, types[enterprise_type], target_skills, similarity_weight, distance_weight)

        # Afficher les 5 premières recommandations
        click.echo(colored('Voici les nouvelles recommandations :', '\n'+Fore.BLUE))

        click.echo(dataset[["company_offeredRole", "Company_Name", "Company_RoleLocation", "distance_en_km", "weighted_similarity_distance"]].head(5))
        display_dataframe(dataset["requested_url"].head(5))

    click.echo("\n")
    click.echo(Fore.GREEN + 'Merci d\'avoir utilisé notre outil !' + Style.RESET_ALL)


if __name__ == '__main__':
    dialogue()


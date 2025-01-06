########## START ##########
async def start_message(username, user_language):
    if user_language == "fr":
        return f"""🚀 Bienvenue dans Financial Freedom Calculator, {username}.

Ce bot est là pour vous aider à calculer combien d'argent vous devez investir pour être financièrement libre !

Utilisez /calculate pour calculer combien d'argent vous avez besoin !
"""
    elif user_language == "es":
        return f"""🚀 ¡Bienvenido a Financial Freedom Calculator {username}.

Este bot está aquí para ayudarte a calcular cuánto dinero necesitas invertir para ser financieramente libre.

Usa /calculate para calcular cuánto dinero necesitas !
        """
    else:
        # Default message for unsupported languages or English
        return f"""🚀 Welcome to Financial Freedom Calculator {username}.

This bot is here to help you calculate how much money you need to invest to be financially free!

Use /calculate to calculate how much money you need !
"""


########## CALCULATE ##########
async def net_amount(user_language):
    if user_language == "fr":
        return f"""Veuillez entrer le montant net mensuel que vous souhaitez atteindre.
"""
    elif user_language == "es":
        return f"""Por favor, ingresa la cantidad neta mensual que deseas alcanzar.
        """
    else:
        # Default message for unsupported languages or English
        return f"""Please enter the net monthly amount you want to achieve.
"""


async def net_amount_error(user_language):
    if user_language == "fr":
        return f"""Veuillez entrer un montant valide pour le revenu mensuel net.
"""
    elif user_language == "es":
        return f"""Por favor, ingresa una cantidad válida para el monto mensual neto.
        """
    else:
        # Default message for unsupported languages or English
        return f"""Please enter a valid number for the net monthly amount.
"""


async def percentage(user_language):
    if user_language == "fr":
        return f"""Maintenant, veuillez entrer le pourcentage que vous retirerez chaque année :
"""
    elif user_language == "es":
        return f"""Ahora, por favor ingresa el porcentaje que retirarás cada año:
        """
    else:
        # Default message for unsupported languages or English
        return f"""Now, please enter the percentage you will withdraw each year:
"""


async def percentage_error(user_language):
    if user_language == "fr":
        return f"""Veuillez entrer un pourcentage valide.
"""
    elif user_language == "es":
        return f"""Por favor, ingresa un porcentaje válido.
        """
    else:
        # Default message for unsupported languages or English
        return f"""Please enter a valid percentage.
"""


async def result_message(user_language, amount, perc, result, currency):
    if user_language == "fr":
        return f"""Pour obtenir un revenu de {amount}{currency} par mois grâce à vos investissements, il vous faut investir {result} et faire une performance qui vous permet de sortir {perc}% par an.
"""
    elif user_language == "es":
        return f"""Para obtener un ingreso de {amount}{currency} al mes gracias a tus inversiones, necesitas invertir {result} y lograr un rendimiento que te permita retirar {perc}% al año.
        """
    else:
        # Default message for unsupported languages or English
        return f"""To achieve a monthly income of {currency}{amount} from your investments, you need to invest {result} and achieve a performance that allows you to withdraw {perc}% per year.
"""


async def result_message_pea(
    user_language, amount, perc, result, currency, pea_yield, total_invest
):
    if user_language == "fr":
        return f"""Pour obtenir un revenu de {amount}{currency} par mois grâce à vos investissements, il vous faut:

Investir 150 000€ dans un PEA et faire une performance qui vous permet de sortir {perc}%. Ca vous fera {pea_yield}€ par an.

Ensuite, vous investissez le reste, soit {result}, sur un compte titre et faire une performance qui vous permet de sortir {perc}% par an.

Ce qui vous fera un total de {total_invest} à investir.
"""


async def help_message(username, user_language):
    if user_language == "fr":
        return f"""Si vous avez besoin d'aide, contactez-moi @techsherpa !

Pour information:
- Le PEA est taxé à 17.2% après 5 ans.
- Le compte titre est taxé à 30%

Les calculs prennent en compte tout cela !
"""
    elif user_language == "es":
        return f"""Si necesitas ayuda, ¡contáctame @techsherpa!

Para información, el cálculo se realiza con una tributación del 30%.
"""
    else:
        # Default message for unsupported languages or English
        return f"""If you need any help, contact me @techsherpa!

For information, the calculation is done with a 30% taxation.
"""

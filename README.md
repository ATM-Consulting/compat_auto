# PHP Module Updater Script

Ce petit script Python est conçu pour aider les dev à faire la compat des modules.

## Prérequis

- Python >=3.8

## Installation des dépendances

Tu dois installer les librairies nécessaires avec la commande : 

```bash pip install -r requirements.txt ```

## Configuration

Il faut modifier les informations contenues dans config.ini (nom base de données, username..)

## Lancement du script

Pour les noobs qui ne savent toujours pas lancer un script python :) 

```bash python3 script.py ```

## Conseils

- Il vaut mieux s'assurer que le module qu'on passe au script est GITté et qu'il n'y a pas de diff
- Redémarrer le module sur Dolibarr qu'on souhaite MAJ pour que toutes les confs soient contenues en BDD
- Ne jamais faire confiance à 100% au script (ni à Dolibarr d'ailleurs)

## Premières fonctionnalités

- $conf->module->enabled / !empty($conf->module->enabled) => isModEnabled('module') 
- $quelquechose->fk_origin_line => $quelquechose->fk_elementdet ?? $quelquechose->fk_origin_line
- $conf->global->QUELQUECHOSE => getDolGlobalString(QUELQUECHOSE) ou getDolGlobalInt(QUELQUECHOSE) (pas de modification s'il ne trouve pas un type connu en bdd)
- $user->rights->module->droit => $user->hasRight('module', 'quelquechose') / $user->rights->module->droit1->droit2 => $user->hasRight('module', 'droit1', 'droit2')




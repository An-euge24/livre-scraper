# min, hour, day of month, month, day of week, command

# field          allowed values
# -----          --------------
# minute         0-59
# hour           0-23
# day of month   1-31
# month          1-12 (or names, see below)
# day of week    0-6 (0 to 6 are Sunday to Saturday,

# Run a commande every minute
# * * * * * /usr/local/bin/python3 /app/main.py >> /data/result.output 2>&1
* * * * * root /usr/local/bin/python3 /app/main.py >> /data/scraper.log 2>&1

#TZ=Europe/Paris	Définit la timezone pour que cron utilise l'heure de Paris
#* * * * *	Exécute chaque minute (tu peux changer ça)
#/usr/local/bin/python3	Chemin complet vers Python dans le conteneur
#/app/main.py	Ton script Python
#>> /var/log/cron.log	Ajoute les logs au fichier cron.log
#2>&1	Redirige aussi les erreurs vers le fichier log
#(ligne vide)	Obligatoire pour que cron fonctionne
#* * * * *	Chaque minute
#*/5 * * * *	Toutes les 5 minutes
#*/30 * * * *	Toutes les 30 minutes
#0 * * * *	Toutes les heures
#0 */2 * * *	Toutes les 2 heures
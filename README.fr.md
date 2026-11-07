# HomeServer

Un point de départ **privé par défaut** pour héberger Nextcloud sur un serveur
domestique Debian avec Docker Compose. Le [README principal](README.md) contient
le démarrage rapide et les liens vers tous les guides.

## Périmètre

- Nextcloud, PostgreSQL, Redis et cron dans quatre services, images épinglées.
- Données persistantes, base/cache sans ports publiés, web sur loopback uniquement.
- Initialisation des secrets sans écrasement, diagnostic en lecture seule et
  envoi Wake-on-LAN local avec aperçu par défaut.
- Documentation de l'accès privé, des sauvegardes, de la reprise et de l'énergie.

Le projet est un **starter communautaire précoce**, pas un installateur complet.
Il ne partitionne aucun disque, ne configure pas le BIOS/pare-feu/SSH, n'installe
pas Tailscale et n'active pas l'arrêt automatique. Le serveur personnel qui a
inspiré le projet et les données de son propriétaire ne sont pas distribués.

## Démarrage

Sur une installation Linux neuve, avec Python 3.10+, Docker Engine et Compose
Plugin déjà installés :

```sh
git clone https://github.com/Fogbose/HomeServer.git
cd HomeServer
python3 tools/homeserver.py init
# Relire .env avant de continuer.
docker compose config -q
docker compose up -d --wait --wait-timeout 600
docker compose exec -T -u www-data app php occ background:cron
python3 tools/homeserver.py check
```

Employer sudo si nécessaire pour l'accès Docker. Depuis Windows, administrer
Debian par SSH ; ne pas exécuter ces commandes comme si Windows était le serveur.
Un tunnel SSH vers le port 8080 permet le premier accès sans ouvrir le service
sur le LAN. Le compte initial est ncadmin ; son mot de passe est généré dans
`secrets/admin_password`, jamais affiché par l'outil d'initialisation.

Avant tout document unique : mettre en place une copie externe et valider une
restauration isolée. Les tests Python ne prouvent ni une sauvegarde ni le réveil
de votre matériel. Voir la [portée des validations](docs/validation.md).

## Contribuer

Tests : `python3 -m unittest discover -s tests -v`. Les règles sont dans
[CONTRIBUTING.md](CONTRIBUTING.md). Ne transmettre aucun secret ou journal privé
dans une issue ; lire [SECURITY.md](SECURITY.md) pour les vulnérabilités.

Licence [MIT](LICENSE). Les composants externes conservent leurs propres licences.

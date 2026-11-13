# Maintenance simple

Cette fiche est générique. Le starter ne déploie pas les automatismes propres
à une installation personnelle. Noter les dates et adapter les noms de services.

| Quand | Que faire | Automatisable ? |
| --- | --- | --- |
| Chaque jour / après une alerte | Vérifier la réussite et la date de la capture serveur **et** de la copie externe ; contrôler l'espace libre | Oui, captures et alertes ; pas configuré par ce starter |
| Chaque semaine | Regarder Administration → Vue d'ensemble : erreurs, dernier cron, versions ; vérifier les alertes de sauvegarde | Oui pour les alertes ; lecture humaine utile |
| Chaque mois | Préparer les mises à jour OS, images et apps : compatibilité, sauvegarde cohérente, test, fenêtre d'arrêt, vérification après mise à jour | Détection oui ; mises à jour/migrations à superviser |
| Chaque mois si HPB concerné | Redémarrer uniquement HPB hors appel pour renouveler ses identifiants TURN temporaires ; toujours avant leur expiration | Possible avec détection fiable des appels ; pas de redémarrage aveugle |
| Avant expiration TLS | Renouveler le certificat, vérifier clé/certificat et recharger le proxy | Oui ; contrôler le timer et l'expiration réelle |
| Tous les trois mois et après changement important | Restaurer une sauvegarde dans un environnement isolé, vérifier fichiers et base, puis tester avec un compte ordinaire | Procédure automatisable ; validation de récupération à conserver |
| À chaque départ/perte d'appareil | Révoquer sessions et accès VPN, revoir partages et récupération Passwords | Action humaine, assistable |

Ne pas confondre sauvegarde récente et restauration prouvée. Un portable éteint
ne réalise pas sa copie externe. Ne pas lancer `down -v`, purger les archives ou
revenir simplement à une ancienne image après migration de base.

Voir [exploitation](operations.md), [sauvegarde/reprise](backup-restore.md),
[Talk](talk.md) et [modules](modules.md). Les mises à jour restent nécessaires
même si une version d'image est épinglée.

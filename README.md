# Attestation-Covid19

Un script python pour générer les attestations pour le Covid-19. Ce script peut fonctionner sur Android avec Termux (https://play.google.com/store/apps/details?id=com.termux&hl=en). Cela permet de générer l'attestation automatiquement en appuyant sur un widget sur l'écran du Smartphone. Le code QR générée par ce script peut être vérifié avec QR-DNUM (https://play.google.com/store/apps/details?id=fr.gouv.interieur.qr_dnum) qui est une application utilisée par les forces de police pour vérifier la validité des attestations.

Un exemple d'utilisation:
python attestation.py --first-name Bob --last-name Lechobin --birth-date 11/07/1984 --birth-city Paris --address "15 rue de la Melasse" --current-city "Lyon" --current-postcode 69000 --leave-date 01/11/2020 --leave-hour 11:27 --motif achats

Si les paramètres leave-date et leave-hour ne sont pas donnés, le script sélectionne la date et l'heure actuelle.

Le nom du fichier généré est "attestation.pdf".

Le code "python attestation.py" permet d'afficher l'aide pour l'utilisation de ce script.

Version initiale du projet: https://github.com/tdopierre/AttestationNumeriqueCOVID-19

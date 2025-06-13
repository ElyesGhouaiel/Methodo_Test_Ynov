# Activité – Jeu de tests automatisés multi-technos

## Scénario testé

Nous avons choisi de tester une fonction métier simple :  
 **Calcul des points fidélité** selon le montant d’achat et le statut VIP du client.

### Règles :
- 1 point pour chaque tranche de 10€
- Si le client est VIP, les points sont doublés
- Les points sont arrondis à l’entier inférieur

---

## Types de tests utilisés

- **Tests unitaires** dans chaque technologie
- Tests écrits avec :
  - `PHPUnit` en PHP
  - `Jest` en JavaScript

---

## Choix des langages / frameworks

- **PHP + PHPUnit** : langage backend classique, utilisé en entreprise
- **JavaScript + Jest** : langage polyvalent utilisé côté client et serveur, framework de test moderne

---

## Ce que montrent les rapports

- Tous les tests passent avec succès dans les deux langages
- Couverture de plusieurs cas :
  - Clients VIP et non VIP
  - Montants faibles, élevés, et limites
  - Gestion correcte de l’arrondi

---

## Organisation du projet

```plaintext
Activite_seance_1/
├── Js/
│   ├── fidelite.js
│   ├── fidelite.test.js
│   ├── package.json
│   └── package-lock.json
├── Php/
│   ├── src/
│   │   └── fidelite.php
│   └── tests/
│       └── FideliteTest.php
├── vendor/              ← généré par Composer
├── composer.json
├── composer.lock
├── Rapport_Test_Php.png
├── Rapport_Test_Js.png
└── README.md

Rendu préparé par Elyes Ghouaiel – Ynov 2025
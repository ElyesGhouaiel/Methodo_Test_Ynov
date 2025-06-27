# TP – Bibliothèque de gestion d’inscriptions (Séance 3)

## 1. Objectif
Implémenter la génération d’un e-mail de confirmation d’inscription et la tester
rigoureusement via **TDD** puis **Approval Testing**.

## 2. Cycle TDD suivi
| Étape | Action |
|-------|--------|
| Red   | Écriture des tests dans `inscription.test.ts` |
| Green | Code minimal dans `inscription.ts` pour passer les tests |
| Refactor | Nettoyage / factorisation |
| Approval | Ajout du test `emailConfirmation.approval.test.ts` et génération du golden file |

## 3. Commandes
```bash
npm install --ignore-scripts   # installation
npm test                       # 2 suites, 5 tests verts
````

## 4. Exemple de fichier d’approbation

> Extrait de `emailConfirmation.approved.txt`
> (captures écran possibles si voulu)

```
Bonjour Jean Dupont,
…
Statut : Confirmée
```

## 5. Stratégie de tests

* **Unitaires TDD** : couvrent les cas nominaux + validations (e-mail invalide, événement passé).
* **Approval Testing** : garantit la non-régression du format texte complet (dates, accents, sauts de ligne).
* Reporter configuré en mode `nodediff`, ligne‐endings ignorés.

## 6. Limites / pistes

* Pas de gestion de base de données.
* Pas de multi-langue ni de fuseaux horaires multiples.

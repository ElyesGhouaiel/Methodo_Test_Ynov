import { Participant, Evenement, Inscription, EmailConfirmation } from './types';

export class BibliothequeInscription {
  private inscriptions: Inscription[] = [];
  private prochainNumero = 1;

  inscrireParticipant(participant: Participant, evenement: Evenement): Inscription {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(participant.email)) {
      throw new Error('Email invalide');
    }
    if (evenement.date < participant.dateInscription) {
      throw new Error('Impossible de s\'inscrire à un événement passé');
    }
    if (evenement.places !== undefined && evenement.places <= 0) {
      throw new Error('Aucune place disponible');
    }

    const num = `CONF-${String(this.prochainNumero).padStart(8, '0')}`;
    const inscription: Inscription = {
      participant,
      evenement,
      numeroConfirmation: num,
      statut: 'confirmee',
      dateInscription: new Date()
    };
    this.inscriptions.push(inscription);
    this.prochainNumero++;
    return inscription;
  }

  genererEmailConfirmation(i: Inscription): EmailConfirmation {
    const { participant: p, evenement: e, numeroConfirmation: n } = i;
    const sujet = `Confirmation d'inscription - ${e.nom}`;
    const dateEvt = e.date.toLocaleDateString('fr-FR',
      { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });

    const contenu = `Bonjour ${p.prenom} ${p.nom},

Nous avons le plaisir de confirmer votre inscription à l'événement suivant :

=== DÉTAILS DE L'ÉVÉNEMENT ===
Nom : ${e.nom}
Date : ${dateEvt}
Lieu : ${e.lieu}
Prix : ${e.prix}€
Description : ${e.description}

=== VOS INFORMATIONS ===
Nom : ${p.nom}
Prénom : ${p.prenom}
Email : ${p.email}
Téléphone : ${p.telephone ?? 'N/A'}
Date d'inscription : ${p.dateInscription.toLocaleDateString('fr-FR')}

=== CONFIRMATION ===
Numéro de confirmation : ${n}
Statut : Confirmée

Merci de conserver ce numéro de confirmation pour vos dossiers.

Cordialement,
L'équipe d'organisation`;

    return { destinataire: p.email, sujet, contenu, numeroConfirmation: n };
  }
}

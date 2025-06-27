import approvals = require('approvals');
import { BibliothequeInscription } from './inscription';
import { Participant, Evenement } from './types';

describe('Email de confirmation – approval-testing', () => {
  it('génère un contenu email approuvé', async () => {
    const biblio = new BibliothequeInscription();

    const participant: Participant = {
      nom: 'Dupont',
      prenom: 'Jean',
      email: 'jean.dupont@email.com',
      telephone: '0123456789',
      dateInscription: new Date('2024-01-15')
    };

    const evenement: Evenement = {
      id: 'EVT001',
      nom: 'Conférence Tech 2024',
      date: new Date('2024-03-15'),
      lieu: 'Paris Convention Center',
      prix: 150,
      description: 'Une conférence sur les dernières technologies',
      places: 100
    };

    const ins = biblio.inscrireParticipant(participant, evenement);
    const email = biblio.genererEmailConfirmation(ins);

    await approvals.verify(__dirname, 'emailConfirmation', email.contenu);
  });
});

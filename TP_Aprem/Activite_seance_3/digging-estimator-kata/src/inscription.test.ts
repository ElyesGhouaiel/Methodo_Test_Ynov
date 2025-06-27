import { BibliothequeInscription } from './inscription';
import { Participant, Evenement } from './types';

describe('BibliothequeInscription - TDD', () => {
  let bibliotheque: BibliothequeInscription;
  let participantTest: Participant;
  let evenementTest: Evenement;

  beforeEach(() => {
    bibliotheque = new BibliothequeInscription();

    participantTest = {
      nom: 'Dupont',
      prenom: 'Jean',
      email: 'jean.dupont@email.com',
      telephone: '0123456789',
      dateInscription: new Date('2024-01-15')
    };

    evenementTest = {
      id: 'EVT001',
      nom: 'Conférence Tech 2024',
      date: new Date('2024-03-15'),
      lieu: 'Paris Convention Center',
      prix: 150,
      description: 'Une conférence sur les dernières technologies',
      places: 100
    };
  });

  // TEST 1 : inscription de base
  it('inscrit un participant', () => {
    const ins = bibliotheque.inscrireParticipant(participantTest, evenementTest);

    expect(ins.participant.email).toBe('jean.dupont@email.com');
    expect(ins.evenement.nom).toBe('Conférence Tech 2024');
    expect(ins.numeroConfirmation).toMatch(/^CONF-\d{8}$/);
    expect(ins.statut).toBe('confirmee');
  });

  // TEST 2 : génération de l’e-mail
  it('génère un email de confirmation', () => {
    const ins = bibliotheque.inscrireParticipant(participantTest, evenementTest);
    const email = bibliotheque.genererEmailConfirmation(ins);

    expect(email.destinataire).toBe('jean.dupont@email.com');
    expect(email.contenu).toContain('Jean Dupont');
    expect(email.contenu).toContain('Conférence Tech 2024');
    expect(email.contenu).toContain('150');
    expect(email.numeroConfirmation).toBe(ins.numeroConfirmation);
  });

  // TEST 3 : validations
  it('rejette un email invalide', () => {
    participantTest.email = 'invalide';
    expect(() =>
      bibliotheque.inscrireParticipant(participantTest, evenementTest)
    ).toThrow('Email invalide');
  });

  it('rejette un événement passé', () => {
    evenementTest.date = new Date('2020-01-01');
    expect(() =>
      bibliotheque.inscrireParticipant(participantTest, evenementTest)
    ).toThrow('Impossible de s\'inscrire à un événement passé');
  });
});

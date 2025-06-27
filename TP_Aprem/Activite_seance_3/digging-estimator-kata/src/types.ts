export interface Participant {
    nom: string; prenom: string; email: string;
    telephone?: string; dateInscription: Date;
  }
  export interface Evenement {
    id: string; nom: string; date: Date; lieu: string;
    prix: number; description: string; places?: number;
  }
  export interface Inscription {
    participant: Participant; evenement: Evenement;
    numeroConfirmation: string; dateInscription: Date;
    statut: 'confirmee' | 'en_attente' | 'annulee';
  }
  export interface EmailConfirmation {
    destinataire: string; sujet: string; contenu: string; numeroConfirmation: string;
  }
  
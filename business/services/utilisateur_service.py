from business.dao.utilisateur_dao import UtilisateurDao
from business.client.compte_utilisateur import CompteUtilisateur

from getpass import getpass
from argon2 import PasswordHasher

ph = PasswordHasher()
import random
import string
import re


class Utilisateur(UtilisateurDao):
    def create_account(self, nom, mail, mdp, mdp_verif):
        """
        Création d'un compte et ajout d'un utilisateur à la base de données

        Parameters:
        -----------

        Returns :
        ----------

        """
        name_user = nom
        utilisateurdao = UtilisateurDao()

        while True:
            # mail = Utilisateur.get_user_info(self, info="mail")
            if not utilisateurdao.check_email_valide(mail=mail):
                print("Adresse e-mail invalide. Veuillez réessayer.")
                continue

            if not utilisateurdao.check_email_unique(mail=mail):
                print("Adresse e-mail déjà existante. Veuillez en choisir une autre.")
                continue
            else:
                print("Adresse mail valide")
                break

        while True:
            # passw = UtilisateurDao.get_user_info(self, info="mdp")
            if not utilisateurdao.check_mdp_valide(mdp=mdp):
                print(
                    "Le mot de passe ne remplit pas les conditions. Veuillez réessayer."
                )
                continue
            else:
                print("Le mot de passe est conforme")
                break

        sel = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(16)
        )

        mot_de_passe_concatene = sel + mdp

        password = ph.hash(mot_de_passe_concatene)

        while True:
            password_to_check = UtilisateurDao.get_user_info(self, info="mdp_to_check")
            if not utilisateurdao.check_mdp_egal(
                mdp=password, mdp_to_check=sel + password_to_check
            ):
                print("Le mot de passe est invalide. Veuillez réessayer.")
                continue
            else:
                print("Le mot de passe est valide.")
                break

        UtilisateurDao().add_db(name_user, mail, password, sel)

    def se_connecter(
        self,
        mail,
        passw
    ):
        """Permet à un utilisateur de se connecter en saisissant son adresse e-mail et son mot de passe.

        Returns:
            CompteUtilisateur: Un objet CompteUtilisateur contenant les informations de l'utilisateur
                              connecté si la connexion réussit. None sinon.
        """
        max_attempts = 3  # Nombre maximum de tentatives
        attempts = 0  # Compteur de tentatives

        while attempts < max_attempts:
            try:
                # Demander à l'utilisateur de saisir son identifiant et son mot de passe
                mail = mail

                utilisateur = UtilisateurDao().verif_connexion(mail=mail,passw=passw)

                # Vérifier si l'utilisateur a été trouvé dans la base de données
                if utilisateur:
                    name = UtilisateurDao.get_value_from_mail(
                        self, mail=mail, value="nom"
                    )
                    print(f"Connexion réussie ! Bienvenue {name}")
                    CompteUtilisateur._connexion = True

                    CompteUtilisateur.id = UtilisateurDao.get_value_from_mail(
                        self, mail=mail, value="id_compte_utilisateur"
                    )

                    CompteUtilisateur.nom = UtilisateurDao.get_value_from_mail(
                        self, mail=mail, value="nom"
                    )
                    CompteUtilisateur.age = UtilisateurDao.get_value_from_mail(
                        self, mail=mail, value="age"
                    )
                    CompteUtilisateur.code_postal = UtilisateurDao.get_value_from_mail(
                        self, mail=mail, value="code_postal"
                    )
                    CompteUtilisateur.tel = UtilisateurDao.get_value_from_mail(
                        self, mail=mail, value="tel"
                    )
                    CompteUtilisateur.ville = UtilisateurDao.get_value_from_mail(
                        self, mail=mail, value="ville"
                    )
                    CompteUtilisateur.mail=mail
                    
                    return CompteUtilisateur
                else:
                    print(
                        "Identifiant ou mot de passe incorrect. Vous avez encore",
                        max_attempts - attempts - 1,
                        "tentatives.",
                    )
                    attempts += 1

            except Exception as e:
                print("Erreur lors de la connexion à la base de données :", e)
        print("Trop de tentatives infructueuses. La connexion est bloquée.")
        return None


# Appeler la fonction se_connecter
if __name__ == "__main__":
    u1 = Utilisateur()
    u3 = u1.create_account(
        nom="tom",
        mail="tom.t@gmail.com",
        mdp="Tom0001",
        mdp_verif="Tom0001",
    )
    # CompteUtilisateurService().deconnexion(u3)

    # CompteUtilisateurService().modifierInfo(u3, mail="pascal@gmail")
    UtilisateurDao().afficher_db()

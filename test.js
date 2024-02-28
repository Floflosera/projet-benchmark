document.addEventListener("DOMContentLoaded", function() {
    let treeContainer = document.getElementById('tree-container');
    let ipList = document.getElementById('ip-list');
    let encadrer = document.getElementById('encadrer');
    let nlpSelectContainer = null;
    let visionSelectContainer = null;

    function executerListIP() {
        fetch('listIp.py')
            .then(response => response.text())
            .then(data => {
                // Après l'exécution de listIP.py, affiche l'arbre dans le conteneur treeContainer
                fetch('tree.txt')
                    .then(response => response.text())
                    .then(data => {
                        const arbre = parserArbre(data);
                        afficherArbre(treeContainer, arbre); // Utilisation de treeContainer comme conteneur
                    })
                    .catch(error => console.error('Erreur lors du chargement de l\'arbre:', error));
            })
            .catch(error => console.error('Erreur lors de l\'exécution de listIP.py:', error));
    }

    function parserArbre(data) {
        const lignes = data.split('\n');
        const arbre = {};
        lignes.forEach(ligne => {
            const parties = ligne.split('/');
            let noeudCourant = arbre;
            parties.forEach(partie => {
                if (!noeudCourant[partie]) {
                    noeudCourant[partie] = {};
                }
                noeudCourant = noeudCourant[partie];
            });
        });
        return arbre;
    }

    function afficherArbre(container, arbre) {
        const ul = document.createElement('ul');
        container.appendChild(ul);
        Object.keys(arbre).forEach(key => {
            const li = document.createElement('li');
            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            li.appendChild(checkbox);
            li.appendChild(document.createTextNode(key));
            ul.appendChild(li);
            if (Object.keys(arbre[key]).length > 0) {
                afficherArbre(li, arbre[key]);
            } else {
                checkbox.addEventListener('change', function() {
                    const estCoche = checkbox.checked;
                    const ip = key;

                    if (estCoche) {
                        const ipAffichage = document.createElement('p');
                        ipAffichage.textContent = ip;
                        ipList.appendChild(ipAffichage);

                        const elementSelectionne = document.createElement('div');
                        elementSelectionne.textContent = key;
                        elementSelectionne.classList.add('selected-element');
                        encadrer.appendChild(elementSelectionne);

                        const conteneurSaisie = document.createElement('div');
                        conteneurSaisie.classList.add('input-container');

                        const nomUtilisateurSaisie = document.createElement('input');
                        nomUtilisateurSaisie.type = 'text';
                        nomUtilisateurSaisie.placeholder = 'Nom d\'utilisateur';
                        nomUtilisateurSaisie.id = 'nom-utilisateur-input'; // Ajout d'un identifiant unique
                        nomUtilisateurSaisie.classList.add('ip-input');
                        nomUtilisateurSaisie.classList.add('gagaga')
                        conteneurSaisie.appendChild(nomUtilisateurSaisie);

                        const motDePasseSaisie = document.createElement('input');
                        motDePasseSaisie.type = 'text';
                        motDePasseSaisie.placeholder = 'Mot de passe';
                        motDePasseSaisie.id = 'mot-de-passe-input'; // Ajout d'un identifiant unique
                        motDePasseSaisie.classList.add('ip-input');
                        conteneurSaisie.appendChild(motDePasseSaisie);

                        encadrer.appendChild(conteneurSaisie);
                    } else {
                        const ipAffichages = ipList.querySelectorAll('p');
                        ipAffichages.forEach(function(ipAffichage) {
                            if (ipAffichage.textContent === ip) {
                                ipList.removeChild(ipAffichage);
                                const elementSelectionne = encadrer.querySelector('.selected-element');
                                if (elementSelectionne) {
                                    encadrer.removeChild(elementSelectionne);
                                }
                                const conteneurSaisie = encadrer.querySelector('.input-container');
                                if (conteneurSaisie) {
                                    encadrer.removeChild(conteneurSaisie);
                                }
                            }
                        });
                    }
                    verifierSelectionNLP();
                    verifierSelectionVision();
                });
            }
        });
    }

    function verifierSelectionNLP() {
        const caseNLP = document.getElementById('nlp-checkbox');
        const estCoche = caseNLP.checked;

        if (estCoche) {
            ajouterSelectionNLP();
        } else {
            supprimerSelectionNLP();
        }
    }

    function ajouterSelectionNLP() {
        if (!nlpSelectContainer) {
            nlpSelectContainer = document.createElement('div');
            nlpSelectContainer.id = 'nlp-select-container';

            const conteneurSelect = document.createElement('div');
            conteneurSelect.classList.add('select-container');

            const libelleSelect = document.createElement('label');
            libelleSelect.textContent = 'NLP';
            conteneurSelect.appendChild(libelleSelect);

            const select = document.createElement('select');
            const option1 = document.createElement('option');
            option1.value = 'option1';
            option1.text = 'Option NLP 1';
            select.appendChild(option1);
            // Ajouter plus d'options ici

            conteneurSelect.appendChild(select);
            nlpSelectContainer.appendChild(conteneurSelect);

            document.querySelector('.menu_choix').appendChild(nlpSelectContainer);
        }
    }

    function supprimerSelectionNLP() {
        if (nlpSelectContainer) {
            nlpSelectContainer.remove();
            nlpSelectContainer = null;
        }
    }

    function verifierSelectionVision() {
        const caseVision = document.getElementById('vision-checkbox');
        const estCoche = caseVision.checked;

        if (estCoche) {
            ajouterSelectionVision();
        } else {
            supprimerSelectionVision();
        }
    }

    function ajouterSelectionVision() {
        if (!visionSelectContainer) {
            visionSelectContainer = document.createElement('div');
            visionSelectContainer.id = 'vision-select-container';

            const conteneurSelect = document.createElement('div');
            conteneurSelect.classList.add('select-container');

            const libelleSelect = document.createElement('label');
            libelleSelect.textContent = 'Vision';
            conteneurSelect.appendChild(libelleSelect);

            const select = document.createElement('select');
            const option1 = document.createElement('option');
            option1.value = 'option1';
            option1.text = 'Option Vision 1';
            select.appendChild(option1);
            // Ajouter plus d'options ici

            conteneurSelect.appendChild(select);
            visionSelectContainer.appendChild(conteneurSelect);

            document.querySelector('.menu_choix').appendChild(visionSelectContainer);
        }
    }

    function supprimerSelectionVision() {
        if (visionSelectContainer) {
            visionSelectContainer.remove();
            visionSelectContainer = null;
        }
    }

    function cocherCases(checked) {
        document.getElementById('nlp-checkbox').checked = checked;
        document.getElementById('vision-checkbox').checked = checked;
    }

    function sauvegarderEtatCase() {
        localStorage.setItem('nlpCheckboxState', document.getElementById('nlp-checkbox').checked.toString());
        localStorage.setItem('visionCheckboxState', document.getElementById('vision-checkbox').checked.toString());
    }

    function restaurerEtatCase() {
        document.getElementById('nlp-checkbox').checked = false;
        document.getElementById('vision-checkbox').checked = false;

        const etatCaseNLP = localStorage.getItem('nlpCheckboxState');
        const etatCaseVision = localStorage.getItem('visionCheckboxState');

        if (etatCaseNLP === 'true') {
            document.getElementById('nlp-checkbox').checked = true;
            verifierSelectionNLP();
        }

        if (etatCaseVision === 'true') {
            document.getElementById('vision-checkbox').checked = true;
            verifierSelectionVision();
        }
    }

    document.getElementById('analyse-btn').addEventListener('click', function() {
        encadrer.innerHTML = '';
        cocherCases(false);
        sauvegarderEtatCase();

        // Commence par exécuter listIp.py
        executerListIP();
    });

    document.getElementById('nlp-checkbox').addEventListener('change', function() {
        verifierSelectionNLP();
        sauvegarderEtatCase();
    });

    document.getElementById('vision-checkbox').addEventListener('change', function() {
        verifierSelectionVision();
        sauvegarderEtatCase();
    });

    restaurerEtatCase();

    document.getElementById('result-btn').addEventListener('click', function() {
        afficherDonnees();

        fetch('/run_graphe', {
            method: 'POST',
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erreur lors de la récupération du graphique');
                }
                return response.blob(); // Récupérer les données binaires de la réponse
            })
            .then(blob => {
                // Créer une URL à partir des données binaires
                const url = URL.createObjectURL(blob);
                // Créer une balise d'image pour afficher le graphique
                const img = document.createElement('img');
                img.src = url;
                // Supprimer l'image précédente s'il y en a une
                const previousImg = document.querySelector('#graph-img');
                if (previousImg) {
                    previousImg.remove();
                }
                // Ajouter un identifiant à l'image pour la référencer facilement
                img.id = 'graph-img';
                // Ajouter l'image à la page
                document.body.appendChild(img);
            })
            .catch(error => console.error('Erreur lors de l\'exécution du script graphe.py:', error));
    });

    document.getElementById('Valider').addEventListener('click', function() {
        const ipAffichages = document.querySelectorAll('.encadrer .selected-element');
        const elementsNomUtilisateur = document.querySelectorAll('#nom-utilisateur-input');
        const elementsMotDePasse = document.querySelectorAll('#mot-de-passe-input');

        // Sélectionner la div avec la classe "select-container"
        const selectContainer = document.querySelector('.select-container');
        // Récupérer le label à l'intérieur de la div
        const label = selectContainer.querySelector('label');

        // Initialiser un tableau pour stocker les promesses
        const promises = [];

        for (let i = 0; i < ipAffichages.length; i++) {
            const donnees = {
                ip: ipAffichages[i].textContent,
                nomUtilisateur: elementsNomUtilisateur[i].value,
                motDePasse: elementsMotDePasse[i].value,
                ia:label.textContent
            };

            console.log(donnees);

            // Ajouter la promesse à notre tableau de promesses
            const promise = fetch('/valider', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(donnees)
            })
                .then(response => {
                    if (response.ok) {
                        console.log('Données envoyées avec succès.');
                    } else {
                        console.error('Erreur lors de l\'envoi des données au serveur.');
                    }
                });

            promises.push(promise);
        }

        // Attendre que toutes les promesses se terminent
        Promise.all(promises).then(() => {
            // Une fois que toutes les requêtes sont terminées, exécuter la requête pour /run_connectSHH
            var xhr = new XMLHttpRequest();
            //console.log('lancement SSH.');
            xhr.open("POST", "/run_connectSSH", true);
            //console.log('lancement SSH.');
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    // Traitement de la réponse du serveur, si nécessaire
                    console.log(xhr.responseText);
                    //console.log('lancement SSH.');
                }
                else{
                    //console.log('perdu');
                }
            };
            xhr.send();
        });
    });

    function afficherDonnees() {
        const divAnalyse = document.querySelector('.analyse');

        // Supprimer le tableau existant s'il y en a un
        const tableauExistant = divAnalyse.querySelector('.data-table');
        if (tableauExistant) {
            divAnalyse.removeChild(tableauExistant);
        }

        fetch('donnees.txt')
            .then(response => response.text())
            .then(data => {
                const tableauDonnees = data.split('\n');

                const table = document.createElement('table');
                table.classList.add('data-table');

                const ligneEnTete = document.createElement('tr');
                const enTetes = tableauDonnees[0].split('\t');
                enTetes.forEach(enTeteTexte => {
                    const enTete = document.createElement('th');
                    enTete.textContent = enTeteTexte.trim();
                    ligneEnTete.appendChild(enTete);
                });
                table.appendChild(ligneEnTete);

                for (let i = 1; i < tableauDonnees.length; i++) {
                    const donneesLigne = tableauDonnees[i].split('\t');
                    const ligne = document.createElement('tr');
                    donneesLigne.forEach(donneeCellule => {
                        const cellule = document.createElement('td');
                        cellule.textContent = donneeCellule.trim();
                        ligne.appendChild(cellule);
                    });
                    table.appendChild(ligne);
                }

                divAnalyse.appendChild(table);
            })
            .catch(error => console.error('Erreur lors du chargement des données:', error));
    }
});
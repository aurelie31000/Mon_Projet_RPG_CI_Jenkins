// Jenkinsfile

// L'ensemble du pipeline est encapsulé dans un bloc 'pipeline'.
// C'est la structure déclarative standard.
pipeline {
    // Définit l'agent sur lequel le pipeline s'exécutera.
    // 'any' signifie que Jenkins peut utiliser n'importe quel agent disponible.
    agent any

    // Section pour les variables d'environnement.
    // Ici, on récupère le Personal Access Token (PAT) GitHub que vous avez configuré dans Jenkins.
    // L'ID 'github-pat' DOIT correspondre à l'ID que vous avez donné à votre Secret text credential dans Jenkins.
    environment {
        GITHUB_TOKEN = credentials('github-pat') // Utilise l'ID 'github-pat' que vous avez défini.
    }

    // La section 'stages' contient les différentes phases de votre pipeline CI/CD.
    stages {
        // Étape 1 : Récupération du code source
        stage('Checkout Code') {
            steps {
                echo 'Checking out code from dev branch...'
                // Récupère le code de la branche 'dev' depuis votre dépôt GitHub.
                // L'URL doit correspondre exactement à votre dépôt.
                // Pour un dépôt public, aucun identifiant n'est nécessaire ici pour le clonage.
                git branch: 'dev', url: 'https://github.com/aurelie31000/Mon_Projet_RPG_CI_Jenkins.git'
            }
        }

        // Étape 2 : Installation des dépendances Python
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies (pytest)...'
                // Crée un environnement virtuel Python pour isoler les dépendances du projet.
                // Utilise 'bat' pour les commandes Windows.
                // 'python -m venv venv' créera le dossier 'venv' contenant l'environnement.
                bat 'python -m venv venv'
                // Installe 'pytest' directement dans l'environnement virtuel en utilisant le pip de l'environnement.
                bat 'venv\\Scripts\\pip install pytest'
            }
        }

        // Étape 3 : Exécution des tests Python
        stage('Run Tests') {
            steps {
                echo 'Running Python tests...'
                // Exécute pytest à partir de l'environnement virtuel sur le dossier 'tests/'.
                // Utilise le python de l'environnement virtuel.
                bat 'venv\\Scripts\\python -m pytest tests\\'
            }
        }

        // Étape 4 : Fusion vers la branche 'main' (en cas de succès des tests)
        stage('Merge to Main (Fast-Forward)') {
            // La directive 'when' garantit que cette étape ne s'exécute que si toutes les étapes précédentes
            // (notamment les tests) ont réussi. 'currentBuild.result == null' signifie "en cours" (donc pas encore d'échec),
            // et 'currentBuild.result == 'SUCCESS'' signifie que le build a réussi jusqu'à présent.
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Tests passed. Merging dev into main (fast-forward)...'
                script {
                    // Configure l'utilisateur Git pour que les commits effectués par Jenkins soient identifiables.
                    // Utilise 'bat' pour les commandes Windows.
                    bat 'git config user.email "jenkins@example.com"'
                    bat 'git config user.name "Jenkins CI Bot"'

                    // Récupère la dernière version de 'main' pour s'assurer qu'elle est à jour localement.
                    bat 'git checkout main'
                    bat 'git pull origin main'

                    // Tente une fusion 'fast-forward' de 'dev' dans 'main'.
                    // L'option '--ff-only' empêche une fusion "non fast-forward" qui créerait un commit de fusion.
                    // Cela garantit un historique linéaire si possible.
                    bat 'git merge --ff-only dev'

                    // Pousse les changements de 'main' vers le dépôt distant sur GitHub.
                    // L'authentification utilise le PAT (GITHUB_TOKEN) via l'URL HTTPS avec oauth2.
                    bat "git push https://oauth2:${GITHUB_TOKEN}@github.com/aurelie31000/Mon_Projet_RPG_CI_Jenkins.git main"
                    echo 'Main branch updated successfully!'
                }
            }
        }
    }

    // La section 'post' définit les actions à effectuer après que tous les stages sont terminés,
    // en fonction du résultat global du pipeline.
    post {
        // Toujours exécuté, que le pipeline réussisse ou échoue.
        always {
            echo 'Pipeline finished.'
        }
        // Exécuté si le pipeline s'est terminé avec succès.
        success {
            echo 'Build successful.'
        }
        // Exécuté si le pipeline a échoué (par exemple, si les tests ont échoué).
        failure {
            echo 'Build failed! Handling the failed commit...'
            script {
                // Assurez-vous que Python est bien installé sur la machine où tourne votre agent Jenkins, et que la commande python est accessible via le PATH système.

                // Génère un identifiant unique pour la branche d'échec (horodatage + numéro de build Jenkins).
                // Utilise 'powershell' pour obtenir l'horodatage sur Windows.
                def uniqueId = powershell(returnStdout: true, script: 'Get-Date -Format माननेMMddHHmmss').trim()
                def failureBranchName = "failures/${env.BUILD_NUMBER}-${uniqueId}" // Exemple: failures/15-20250622173000

                // Récupère le SHA (identifiant unique) du commit qui a été testé et qui a causé l'échec.
                // Il est crucial de le faire AVANT de réinitialiser la branche 'dev'.
                bat 'git checkout dev' // Assurez-vous d'être sur la branche 'dev' pour obtenir le bon HEAD
                def failedCommitSha = bat(returnStdout: true, script: 'git rev-parse HEAD').trim()

                // Réinitialise la branche 'dev' au commit précédent. Cela "retire" le commit en échec de 'dev'.
                bat 'git reset --hard HEAD^'

                // Pousse de force la branche 'dev' réinitialisée vers GitHub.
                // Le '--force' est nécessaire car l'historique de 'dev' a été réécrit localement.
                bat 'git push https://oauth2:${GITHUB_TOKEN}@github.com/aurelie31000/Mon_Projet_RPG_CI_Jenkins.git dev --force'

                // Crée une nouvelle branche sous 'failures/' à partir du commit qui a échoué,
                // et la pousse vers GitHub. Cela permet de conserver l'historique du commit défectueux
                // sans qu'il ne bloque la branche 'dev'.
                bat "git push https://oauth2:${GITHUB_TOKEN}@github.com/aurelie31000/Mon_Projet_RPG_CI_Jenkins.git ${failedCommitSha}:${failureBranchName}"

                echo "Failure branch ${failureBranchName} created from failed commit ${failedCommitSha}. Dev branch reset and forced pushed."
            }
        }
    }
}

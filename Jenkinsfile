import java.text.SimpleDateFormat
import java.util.Date

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
                git branch: 'dev', url: 'https://github.com/aurelie31000/Mon_Projet_RPG_CI_Jenkins.git'
            }
        }

        // Étape 2 : Installation des dépendances Python
        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies (pytest)...'
                // Crée un environnement virtuel Python pour isoler les dépendances du projet.
                sh 'python3 -m venv venv'
                // Installe 'pytest' directement dans l'environnement virtuel en utilisant le pip de l'environnement.
                sh 'venv/bin/pip install pytest'
            }
        }

        // Étape 3 : Exécution des tests Python
        stage('Run Tests') {
            steps {
                echo 'Running Python tests...'
                // Exécute pytest à partir de l'environnement virtuel sur le dossier 'tests/'.
                sh 'venv/bin/python -m pytest tests/'
            }
        }

        // Étape 4 : Fusion vers la branche 'principal' (en cas de succès des tests)
        stage('Merge to Principal (Fast-Forward)') {
            // La directive 'when' garantit que cette étape ne s'exécute que si toutes les étapes précédentes
            // (notamment les tests) ont réussi.
            when {
                expression { currentBuild.result == null || currentBuild.result == 'SUCCESS' }
            }
            steps {
                echo 'Tests passed. Merging dev into principal (fast-forward)...'
                script {
                    // Configure l'utilisateur Git pour que les commits effectués par Jenkins soient identifiables.
                    sh 'git config user.email "jenkins@example.com"'
                    sh 'git config user.name "Jenkins CI Bot"'
                    // Affiche toutes les branches (locales et distantes) pour le débogage
                    echo 'Listing all branches in the repository:'
                    sh 'git branch -a'
                    // Récupère la dernière version de 'principal' pour s'assurer qu'elle est à jour localement.
                    sh 'git checkout -B principal origin/principal'
                    // Pull en plus pour être sûr
                    sh 'git pull origin principal'
                    // Tente une fusion 'fast-forward' de 'dev' dans 'principal'.
                    sh 'git merge --ff-only dev'
                    // Pousse les changements de 'principal' vers le dépôt distant sur GitHub.
                    sh "git push https://oauth2:${GITHUB_TOKEN}@github.com/aurelie31000/Mon_Projet_RPG_CI_Jenkins.git principal"
                    echo 'Principal branch updated successfully!'
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
                // Génère un identifiant unique pour la branche d'échec (horodatage + numéro de build Jenkins).
                def now = new Date(currentBuild.timestamp)
                def sdf = new SimpleDateFormat("yyyyMMddHHmmss")
                def uniqueId = sdf.format(now)
                def failureBranchName = "failures/${env.BUILD_NUMBER}-${uniqueId}"
                // Récupère le SHA (identifiant unique) du commit qui a été testé et qui a causé l'échec.
                sh 'git checkout dev'
                def failedCommitSha = sh(returnStdout: true, script: 'git rev-parse HEAD').trim()
                // Réinitialise la branche 'dev' au commit précédent.
                sh 'git reset --hard HEAD^'
                // Pousse de force la branche 'dev' réinitialisée vers GitHub.
                sh "git push https://oauth2:${GITHUB_TOKEN}@github.com/aurelie31000/Mon_Projet_RPG_CI_Jenkins.git dev --force"
                // Crée une nouvelle branche sous 'failures/' à partir du commit qui a échoué.
                sh "git push https://oauth2:${GITHUB_TOKEN}@github.com/aurelie31000/Mon_Projet_RPG_CI_Jenkins.git ${failedCommitSha}:${failureBranchName}"
                echo "Failure branch ${failureBranchName} created from failed commit ${failedCommitSha}. Dev branch reset and forced pushed."
            }
        }
    }
}

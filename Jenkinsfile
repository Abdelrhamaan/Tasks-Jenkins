pipeline {
    agent any

    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'main', description: 'Branch to checkout')
        booleanParam(name: 'MIGRATIONS', defaultValue: false, description: 'Run migrations')
        booleanParam(name: 'COLLECTSTATIC', defaultValue: false, description: 'Run collectstatic')
        string(name: 'MODULE_NAME', defaultValue: '', description: 'Module name for migrations')
        string(name: 'SCRIPT_NAME', defaultValue: '', description: 'Script to run')
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the branch specified by the parameter
                git branch: params.BRANCH_NAME, url: 'https://github.com/Abdelrhamaan/Employee-Jenkins.git'
            }
        }
        stage('Migrations') {
            when {
                expression { params.MIGRATIONS }
            }
            steps {
                script {
                    if (params.MODULE_NAME?.trim()) {
                        sh "python manage.py makemigrations ${params.MODULE_NAME}"
                    } else {
                        sh "python manage.py makemigrations"
                    }
                    sh "python manage.py migrate"
                }
            }
        }
        stage('Collect Static Files') {
            when {
                expression { params.COLLECTSTATIC }
            }
            steps {
                sh "python manage.py collectstatic --noinput"
            }
        }
        stage('Run Custom Script') {
            when {
                expression { params.SCRIPT_NAME?.trim() }
            }
            steps {
                sh "chmod +x ${params.SCRIPT_NAME}"
                sh "./${params.SCRIPT_NAME}"
            }
        }
        stage('Docker Compose Up') {
            steps {
                // Bring up the containers (you may use -d if you want detached mode)
                sh "docker-compose up"
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}

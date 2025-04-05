pipeline {
    agent any

    environment {
        PROJECT_DIR = '/home/ec2-user/Employee-Jenkins'
    }

    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'main')
        booleanParam(name: 'MIGRATIONS', defaultValue: false)
        booleanParam(name: 'COLLECTSTATIC', defaultValue: false)
        string(name: 'MODULE_NAME', defaultValue: '')
        string(name: 'SCRIPT_NAME', defaultValue: '')
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: params.BRANCH_NAME, 
                    url: 'https://github.com/Abdelrhamaan/Employee-Jenkins.git'
            }
        }

        stage('Database Operations') {
            when {
                expression { params.MIGRATIONS }
            }
            steps {
                dir("${env.PROJECT_DIR}") {
                    sh """
                    docker exec employee_management python manage.py makemigrations ${params.MODULE_NAME}
                    docker exec employee_management python manage.py migrate
                    """
                }
            }
        }

        stage('Collect Static') {
            when {
                expression { params.COLLECTSTATIC }
            }
            steps {
                dir("${env.PROJECT_DIR}") {
                    sh 'docker exec employee_management python manage.py collectstatic --noinput'
                }
            }
        }

        stage('Custom Script') {
            when {
                expression { params.SCRIPT_NAME?.trim() }
            }
            steps {
                dir("${env.PROJECT_DIR}") {
                    sh """
                    docker exec employee_management chmod +x ${params.SCRIPT_NAME}
                    docker exec employee_management ./${params.SCRIPT_NAME}
                    """
                }
            }
        }

        stage('Restart Services') {
            steps {
                dir("${env.PROJECT_DIR}") {
                    sh 'docker-compose restart employee_management employee_db'
                }
            }
        }
    }

    post {
        always {
            dir("${env.PROJECT_DIR}") {
                sh '''
                docker logs employee_management > employee_management.log || true
                docker logs employee_db > employee_db.log || true
                '''
                archiveArtifacts artifacts: '*.log', allowEmptyArchive: true
            }
        }
    }
}

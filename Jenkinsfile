pipeline {
    agent any

    parameters {
        string(name: 'BRANCH_NAME', defaultValue: 'main')
        booleanParam(name: 'MIGRATIONS', defaultValue: false)
        booleanParam(name: 'COLLECTSTATIC', defaultValue: false)
        string(name: 'MODULE_NAME', defaultValue: '')
        string(name: 'SCRIPT_NAME', defaultValue: '')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                deleteDir()
            }
        }
        
        stage('Checkout Code') {
            steps {
                git branch: params.BRANCH_NAME, 
                     url: 'https://github.com/Abdelrhamaan/Employee-Jenkins.git'
            }
        }
        
        stage('Rebuild Containers') {
            steps {
                sh '''
                docker-compose -f /home/ec2-user/Employee-Jenkins/docker-compose.yml down -v
                docker-compose -f /home/ec2-user/Employee-Jenkins/docker-compose.yml build --no-cache
                docker-compose -f /home/ec2-user/Employee-Jenkins/docker-compose.yml up -d
                '''
            }
        }
        
        stage('Database Operations') {
            when {
                expression { params.MIGRATIONS }
            }
            steps {
                script {
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
                sh 'docker exec employee_management python manage.py collectstatic --noinput'
            }
        }
        
        stage('Custom Script') {
            when {
                expression { params.SCRIPT_NAME?.trim() }
            }
            steps {
                sh """
                docker exec employee_management chmod +x ${params.SCRIPT_NAME}
                docker exec employee_management ./${params.SCRIPT_NAME}
                """
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: '**/docker-compose.log', allowEmptyArchive: true
        }
    }
}
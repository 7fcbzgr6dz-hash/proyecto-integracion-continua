
pipeline {
    agent any

    stages {

        stage('Preparar entorno') {
            steps {
                echo 'Preparando entorno de integración continua...'
                sh 'python3 --version'
                sh 'python3 -m venv venv'
            }
        }

        stage('Instalar dependencias') {
            steps {
                sh './venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Ejecutar pruebas') {
            steps {
                sh './venv/bin/python -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'Integración continua exitosa. Todas las pruebas pasaron.'
        }

        failure {
            echo 'La integración continua falló. Revisar los errores.'
        }
    }
}

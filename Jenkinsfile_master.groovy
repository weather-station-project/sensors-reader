@Library('shared-library') _
import com.davidleonm.WeatherStationSensorsReaderVariables

pipeline {
  agent { label 'slave' }

  stages {
    stage('Prepare Python ENV') {
      steps {
        script {
          setBuildStatus('pending', "${WeatherStationSensorsReaderVariables.RepositoryName}")

          // Clean & Prepare new python environment
          sh '''
             rm -rf ENV
             python3 -m venv ENV

             ENV/bin/pip install --upgrade pip
             ENV/bin/pip install --upgrade wheel
             ENV/bin/pip install --upgrade setuptools

             ENV/bin/pip install psycopg2
             '''
        }
      }
    }

    stage('Execute unit tests') {
      steps {
        script {
          sh "ENV/bin/python -m unittest discover -s ${WORKSPACE}/WeatherStationSensorsReader"
        }
      }
    }

    stage('SonarQube analysis') {
      environment {
        def scannerHome = tool 'Sonarqube'
      }

      steps {
        script {
          sh "ENV/bin/coverage run -m unittest discover -s ${WORKSPACE}/WeatherStationSensorsReader"
          sh "ENV/bin/coverage xml -i"
        }

        withSonarQubeEnv('Sonarqube') {
          sh "${scannerHome}/bin/sonar-scanner"
        }

        timeout(time: 10, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Build & Deploy image') {
      steps {
        script {
          def dockerImage = null

          try {
            version = sh(script: 'cat VERSION', returnStdout: true)
            dockerImage = docker.build("${WeatherStationSensorsReaderVariables.DockerHubRegistryName}", "--file ./Dockerfile ${WORKSPACE}")

            docker.withRegistry('', 'docker-hub-login') {
              dockerImage.push("${version}")
              dockerImage.push('latest')
            }
          } finally {
            if (dockerImage != null) {
              sh """
                 docker rmi -f ${WeatherStationSensorsReaderVariables.DockerHubRegistryName}:${version}
                 docker rmi -f ${WeatherStationSensorsReaderVariables.DockerHubRegistryName}:latest
                 """
            }
          }
        }
      }
    }
  }
  post {
    success {
      script {
        setBuildStatus('success', "${WeatherStationSensorsReaderVariables.RepositoryName}")
      }
    }

    failure {
      script {
        setBuildStatus('failure', "${WeatherStationSensorsReaderVariables.RepositoryName}")
      }
    }
  }
}
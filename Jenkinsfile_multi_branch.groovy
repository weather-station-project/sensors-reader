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

             ENV/bin/pip install --no-cache-dir --upgrade pip
             ENV/bin/pip install --no-cache-dir --upgrade wheel
             ENV/bin/pip install --no-cache-dir --upgrade setuptools

             ENV/bin/pip install --no-cache-dir psycopg2 gpiozero coverage
             '''
        }
      }
    }

    stage('Execute unit tests and code coverage') {
      steps {
        script {
          sh """
             ENV/bin/python -m unittest discover -s ${WORKSPACE}/WeatherStationSensorsReader
             ENV/bin/coverage run -m unittest discover -s ${WORKSPACE}/WeatherStationSensorsReader
             """
        }
      }
    }

    stage('SonarQube analysis') {
      environment {
        def scannerHome = tool 'Sonarqube'
      }

      steps {
        script {
          sh "ENV/bin/coverage xml"
        }

        withSonarQubeEnv('Sonarqube') {
          sh "${scannerHome}/bin/sonar-scanner"
        }

        timeout(time: 10, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }

    stage('Deploy on staging') {
      steps {
        script {
          deployContainerOnRepository("${WeatherStationSensorsReaderVariables.DockerHubStagingRegistryName}")
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

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

             ENV/bin/pip install --no-cache-dir psycopg2 gpiozero coveralls
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

    stage('Upload report to Coveralls.io') {
      steps {
        withCredentials([string(credentialsId: 'coveralls-sensors-reader-repo-token', variable: 'COVERALLS_REPO_TOKEN')]) {
          sh 'ENV/bin/coveralls'
        }
      }
    }

    stage('Build & Deploy image') {
      steps {
        script {
          deployContainerOnRepository("${WeatherStationSensorsReaderVariables.DockerHubRegistryName}")
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

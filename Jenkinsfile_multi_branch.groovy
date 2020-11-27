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

    stage('Deploy on staging') {
      steps {
        script {
          deployWeatherStationSensorsReaderOnStaging()
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

pipeline {
  agent {
    docker {
      image 'python:3'
    }

  }
  stages {
    stage('build') {
      steps {
        pybat(script: 'aa.sh', returnStatus: true, returnStdout: true)
        publishCoverage(calculateDiffForChangeRequests: true, failNoReports: true, failUnhealthy: true, failUnstable: true)
      }
    }
    stage('Test') {
      steps {
        slackSend()
      }
    }
    stage('Deploy') {
      steps {
        sleep 3
      }
    }
  }
}
node {
   stage('Downloading changes') { // for display purposes
      //git "https://github.com/vassik/third-party-tool.git"
      checkout scm
   }
   stage('Downloading a tool and building') {
      sh "rm -rf third-party-tool"
      sh "git clone https://github.com/vassik/third-party-tool.git"
   }
   stage('Testing') {
      sh "./testframework/test.py"
   }
   stage('Publishing HTML Report') {
      publishHTML (target: [
          allowMissing: false,
          alwaysLinkToLastBuild: false,
          keepAll: true,
          reportDir: 'htmlreports',
          reportFiles: 'index.html',
          reportName: "Test Execution Report"
        ])      
   }
}

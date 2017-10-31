node {
   stage('Downloading changes') { // for display purposes
      //git "https://github.com/vassik/third-party-tool.git"
      checkout scm
   }
   stage('Downloading a tool and building') {
      sh "rm -rf xwiki-platform"
      sh "git clone https://github.com/vassik/xwiki-platform.git"
      
      //this should be commented once in master...
      //sh "cd third-party-tool/ && git branch --track config-testing_env_folder origin/config-testing_env_folder && git checkout config-testing_env_folder && cd .."
   }
   stage('Testing') {
      sh "./testframework/test.py"
   }
   stage('Publishing HTML Report') {
      publishHTML (target: [
          allowMissing: false,
          alwaysLinkToLastBuild: false,
          keepAll: true,
          reportDir: 'report/htmlreports',
          reportFiles: 'index.html',
          reportName: "Test Execution Report"
        ])      
   }
}

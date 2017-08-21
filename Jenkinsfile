node {
   stage('Downloading changes') { // for display purposes
      //git "https://github.com/vassik/third-party-tool.git"
      checkout scm
   }
   stage('Downloading the tool to test') {
      sh "rm -rf third-party-tool"
      sh "git clone https://github.com/vassik/third-party-tool.git"
      sh "ls -la"
   }
   stage('Building Compilers') {
      // Run the maven build
      //sh "mvn -Dmaven.test.failure.ignore clean install"
   }
   stage('Building Xtext plugins') {
      //sh("cd language/ && mvn -Dmaven.test.failure.ignore -pl !thingml.ui.tests clean install && cd ..")
   }
   stage('Building TestJar') {
      //sh("cd testJar/ && mvn -Dmaven.test.failure.ignore clean install && cd ..")
   }
   stage('Testing') {
      //sh "./testframework/test.py"
   }
   stage('Publishing HTML Report') {
//      publishHTML (target: [
//          allowMissing: false,
//          alwaysLinkToLastBuild: false,
//          keepAll: true,
//          reportDir: 'htmlreports',
//          reportFiles: 'index.html',
//          reportName: "Test Execution Report"
//        ])      
   }
}

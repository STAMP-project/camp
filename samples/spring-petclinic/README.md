
## Use CAMP with Spring-petclinic application

We provide a sample docker-based project called `Spring-petclinic` which is a popular spring-based web application https://github.com/spring-projects/spring-petclinic that supports different types of DB (HSQLDB, Postgres, MySQL) and Jetty as web sever.

**NB:** Before generating configurations, please edit the `camp.yml` file by giving the host machine ip (use `ifconfig` and provide the `en0` ip).
```
pattern: "IP_ADDRESS"
replacements: [ "XXX.XXX.XXX.XXX" ] #provide your host machine IP
```
Generate configurations to support different DB (PetClinic app + MySQL and PetClinic app + Postgres).
```
docker run -t -v $PWD:/campworkingdir -v /var/run/docker.sock:/var/run/docker.sock -t fchauvel/camp:latest camp generate -d /campworkingdir
docker run -t -v $PWD:/campworkingdir -v /var/run/docker.sock:/var/run/docker.sock -t fchauvel/camp:latest camp realize -d /campworkingdir
```
Select one of the two generated applications to run, available in `out/`.
```
cd out/config_1/ #or cd out/config_2/
docker-compose up -d #do not run in a detached mode if you would like to check logs
```
Two containers will be created, one for the web app, and one for the database.
To verify that the application is well started, please browse: http://localhost:8080.
## Run stress tests
Open a new terminal tab and install Jmeter on your host machine.
```
apt install jmeter
```
Run stress tests.
```
#In ~/spring-petclinic/tests
jmeter -n -t petclinic_test_plan.jmx -l out/jtllog.csv -j out/jmeterrun.log
```

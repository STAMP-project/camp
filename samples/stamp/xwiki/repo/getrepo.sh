mkdir git
cd git
git clone https://github.com/xwiki-contrib/docker-xwiki
cp docker-xwiki/9 ../
cd ..
mv mysql-tomcat xwiki9mysql
mv postgres-tomcat xwiki9postgres

cd
git clone https://github.com/docker-library/tomcat
cd tomcat
bash ./update.sh
cp 7/jre8/
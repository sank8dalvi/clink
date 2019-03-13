import mysql.connector
from mysql.connector import errorcode

''''
CREATE TABLE `clink`.`tagdata` ( `uid` INT NOT NULL AUTO_INCREMENT , `passID` VARCHAR(255) NOT NULL , `bagID` VARCHAR(255) NOT NULL , `bagWT` INT NOT NULL , PRIMARY KEY (`uid`)) ENGINE = InnoDB;

CREATE TABLE `clink`.`collected` ( `uid` INT NOT NULL AUTO_INCREMENT , `passID` VARCHAR(255) NOT NULL , `bagID` VARCHAR(255) NOT NULL , `bagWT` INT(11) NOT NULL , PRIMARY KEY (`uid`)) ENGINE = InnoDB;
'''


def clinkConnect(db):
    try:
        return mysql.connector.connect(**db)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)


def clinkClose(con):
    con.close()

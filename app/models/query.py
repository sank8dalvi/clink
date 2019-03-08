class Query:
	addbags = "INSERT INTO `tagdata` (`passID`, `bagID`, `bagWT`) VALUES (%s,%s,%s)"
	matchtag = "SELECT * FROM `tagdata` WHERE `passID` = %s AND `bagID` = %s LIMIT 1"
	gettable = "SELECT * FROM `tagdata` LIMIT 10"

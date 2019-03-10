class Query:
	addpassbags = "INSERT INTO `tagdata` (`passID`, `bagID`, `bagWT`) VALUES (`%s`,`%s`,`%s`)"
	matchtag = "SELECT * FROM `tagdata` WHERE `passID` = `%s` AND `bagID` = `%s` LIMIT 1"
	delTag = "DELETE FROM `tagdata` WHERE `%s` = 34545 AND `bagID` = `%s`"
	gettable = "SELECT * FROM `tagdata`"
	UpColl = "INSERT INTO `collected`(`uid`, `passID`, `bagID`, `bagWT`) VALUES (`%s`,`%s`,`%s`)"
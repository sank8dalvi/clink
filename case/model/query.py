class Query:
	addpassbags = "INSERT INTO `tagdata` (`passID`, `bagID`, `bagWT`) VALUES ({},{},{})"
	matchtag = "SELECT * FROM `tagdata` WHERE `passID` = {} AND `bagID` = {} LIMIT 1"
	delTag = "DELETE FROM `tagdata` WHERE {} = 34545 AND `bagID` = {}"
	gettable = "SELECT * FROM `tagdata`"
	UpColl = "INSERT INTO `collected`(`uid`, `passID`, `bagID`, `bagWT`) VALUES ({},{},{})"
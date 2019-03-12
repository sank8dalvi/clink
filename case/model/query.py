class Query:
	addpassbags = "INSERT INTO `tagdata` (`passID`, `bagID`, `bagWT`) VALUES ({},{},{})"
	matchtag = "SELECT * FROM `tagdata` WHERE `passID` = {} AND `bagID` = {} LIMIT 1"
	delTag = "DELETE FROM `tagdata` WHERE `passID` = {} AND `bagID` = {}"
	gettable = "SELECT `passID`,`bagID`,`bagWT` FROM `tagdata`"
	UpColl = "INSERT INTO `collected`(`uid`, `passID`, `bagID`, `bagWT`) VALUES ({},{},{})"
	getbags = "SELECT * FROM `tagdata` WHERE `passID` = {}"
	getPassCount = "SELECT COUNT(DISTINCT `passID`) FROM `tagdata`"
	getBagCount = "SELECT COUNT(`bagID`) FROM `tagdata`"
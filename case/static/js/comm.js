function communicate(method, url, data){
	$.ajax({
	url: url,
	  type: "POST",
	  headers: {
	    "accept": "application/json",
	    "content-type": "application/x-www-form-urlencoded"
	  },
	  data: data
	});
}
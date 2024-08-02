main_arr=[];
function getTeamPerformance() {
	var arr=[]
	for (var i = document.getElementsByClassName("graph-label").length - 1; i >= 0; i--) {
		var a =[document.getElementsByClassName("graph-label")[i].innerText,document.getElementsByClassName("graph-value")[i].innerText];
		label = a[0];
		count = a[1];
		obj={};
		obj[label] = count;
		arr.push(obj);
	}
	for (var i = document.getElementsByClassName("information-label").length - 1; i >= 0; i--) {
		var a = [document.getElementsByClassName("information-label")[i].innerText, document.getElementsByClassName("information-count")[i].innerText]
		label = a[0];
		count = a[1];
		obj={};
		obj[label] = count;
		arr.push(obj);
	}
	obj = {"teamName":document.getElementsByClassName("content-title")[0].innerText};
	arr.push(obj);
	obj={"Season":document.getElementsByClassName("title")[5].innerText};
	arr.push(obj);
	return arr;
}
for (var i = document.getElementsByClassName("list-item").length - 1; i >= 0; i--) {
	document.getElementsByClassName("list-item")[i].click();document.getElementsByClassName("list-item")[i].click();
	var a = getTeamPerformance();
	main_arr.push(a);
}
return main_arr;
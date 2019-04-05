$(document).ready(function() {
	$("#btn-news").on("click", function () {
		console.log("Alldskljd");
	});

	$(".fa-search").on("click", function () {
		// console.log($("#mysearch").css("width"));
		if ( $("#mysearch").css("width") == "200px" ) {
			// console.log("yes");
			$("#mysearch").focus().css("width", "500px");
		}
	});
});
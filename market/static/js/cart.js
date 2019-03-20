alert("debut");
$(document).ready(function() {
	function set_qte(ctrl_tag, qte_tag, total_tag){
		window.new_qte = parseInt($(qte_tag).text());
		// console.log(new_qte);

		if ($(ctrl_tag).text() === "+") {
			window.new_qte++;
		}else if ($(ctrl_tag).text() === "-"){
			if (window.new_qte > 1) {
				window.new_qte--;
			}
		}

		$(qte_tag).text(window.new_qte); //Affichage de la window.new_qte
		
		$.ajax({
			url : "{% url 'price' id=5 %}",
			type : 'GET',
			dataType : 'text',
			success : function(rep, statut){
				console.log(rep);
				total = window.new_qte * parseInt(rep);
				$(total_tag).text(total);

			},
			error : function(resultat, statut, erreur){
				console.log(erreur);
				alert("erreur AJAX");
			},
		});				
	}

	function init(total_tag, id) {
		window.current = total_tag
		$.ajax({
			url : "{% url 'total' id=" + id + " %}",
			type : 'GET',
			dataType : 'text',

			success : function(rep, statut){
				console.log(rep);
				window.current.innerText = rep;
			},
			error : function(resultat, statut, erreur){
				console.log(erreur);
			},
		});
	}

	$(".quantite").on("click", function () {
		init(this.firstElementChild, this.value);
	});

	$(".ctrl-quantite").on("click", function () {
		set_qte(this.firstElementChild,
				this.parentElement.children[1].firstElementChild,
				this.parentElement.parentElement.children[5]);
	});

});
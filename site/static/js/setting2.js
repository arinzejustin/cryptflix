function googleTranslateElementInit() {
  new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}

$(document).ready(function(){
	wow = new WOW(
      {
        animateClass: 'animated',
        offset:       100,
        callback:     function(box) {
          console.log("WOW: animating <" + box.tagName.toLowerCase() + ">")
        }
      }
    );
    wow.init();
    
	var percent =  document.getElementById("Ultra") ? parseFloat(document.getElementById("Ultra").value) : 0; 
	
	//Calculator
	function calc(){
		var money = parseFloat($("#money").val());
		switch (percent) {
		    case 0:
		        if( (money >= 25 && money < 501)){
		        	var profitDaily = money / 100 * 105;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 500 && money < 1001) {
		        	var profitDaily = money / 100 * 107;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 1000 && money < 5001) {
		        	var profitDaily = money / 100 * 110;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 5000 && money < 10001) {
		        	var profitDaily = money / 100 * 120;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 10000 && money < 250001) {
		        	var profitDaily = money / 100 * 125;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 25000 && money < 500001) {
		        	var profitDaily = money / 100 * 130;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        }  if (money >= 50000 && money < 1000001) {
		        	var profitDaily = money / 100 * 135;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money < 25){
					$("#profitDaily").text("Error!");
				}
		        break;
			case 1:
		       if( (money >= 25 && money < 501)){
		        	var profitDaily = money / 100 * 117;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 500 && money < 1001) {
		        	var profitDaily = money / 100 * 125;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 1000 && money < 5001) {
		        	var profitDaily = money / 100 * 140;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 5000 && money < 10001) {
		        	var profitDaily = money / 100 * 170;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 10000 && money < 250001) {
		        	var profitDaily = money / 100 * 190;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 25000 && money < 500001) {
		        	var profitDaily = money / 100 * 220;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        }  if (money >= 50000 && money < 1000001) {
		        	var profitDaily = money / 100 * 250;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money < 25){
					$("#profitDaily").text("Error!");
				}
		        break;
		    case 2:
		    	if( (money >= 25 && money < 501)){
		        	var profitDaily = money / 100 * 140;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 500 && money < 1001) {
		        	var profitDaily = money / 100 * 160;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 1000 && money < 5001) {
		        	var profitDaily = money / 100 * 220;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 5000 && money < 10001) {
		        	var profitDaily = money / 100 * 250;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 10000 && money < 250001) {
		        	var profitDaily = money / 100 * 330;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 25000 && money < 500001) {
		        	var profitDaily = money / 100 * 360;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        }  if (money >= 50000 && money < 1000001) {
		        	var profitDaily = money / 100 * 450;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money < 25){
					$("#profitDaily").text("Error!");
				}
		        break;
		    case 3:
		    	if( (money >= 25 && money < 501)){
		        	var profitDaily = money / 100 * 300;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 500 && money < 1001) {
		        	var profitDaily = money / 100 * 350;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 1000 && money < 5001) {
		        	var profitDaily = money / 100 * 450;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 5000 && money < 10001) {
		        	var profitDaily = money / 100 * 550;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 10000 && money < 250001) {
		        	var profitDaily = money / 100 * 700;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 25000 && money < 500001) {
		        	var profitDaily = money / 100 * 750;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        }  if (money >= 50000 && money < 1000001) {
		        	var profitDaily = money / 100 * 900;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money < 25){
					$("#profitDaily").text("Error!");
				}
		        break;
		    case 4:
		    	if( (money >= 25 && money < 501)){
		        	var profitDaily = money / 100 * 450;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 500 && money < 1001) {
		        	var profitDaily = money / 100 * 500;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 1000 && money < 5001) {
		        	var profitDaily = money / 100 * 700;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 5000 && money < 10001) {
		        	var profitDaily = money / 100 * 800;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 10000 && money < 250001) {
		        	var profitDaily = money / 100 * 1000;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money >= 25000 && money < 500001) {
		        	var profitDaily = money / 100 * 1200;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        }  if (money >= 50000 && money < 1000001) {
		        	var profitDaily = money / 100 * 1400;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money < 25){
					$("#profitDaily").text("Error!");
				}
		        break;
		    case 5:
		    	if( (money >= 5000  && money < 25001)){
		        	var profitDaily = money / 100 *  1200;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money < 5000){
					$("#profitDaily").text("Error!");
				}
		        break;
		    case 6:
		    	if( (money >= 500  && money < 25001)){
		        	var profitDaily = money / 100 *  2500;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money < 500){
					$("#profitDaily").text("Error!");
				}
		        break;
		    case 7:
		    	if( (money >= 100 && money < 25000 )){
		        	var profitDaily = money / 100 *  5000;
					var profitDaily = profitDaily.toFixed(2);

					$("#profitDaily").text(profitDaily);
		        } if (money < 100){
					$("#profitDaily").text("Error!");
				}
		        break;
		}
	}
	if($("#money").length){
		calc();
	}
	$("#money").keyup(function(){
		calc();
	});

	$("#Ultra").on('change', function() {
		percent = parseFloat(this.value);
		calc();
	})
});


/// New Code Starts from Here
jQuery(document).ready(function(){
	
	jQuery("#amttospd").keyup(function(){
		calcNew();
	});
	
	// When Top TAB is clicked, the Deposit TEXT box gets "25$" default value
	jQuery("ul.nav.nav-tabs li a").click(function(){
		 
		var t = jQuery(this).attr("min");
		console.log("min value is " + t);
		jQuery("#amttospd").val(t);
		calcNew();
	});
	
	// Trigger a click on the first TAB when the page loads
	jQuery("ul.nav.nav-tabs li a")[0].click();
	
});

function calculate(depositAmt)
{
	jQuery("#amttospd").val(depositAmt);
	calcNew();
}
function calcNew() 
{
	// Get User Input
	var money = parseFloat($("#amttospd").val().replace(/^\s+|\s+$/,''));
	var plan = "";
	if( money == '' || isNaN(money) ) money = 0;
	
	// Find the Percentage
	/*
	var matchText = "\$" + money
    jQuery(".tab-pane.active td").each(function()
	{  
	   var t = jQuery(this).text(); 
	   if(t.match(/\$25\.00/)) jQuery(this).addClass('LADDU'); });	
	*/
	
	// GET TOP Plans
	if( jQuery(".nav.nav-tabs li.active").length )
	{
		
		var perc = jQuery(".nav.nav-tabs li.active a").attr("perc");
		var profit_percentage = 0;
		if( perc == 135 )
		{
			if( money >=25 && money <= 500 ) { profit_percentage = 105; plan = "plan1"; }
			if( money >=501 && money <= 1000 ) { profit_percentage = 107; plan = "plan2"; }
			if( money >=1001 && money <= 5000 ) { profit_percentage = 110; plan = "plan3"; }
			if( money >=5001 && money <= 10000 ) { profit_percentage = 120; plan = "plan4"; }
			if( money >=10001 && money <= 25000 ) { profit_percentage = 125; plan = "plan5"; }
			if( money >=25001 && money <= 50000 ) { profit_percentage = 130; plan = "plan6"; }
			if( money >=50001 && money <= 100000 ) { profit_percentage = 135; plan = "plan7"; }
		}
		else if( perc == 250 )
		{
			if( money >=25 && money <= 500 ) { profit_percentage = 117; plan = "plan1"; }
			if( money >=501 && money <= 1000 ) { profit_percentage = 125; plan = "plan2"; }
			if( money >=1001 && money <= 5000 ) { profit_percentage = 140; plan = "plan3"; }
			if( money >=5001 && money <= 10000 ) { profit_percentage = 170; plan = "plan4"; }
			if( money >=10001 && money <= 25000 ) { profit_percentage = 190; plan = "plan5"; }
			if( money >=25001 && money <= 50000 ) { profit_percentage = 220; plan = "plan6"; }
			if( money >=50001 && money <= 100000 ) { profit_percentage = 250; plan = "plan7"; }

		}
		else if( perc == 450 )
		{
			if( money >=25 && money <= 500 ) { profit_percentage = 140;  plan = "plan1"; }
			if( money >=501 && money <= 1000 ) { profit_percentage = 160;  plan = "plan2"; }
			if( money >=1001 && money <= 5000 ) { profit_percentage = 220;  plan = "plan3"; }
			if( money >=5001 && money <= 10000 ) { profit_percentage = 250;  plan = "plan4"; }
			if( money >=10001 && money <= 25000 ) { profit_percentage = 330;  plan = "plan5"; }
			if( money >=25001 && money <= 50000 ) { profit_percentage = 360;  plan = "plan6"; }
			if( money >=50001 && money <= 100000 ) { profit_percentage = 450; plan = "plan7"; }	 		
		}
		else if( perc == 900 )
		{
			if( money >=25 && money <= 500 ) { profit_percentage = 300; plan = "plan1"; }	 
			if( money >=501 && money <= 1000 ) { profit_percentage = 350; plan = "plan2"; }	 
			if( money >=1001 && money <= 5000 ) { profit_percentage = 450; plan = "plan3"; }	 
			if( money >=5001 && money <= 10000 ) { profit_percentage = 550; plan = "plan4"; }	 
			if( money >=10001 && money <= 25000 ) { profit_percentage = 700; plan = "plan5"; }	 
			if( money >=25001 && money <= 50000 ) { profit_percentage = 750; plan = "plan6"; }	 
			if( money >=50001 && money <= 100000 ) { profit_percentage = 900;	plan = "plan7"; }	  				
		}
		else if( perc == 1400 )
		{
			if( money >=25 && money <= 500 ) { profit_percentage = 450; plan = "plan1"; }	 
			if( money >=501 && money <= 1000 ) { profit_percentage = 500; plan = "plan2"; }	 
			if( money >=1001 && money <= 5000 ) { profit_percentage = 700; plan = "plan3"; }	 
			if( money >=5001 && money <= 10000 ) { profit_percentage = 800; plan = "plan4"; }	 
			if( money >=10001 && money <= 25000 ) { profit_percentage = 1000; plan = "plan5"; }	 
			if( money >=25001 && money <= 50000 ) { profit_percentage = 1200; plan = "plan6"; }	 
			if( money >=50001 && money <= 100000 ) { profit_percentage = 1400; plan = "plan7"; }	 	 				
		}
		else if( perc == 1200 )
		{
		if( money >=5000 && money <= 25000 ) { profit_percentage = 1200; plan = "plan1"; }			
		}
		else if( perc == 2500 )
		{
				if( money >=500 && money <= 25000 ) { profit_percentage = 2500; plan = "plan1"; }
		}
		else if( perc == 5000 )
		{
			if( money >=100 && money <= 25000 ) { profit_percentage = 5000; plan = "plan1"; }
		}
		
		// Start the calculation
		var total_profit = parseFloat(money * profit_percentage / 100);
		total_profit = total_profit.toFixed(2);
		jQuery("#total_profit").html(total_profit); 
		
		var total_return = parseFloat(money * profit_percentage / 100 - money);
		total_return = total_return.toFixed(2);
		jQuery("#total_return").html(total_return);
		
		// console.log( "Step 2 :",money, total_profit, total_return);
		//
		// Remove Active class from Current PLANS
		jQuery(".tab-content .tab-pane.active table tr").removeClass('active');
		
		if( money != 0 && plan != "")
		{
			// Add active class 
			setTimeout( function()
			{
			   jQuery(".tab-content .tab-pane.active table tr." + plan).addClass('active');
			}, 200);
			console.log(".tab-content .tab-pane.active table tr." + plan);
		}
		else
		{
			console.log("Exception");
		}
		
	}
}
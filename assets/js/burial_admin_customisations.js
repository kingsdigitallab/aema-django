// Burials admin customisations

jQuery(function($){

    $('fieldset.module.aligned h2:contains("Grave goods")')
        .parent()
        .after(
            $('.inline-group.inline-stacked h2:contains("Grave Goods")').parent()
        )

    $('fieldset.module.aligned h2:contains("Burial details")')
        .parent()
        .after(
            $('.inline-group.inline-stacked h2:contains("Burial Individual")').parent()
        )
	
});

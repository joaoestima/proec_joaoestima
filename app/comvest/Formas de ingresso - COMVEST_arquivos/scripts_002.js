/**
 * Scripts de experiência front-end
 *
 * Autor: Infinito Web Sites
 * URL do Autor: http://www.infinito.com.br
**/
jQuery( document ).ready( function() {
   
    // imagesLoaded( 'body', function() {            
    if( window.innerWidth > 900 ){
        jQuery('#sidebar-collapse').addClass('in');        
    } else {
        jQuery( '#sidebar-toggle a' ).click(function(event) {
            if( jQuery( '#sidebar-toggle a .fa' ).hasClass('fa-chevron-down') ) {
                jQuery( '#sidebar-toggle a .fa' ).removeClass('fa-chevron-down').addClass('fa-chevron-up');
            } else {
                jQuery( '#sidebar-toggle a .fa' ).removeClass('fa-chevron-up').addClass('fa-chevron-down');
            }
        });
    }

    jQuery( '#loading' ).fadeOut( 400 );
    // });  

});

function calcular_prazo_frete() {
    jQuery.ajax({
        url: myAjax.ajaxurl,
        dataType: 'json',
        type: 'POST',
        data: {
            'action' : 'calcular_prazo_frete',
            'cep' : jQuery( '#zipcode' ).val()
        },
        beforeSend : function() {
            jQuery( '#wc-correios-simulator' ).block();
        }
    }).success( function( r ) {
        if( r.PrazoEntrega != undefined && r.PrazoEntrega != null ) {
            var prazo = r.PrazoEntrega + 2;
            jQuery( '#simulator-data' ).html( "Prazo estimado: " + prazo + " dias." );
            jQuery( '#wc-correios-simulator' ).unblock();
        }        
    });
}
// detecta se é uma determinada pá´gina
function is_page( p ) {
     var url = window.location.toString();
    if( ( (url.indexOf( p ) > 0 ) ) ) return true;
    return false;
}
// detecta se é a home do site
function is_home() {
    var url = window.location.toString();
    if( (url.indexOf( 'home' ) > 0 ) || ( url.indexOf( '?page_id=' ) < 0 ) ) return true;
    return false;
}
function resize_home_slider() {
    var wh = window.innerHeight; // tela - menu
    jQuery( '#home-slider .item>div' ).css( 'height', wh );
}
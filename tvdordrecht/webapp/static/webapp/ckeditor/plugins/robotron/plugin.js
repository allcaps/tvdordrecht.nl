CKEDITOR.plugins.add( 'robotron', {
    requires: 'widget',
    icons: 'robotron',

    init: function( editor ) {
        editor.widgets.add( 'robotron', {
            button: 'Create a jumbotron box',

            template: 
                '<div class="jumbotron">' +
                '</div>',
        
            editables: {
//                 title: {
//                     selector: '.simplebox-title'
//                 },
                content: {
                    selector: '.jumbotron'
                }
            },
            
            // allowedContent: 'div(!robotron); div(!simplebox-content); h2(!simplebox-title)',
            requiredContent: 'div(jumbotron)',
            
            upcast: function( element ) {
                return element.name == 'div' && element.hasClass( 'jumbotron' );
            }
        
        } );
    },

} );

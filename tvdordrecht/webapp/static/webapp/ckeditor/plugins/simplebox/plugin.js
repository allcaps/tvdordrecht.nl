CKEDITOR.plugins.add( 'simplebox', {
    requires: 'widget',
    icons: 'simplebox',

    init: function( editor ) {
        editor.widgets.add( 'simplebox', {
            button: 'Create a simple box',

            template: 
                '<div class="robotron">' +
                    '<h2 class="simplebox-title">Title</h2>' +
                    '<div class="simplebox-content"><p>Content...</p></div>' +
                '</div>',
        
            editables: {
                title: {
                    selector: '.simplebox-title'
                },
                content: {
                    selector: '.simplebox-content'
                }
            },
            
            allowedContent:
                'div(!robotron); div(!simplebox-content); h2(!simplebox-title)',
        
            requiredContent: 'div(robotron)',
            
            upcast: function( element ) {
                return element.name == 'div' && element.hasClass( 'robotron' );
            }
        
        } );
    },

} );

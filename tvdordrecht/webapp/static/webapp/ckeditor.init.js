var $ = django.jQuery;

CKEDITOR.on("instanceReady", function( ev ) {
    ev.editor.on("paste", function( evt ) {
        var data = $.parseHTML(evt.data.dataValue);
        $( "th p, td p", data).each( function() {
            $( this ).replaceWith(  $( this ).contents() );
            });
        evt.data.dataValue = $('<div>').append(data).html();
        }, 12);
    });


CKEDITOR.stylesSet.add( 'bootstrap_styles', [
    { name: 'Lead', element: 'p', attributes: { 'class': 'lead' } },
    { name: 'Small', element: 'p', attributes: { 'class': 'small' } },
    { name: 'Link as big button', element: 'a', attributes: { 'class': 'btn-lg btn-success' } },
    { name: 'Link as button', element: 'a', attributes: { 'class': 'btn btn-default' } },
    { name: 'Link as blue button', element: 'a', attributes: { 'class': 'btn btn-primary' } },
    { name: 'Link as green button', element: 'a', attributes: { 'class': 'btn btn-success' } },
    { name: 'Table', element: 'table', attributes: { 'class': 'table table-striped' } }
]);

$(document).ready(function(){  

   $( "#id_text" ).wrap('<div style="border:1px solid #eee; margin-left: 190px;"></div>');

    // Template
    var tpl = new CKEDITOR.template( '<div class="{cls}">{label}</div>' );


    CKEDITOR.replace( 'id_text', {
        contentsCss: '/static/webapp/editor.css',
        entities_latin: false,
        basicEntities: false,
        ignoreEmptyParagraph: true,
        stylesSet: 'bootstrap_styles',
        allowedContent: 'div(jumbotron); div(robotron); div h2(simplebox-title); div p(simplebox-content); h1 h2 h3 p a ul ol li strong em; p(lead); a[href]; a(btn); a(btn-default); a(btn-primary); a(btn-success); a(btn-lg); table(table); table(table-striped); thead tfoot tbody tr td th; iframe[*]; img[src]; img(img-responsive); p(small)',
        extraPlugins: 'robotron,iframe',
        toolbar: [
            [ 'Source'], ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo'], 
            ['Format', 'Styles'], ['Bold', 'Italic'], ['BulletedList', 'NumberedList'], ['Link', 'Unlink' ],
            ['Image', 'Table', 'simplebox'], ['RemoveFormat', 'Simplebox', 'Robotron'], ['Find'], ['ShowBlocks', 'Maximize']
        ]    
    });
    
});
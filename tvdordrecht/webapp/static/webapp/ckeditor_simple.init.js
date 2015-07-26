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
]);

$(document).ready(function() {
    $("textarea").each(function(){
        CKEDITOR.replace(this.id, {
            contentsCss: '/static/webapp/editor.css',
            entities_latin: false,
            basicEntities: false,
            ignoreEmptyParagraph: true,
            stylesSet: 'bootstrap_styles',
            allowedContent: 'div(jumbotron); div(robotron); div h2(simplebox-title); div p(simplebox-content); h2 h3 p a ul ol li strong em; p(lead); a[href]; a(btn); a(btn-default); a(btn-primary); a(btn-success); a(btn-lg); table(table); table(table-striped); thead tfoot tbody tr td th; iframe[*]; img[src]; img(img-responsive); p(small)',
            extraPlugins: 'robotron,iframe',
            toolbar: [
                ['Undo', 'Redo'], ['Cut', 'Copy', 'Paste'],
                ['Format', 'Styles'], ['Italic'], ['BulletedList', 'NumberedList'], ['Link', 'Unlink'],
                ['Table'], ['RemoveFormat'], ['Maximize']
            ]
        });
    });
});

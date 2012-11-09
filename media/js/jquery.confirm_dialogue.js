/* author: cyberquatro */
/* license: bsd */
(function( $ ){
    $.fn.cdialog = function(options){
        var settings = $.extend({
            type: 'confirm'
        }, options);
        this.each(function(){
            el = this;
            url = $(el).data('href');
            cb = $(el).data('cb');
            yes_btn = $(el).data('btn');
            msg = $(el).data('message');
            /* selecting template from given options */
            switch (settings.type){
                case 'confirm':
                    template = '#showConfirmDialogue';
                    break
                case 'inform':
                    template = '#showInformDialogue';
                    break
                default:
                    template = '#showConfirmDialogue';
            }
            t = $.template(template);
            $.tmpl(t, {
                url: url,
                ajax: cb ? cb : false,
                yes_btn: yes_btn,
                msg: msg
            }).appendTo('body');
            $('#confirm-dialogue').modal('show');
        });
    }
})(jQuery);

$(function () {
    $(document.body).on(
        'click', //event
        '[data-dialog*="-dialog"]', //selector
        function (e) { //event handler
            if (String($(this).data('dialog')).indexOf('confirm') > -1){
                $(this).cdialog(); //run cdialog
            }
            if (String($(this).data('dialog')).indexOf('inform') > -1){
                $(this).cdialog({'type': 'inform'}); //run idialog
            }
        }
    );
});


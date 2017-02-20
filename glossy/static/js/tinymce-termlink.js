(function () {
    tinymce.PluginManager.add('termlink', function (editor, url) {
        editor.addButton('termlink', {
            text: 'Termi',
            icon: false,
            onclick: function () {
                var terms = [{'text': '---', 'value': '---'}].concat(window.TERMLINK_MENU);
                editor.windowManager.open({
                    title: 'Lisää termiviittaus',
                    body: [
                        {type: 'textbox', name: 'text', label: 'Teksti', value: editor.selection.getContent()},
                        {type: 'listbox', name: 'term', label: 'Termi', values: terms},
                    ],
                    onsubmit: function (e) {
                        if(!e.data.term) {
                            return;
                        }
                        var term = null;
                        for(var i=0; i < window.TERMLINK_MENU.length; i++){
                            var menu = window.TERMLINK_MENU[i].menu;
                            for(var j=0; j < menu.length; j++) {
                                if(menu[j].value == e.data.term){
                                    term = menu[j];
                                }
                            }
                        }
                        var html = [
                            '<a class="glossy-term" data-id="',
                            term.data_id,
                            '" data-parent-id="',
                            term.data_parent_id,
                            '" href="',
                            term.url,
                            '">',
                            term.text,
                            '</a>',
                        ].join('');
                        editor.insertContent(html);
                    },
                });
            }
        });
    });
}());

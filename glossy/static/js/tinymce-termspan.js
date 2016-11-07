(function () {
    tinymce.PluginManager.add('termspan', function (editor, url) {
        editor.addButton('termspan', {
            text: 'Termi',
            icon: false,
            onclick: function () {
                var terms = [{'text': '---', 'value': '---'}].concat(window.TERMSPAN_MENU);
                editor.windowManager.open({
                    title: 'Lisää termiviittaus',
                    body: [
                        {type: 'textbox', name: 'text', label: 'Teksti'},
                        {type: 'listbox', name: 'term', label: 'Termi', values: terms},
                    ],
                    onsubmit: function (e) {
                        if(!e.data.term) {
                            return;
                        }
                        var html = [
                            '<span class="glossy-term" data-term-id="',
                            e.data.term,
                            '">',
                            e.data.text,
                            '</span>',
                        ].join('');
                        editor.insertContent(html);
                    },
                });
            }
        });
    });
}());

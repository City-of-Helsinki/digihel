(function () {
    tinymce.PluginManager.add('termspan', function (editor, url) {
        editor.addButton('termspan', {
            text: 'Termi',
            icon: false,
            onclick: function () {
                const terms = [
                    {
                        text: 'foo',
                        menu: [
                            {text: 'asdf', value: 'foo'},
                            {text: 'rerr', value: 'blep'},
                        ],
                    },
                    {
                        text: 'quux',
                        menu: [
                            {text: 'aawrtsdf', value: 'ahrarhw'},
                            {text: 'wryuw', value: 'awrhahwr'},
                        ],
                    },
                ];
                editor.windowManager.open({
                    title: 'Lisää termiviittaus',
                    body: [
                        {type: 'textbox', name: 'text', label: 'Teksti'},
                        {type: 'listbox', name: 'title', label: 'Termi', values: terms},
                    ],
                    onsubmit: function (e) {
                        console.log(e.data);
                        editor.insertContent('Title: ' + e.data.title);
                    }
                });
            }
        });
    });
}());

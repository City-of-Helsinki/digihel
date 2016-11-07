(function ($) {
    var GLOSSY_TERMS_URL = window.GLOSSY_TERMS_URL || '/glossy-terms/';
    var termMapping = {};

    /**
     * Retrieve term definitions for each `glossy-term` span in the DOM
     * from the Glossy terms AJAX API.
     *
     * @returns {*} jQuery ajax promise
     */
    function retrieveTermDefinitions() {
        var $terms = $('span.glossy-term');
        var termIds = [];
        $terms.each(function () {
            var termId = $(this).data('term-id');
            if (termId && !termMapping[termId]) {
                termIds.push(termId);
            }
        });
        if (!termIds.length) {
            return;
        }
        return $.ajax({
            url: GLOSSY_TERMS_URL,
            data: {ids: termIds.join(',')},
        });
    }

    /**
     * Replace `glossy-term` `span`s with abbrs for currently known terms.
     */
    function replaceTermSpans() {
        $('span.glossy-term').each(function () {
            var $term = $(this);
            var termInfo = termMapping[$term.data('term-id')];
            if (!termInfo) {
                return;
            }
            var $abbr = $('<abbr>', {
                class: 'glossy-term replaced',
                'data-term-id': termInfo.id,
                html: $term.html(),
                title: termInfo.body.replace(/<[^>]+>/g, ' '),
            });
            $term.replaceWith($abbr);
        });
    }

    $(function () {
        retrieveTermDefinitions().done(function (data) {
            termMapping = $.extend(termMapping, data);
            replaceTermSpans();
        });
    });
}(jQuery));

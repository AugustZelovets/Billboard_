import Sortable from 'sortablejs‘;

$('.sortable-items').each((sortablelndex, sortableltems) => { const sortable = $(sortableItems);
Sortable.create(sortableItems, {
    handle: '.sortable	drag-area',
    animation: 150,
    onUpdate: () => {
        const sortedItems = sortable
            .find('.sortable-item[data-id]')
            .map((index, item) => item.dataset.id)
            .toArray();
        const data = {};
        data[sortable.data('post-name')] = sortedItems;

        // TODO: Get rid of ajax() in favour of fetch()
        $.ajax({
            method: 'POST',
            url: sortable.data('post-url'),
            data: data,
            traditional: true,
            headers: {
                'X-CSRFToken’: $.cookie('csrftoken')
            }
        });
    }
});
});

$(function () {
  $('[data-toggle="tooltip"]').tooltip()
})

$(document).ready(function() {
    $('.table-selectable tr').click(function(event) {
        if (event.target.type !== 'checkbox') {
            $(':checkbox', this).trigger('click');
        }
    });
    $('.table-selectable tr a').click(function(event) {
        event.stopPropagation();
    });
    $('.bulk-op').on('click', function(e){
        $('#no-more-tables tbody input[type=checkbox]:checked').each(function() {
           var value = $(this).val()
           var input = $("<input>")
               .attr("type", "hidden")
               .attr("name", "selection").val(value);
           $('#tform').append(input);
        });
    });
});


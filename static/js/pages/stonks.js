
$(document).ready(function get_query() {
    // add task status elements
    divs = $('');
    

    // send ajax POST to get the query data
    $.ajax({
        type: 'POST',
        url: '/get_posts',
        success: function (response) {
            re = JSON.parse(response)
            $('#posts')[0].innerHTML = ''
            for( var el in re ) {
                if (el > 20){
                    break
                }
                div = $('<div><a></a></div>');
                div[0].childNodes[0].textContent = re[el]['text']
                div[0].childNodes[0].setAttribute( 'href' , 'https://www.ozbargain.com.au' + re[el]['link'])
                $('#posts').append(div)
            }
        },
        error: function () {
            alert('Unexpected error');
        }
    });
})
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function rate(event, that)
{
    console.log("clicked");
    const $this = $(that);
    console.log($this);
    const request = new Request(
        '/rate/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: JSON.stringify(
                {
                    'obj_id': $this.data('obj_id'),
                    'obj_name': $this.data('obj_name'),
                    'action_name': $this.data('action_name')
                }
            )
        }
    );

    fetch(request).then(function (response) {
        const result = response.json().then(function (parsed) {
            if (parsed.code == 'FAIL')
                return;
            let like_btn = $(".btn-rate[data-obj_id='" + $this.data('obj_id') + "'][data-obj_name='" + $this.data('obj_name') + "'][data-action_name='like']");
            let dislike_btn = $(".btn-rate[data-obj_id='" + $this.data('obj_id') + "'][data-obj_name='" + $this.data('obj_name') + "'][data-action_name='dislike']");
            if (parsed.selection == 1) {
                like_btn.addClass('rated');
                dislike_btn.removeClass('rated');
            } else if (parsed.selection == -1) {
                like_btn.removeClass('rated');
                dislike_btn.addClass('rated');
            } else {
                like_btn.removeClass('rated');
                dislike_btn.removeClass('rated');
            }
            like_btn.children("val").text(parsed.likes_count);
            dislike_btn.children("val").text(parsed.dislikes_count);
        });
    })
}

function answer_correct(event, that)
{
    const $this = $(that);
    const request = new Request(
        '/answer-correct/',
        {
            method: 'post',
            headers: {
                'X-CSRFToken': csrftoken,
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'answer_id=' + $this.data('answer_id')
        }
    );
    fetch(request).then(function (responce) {
        const result = responce.json().then(function (parsed) {
            console.log(parsed.cb_status)
            $this.prop("checked", parsed.cb_status)
        });
    })
}

$(document).on('click', '.btn-rate', function (event){
    rate(event, this);
});

$(document).on('click', '.cb-correct-answer', function (event){
    answer_correct(event, this);
})
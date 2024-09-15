const followButton = document.querySelector('#follow')
const headings=document.querySelector(".article").querySelectorAll("h2, h3, h4, h5")
const likeButtons = document.querySelectorAll('#comment')


const commentSubmitBtn = document.querySelector('.comment-submit-btn');


console.log("headings:" + headings)
if (headings.length > 0) {
    for (let i = 0; i < headings.length; i++) { 
        headings[i].classList.add("text-danger");
    }
}
function getCookie(name){
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}


function followStatus() {
    let author_id = followButton.value;
    fetch(`/follow_status/${author_id}`)
        .then(response => response.json())
        .then(result => {
            if (result.following) {
                followButton.innerHTML = 'Unfollow'
            } else {
                followButton.innerHTML = 'Follow'
            }
        })
        .catch(error => {
            console.error('Error fetching follow status:', error);
        });
}

window.addEventListener('load', followStatus);

if(followButton){

    followButton.addEventListener('click', () => {
        let author_id = followButton.value
        fetch(`/follow/${author_id}`, {
            method: 'POST',
            headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
            body: JSON.stringify({
                author_id: author_id
            }),
            
        })
        .then(response => response.json())
        .then(result => {

            if (result.message === 'followed') {
                followButton.innerHTML = 'Unfollow'
            } else if (result.message === 'unfollowed') {
                followButton.innerHTML = 'Follow'
            }
        })

    })
}


if(likeButtons){

    function likeStatus(comment_id) {
        let icon = document.querySelector(`.heart_${comment_id}`);
        console.log("heard")
        fetch(`/like_status/${comment_id}`)
            .then(response => response.json())
            .then(result => {
                if (result.liked) {
                    icon.classList.toggle('text-danger');
                }
            })
            .catch(error => {
                console.error('Error fetching like status:', error);
            });
    }
    
    likeButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            let comment_id = this.getAttribute("data-post-id");
            fetch(`/like/${comment_id}`, {
                method: 'POST',
                headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
                body: JSON.stringify({
                    comment_liked: comment_id
                }),
            })
            .then(response => response.json())
            .then(result => {
                let icon = document.querySelector(`.heart_${comment_id}`)
                let countElement = document.querySelector(`.like_count_${comment_id}`)
                let count = parseInt(countElement.innerHTML)
                if (result.message === 'like added') {
                    icon.classList.toggle('text-danger');
                    count += 1
                    countElement.innerHTML=count
                } else if (result.message === 'like removed') {
                    icon.classList.toggle('text-danger');
                    count -= 1
                    countElement.innerHTML=count
                }
            })
            .catch(error => {
                console.error('Error liking/unliking:', error);
            });
        });
    });

    
    likeButtons.forEach(btn => {
        let comment_id = btn.getAttribute("data-post-id")
        likeStatus(comment_id)
    });
}
if(commentSubmitBtn){

    commentSubmitBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const commentBody = document.getElementById('comment-body');
        const text = commentBody.value;
        const form = document.getElementById('comment-form');
        const article_id = form.getAttribute('data-article-id');


        console.log(article_id);  
        console.log(text)


        console.log("CSRF Token: ", getCookie('csrftoken'));
        fetch(`/comment/${article_id}`, {
            method: 'POST',
            headers: {"Content-type": "application/json", "X-CSRFToken": getCookie("csrftoken")},
            body: JSON.stringify({
                text: text
            }),
        })
        .then(response => response.json())
        .then(result => {
            console.log("Comment body: ", text);
            if (result.error) {
                console.log("CSRF Token: ", getCookie('csrftoken'));
                console.error(result.error);
                return;
            }
            else{
            let newComment = document.createElement('div');
            newComment.className = 'comment rounded border border-danger d-flex m-3 flex-start align-items-stretch';

            newComment.innerHTML = `
                <svg style="align-self:center" xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="currentColor" class="text-light m-2 bi bi-person-fill" viewBox="0 0 16 16">
                    <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6"/>
                </svg>
                <div class="border-danger p-2">
                    <h6 class="fw-bold mb-1 text-danger">${result.commenter}</h6>
                    <div class="d-flex align-items-center mb-3">
                        <p class="mb-0 text-light">${result.text}</p>
                    </div>
                </div>
            `;

            document.querySelector('.comments').appendChild(newComment);

            commentBody.value = '';
            }
        })
        .catch(error => console.error('Error:', error));
    });
}
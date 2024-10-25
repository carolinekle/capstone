const followButton = document.querySelector('#follow')

const likeButtons = document.querySelectorAll('#comment')


const commentSubmitBtn = document.querySelector('.comment-submit-btn')

/** hero image code*/
const imgEl = document.querySelector('.hero-img')
imgEl.addEventListener("load",  function() {

    console.log(imgEl)
        const rgb = getAverageRGB(imgEl);

        document.body.style.backgroundColor = 'rgb(' + rgb.r + ',' + rgb.g + ',' + rgb.b + ')'
        const brightness = getBrightness(rgb)
        const text = document.querySelectorAll(".hero-text")

text.forEach( item =>{
        if (brightness > 80) {
            console.log(item)
            item.classList.remove("link-dark", "link-light")
            item.classList.add("link-light")
        } else {
            item.classList.remove("link-dark", "link-light")
            item.classList.add("link-dark")
        }
    })
})

function getAverageRGB(imgEl) {
    var blockSize = 5, 
        defaultRGB = {r: 0, g: 0, b: 0}, 
        canvas = document.createElement('canvas'),
        context = canvas.getContext && canvas.getContext('2d'),
        data, width, height,
        i = -4,
        length,
        rgb = {r: 0, g: 0, b: 0},
        count = 0;

    if (!context) {
        return defaultRGB;
    }

    height = canvas.height = imgEl.naturalHeight || imgEl.offsetHeight || imgEl.height
    width = canvas.width = imgEl.naturalWidth || imgEl.offsetWidth || imgEl.width

    context.drawImage(imgEl, 0, 0)

    try {
        data = context.getImageData(0, 0, width, height)
    } catch (e) {
    
        console.error('Image loading error', e)
        return defaultRGB;
    }

    length = data.data.length

    while ((i += blockSize * 4) < length) {
        ++count;
        rgb.r += data.data[i]
        rgb.g += data.data[i + 1]
        rgb.b += data.data[i + 2]
    }

    rgb.r = ~~(rgb.r / count)
    rgb.g = ~~(rgb.g / count)
    rgb.b = ~~(rgb.b / count)

    return rgb;
}

function getBrightness(rgb) {
    return Math.round((rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000)
}

/*headings*/ 
const headings=document.querySelector(".article").querySelectorAll("h2, h3, h4, h5")
if (headings.length > 0) {
    for (let i = 0; i < headings.length; i++) { 
        headings[i].classList.add("text-danger")
    }
}

function getCookie(name){
    const value = `; ${document.cookie}`
    const parts = value.split(`; ${name}=`)
    if(parts.length == 2) return parts.pop().split(';').shift()
}
/** AJAX */
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
            console.error('Error fetching follow status:', error)
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
                console.error('Error fetching like status:', error)
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
                console.error('Error liking/unliking:', error)
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
        const commentBody = document.getElementById('comment-body')
        const text = commentBody.value
        const form = document.getElementById('comment-form')
        const article_id = form.getAttribute('data-article-id')


        console.log(article_id);  
        console.log(text)


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

            document.querySelector('.comments').appendChild(newComment)
            let alert=document.querySelector('.comment-alert').remove()
                alert.remove()
            commentBody.value = ''
            }
        })
        .catch(error => console.error('Error:', error))
    });
}
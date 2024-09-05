const followButton = document.querySelector('#follow')
const headings=document.querySelector(".article").querySelectorAll("h2, h3, h4, h5")

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

tinymce.init({
    selector: '#content-field',
    plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount linkchecker',
    toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | addcomment showcomments | spellcheckdialog a11ycheck typography | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
    height: '500',
    width:'800',
    tinycomments_mode: 'embedded',
    tinycomments_author: 'Author name',
    mergetags_list: [
      { value: 'First.Name', title: 'First Name' },
      { value: 'Email', title: 'Email' },
    ],
    
});

let btnContainer = document.querySelector('.dash');

let error =document.querySelector('.errorlist')

if (error){
  error.classList.add("alert alert-warning")
}

btnContainer.addEventListener('mouseover', (event) => {
  if (event.target.classList.contains('btn')) {
    let parentDiv = event.target.closest('.btn-parent');
    let relatedLink = parentDiv.querySelector('.btn-hover');

    if (relatedLink) {
      relatedLink.classList.remove("link-dark");
      relatedLink.classList.add("link-light");
    }
  }
});

btnContainer.addEventListener('mouseout', (event) => {
  if (event.target.classList.contains('btn')) {
    let parentDiv = event.target.closest('.btn-parent');
    let relatedLink = parentDiv.querySelector('.btn-hover');

    if (relatedLink) {
      relatedLink.classList.remove("link-light");
      relatedLink.classList.add("link-dark");
    }
  }
});

